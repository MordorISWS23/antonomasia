import abc

from typing import Tuple, Dict
from functools import lru_cache
import numpy as np
import pickle
import gensim.downloader

from wikidata.client import Client

from antonomasia.utils import Sample

class BaseEmbedding(abc.ABC):
  """
  Base class for an embedding method. 
  The class implements the method __contains__ to check whether a Wikidata
  IRI is part of the embedding set.

  The methods embed_entity and embed_predicate are used to retrieve the
  emebddings of an entity and a predicate, respectively.
  """

  @lru_cache(maxsize=100)
  def __contains__(self, s: Sample) -> bool:
    """
    Check wether the embedding method includes the provided identifier.

    Args:
        s (Sample): Sample to be checked against the available ones in the embedding method.
    Returns:
        bool: True if the embedding contains the identifier, False otherwise.
    """
    raise NotImplementedError

  @lru_cache(maxsize=100)
  def embed_entity(self, s: Sample) -> np.array:
    """
    Compute the embedding for the provided entity.

    Args:
        s (Sample): Sample to be checked against the available ones in the embedding method.

    Returns:
        np.array: Embedding vector
    """
    raise NotImplementedError

  @lru_cache(maxsize=100)
  def embed_predicate(self, s: Sample) -> np.array:
    """
    Compute the embedding for the provided predicate.

    Args:
        s (Sample): Sample to be checked against the available ones in the embedding method.

    Returns:
        np.array: Embedding vector
    """
    raise NotImplementedError


class KGE(BaseEmbedding):
  def __init__(self, model_path: str):
    """
    Initialise the Knowledge Graph Embeddings trained using graphvite [1].

    [1] https://graphvite.io/docs/latest/index.html

    Args:
        model_path (str): Path to the embedding model.
    """
    with open(model_path, "rb") as f:
      model = pickle.load(f)
    
    self.e2id = model.graph.entity2id
    self.p2id = model.graph.relation2id
    self.id2e = { v: k for k, v in self.e2id.items() }
    self.ee = model.solver.entity_embeddings
    self.pe = model.solver.relation_embeddings

  def __contains__(self, s: Sample) -> bool:
    """
    Check if the Wikidata identifier is in the embedding model,
    essentially check if the identifier is within the Wikidata5M
    dataset [1]

    [1] Wang, X., Gao, T., Zhu, Z., Zhang, Z., Liu, Z., Li, J., & Tang, J. (2021). 
      KEPLER: A unified model for knowledge embedding and pre-trained language representation. 
      Transactions of the Association for Computational Linguistics, 9, 176-194.

    Args:
        s (Sample): Sample to be checked against the available ones in the embedding method.

    Returns:
        bool: True if the KGE contains the entity s
    """
    return s.wikidata_iri in self.e2id

  def embed_entity(self, s: Sample) -> np.array:
    """
    Retrieve the embedding of an entity.

    Args:
        s (Sample): Sample to be checked against the available ones in the embedding method.

    Returns:
        np.array: Embedding using numpy vector.
    """
    return self.ee[self.e2id[s.wikidata_iri]]

  def embed_predicate(self, s: str) -> np.array:
    """
    Retrieve the embedding of a predicate.

    Args:
        s (str): Wikidata ID of the predicate

    Returns:
        np.array: Embedding using numpy vector.
    """
    return self.pe[self.p2id[s]]


class WordEmbedding(BaseEmbedding):
  def __init__(self, method: str):
    """
    Word embeddings are implemented using the pretrained model from the
    gensim library [1].

    [1] https://radimrehurek.com/gensim/

    Args:
        method (str): Method to use for the word embeddings
    """
    if method == "word2vec":
      self.emb = gensim.downloader.load("word2vec-google-news-300")
    elif method == "glove":
      self.emb = gensim.downloader.load("glove-wiki-gigaword-300")
    else:
      raise ValueError(f"{method} is not a supported embedding method!")
      
  def __contains__(self, s: Sample) -> bool:
    """
    Check if the provided string is part of the word embedding method.
    Split s into multiple components if whitespaces are present and check
    that all the components are present in the embedding.

    Args:
        s (Sample): Sample to be checked against the available ones in the embedding method.

    Returns:
        bool: True if the embedding method contains s, False otherwise
    """
    return all([l in self.emb for l in s.label.split()])

  def embed_entity(self, s: Sample) -> np.array:
    """
    Retrieve the embedding of a string s.
    If multiple whitespace speareted tokens are present in s the
    embedding of the different components is obtained by averaging
    all the different values.

    Args:
        s (Sample): Sample to be checked against the available ones in the embedding method.

    Returns:
        np.array: Embedding using numpy vector.
    """
    embs = [self.emb[w] for w in s.label.split() if w in self.emb]
    if len(embs) > 0:
      emb = np.average(np.stack(embs), axis=0)
    else:
      emb = np.random.random(self.emb.vector_size)
    return emb

  def embed_predicate(self, s: str) -> np.array:
    """
    A predicate is embedded equivalently to an entityt. 
    See ~embed_entity.

    Args:
        s (str): Wikidata ID of the predicate

    Returns:
        np.array: Embedding using numpy vector.
    """
    client = Client()
    label = str(client.get(s, load=True).label)
    return self.embed_entity(Sample(s, label, []))


class MetaEmbedding(BaseEmbedding):
  def __init__(self, word_embedding: WordEmbedding, kge: KGE, method: str = "concatenate"):
    """
    Initialise the meta-embedding method, which fuses together word embeddings
    and Knowledge Graph embeddings.

    Args:
        word_embedding (WordEmbedding): Word embedding method.
        kge (KGE): Knowledge Graph Embedding method.
    """
    self.kge = kge
    self.we = word_embedding

    assert method in ["concatenate", "average"]
    self.method = method

  def __contains__(self, s: Sample) -> bool:
    """
    Check if the provided string is part of both the embedding methods.

    Args:
        s (Sample): Sample to be checked against the available ones in the embedding method.

    Returns:
        bool: True if the embedding method contains s, False otherwise
    """
    return (s in self.kge) and (s in self.we)

  def _combine_embeddings(self, a: np.array, b: np.array) -> np.array:
    """
    Combine two embeddings together.

    Args:
        a (np.array): embedding a
        b (np.array): embedding b

    Returns:
        np.array: Combined embedding
    """
    if self.method == "concatenate":
      emb = np.concatenate((a, b))
    elif self.method == "average":
      max_d = max(a.shape[0], b.shape[0])
      a = np.pad(a, [(0, max_d - a.shape[0])])
      b = np.pad(b, [(0, max_d - b.shape[0])])
      emb = np.mean(np.array([a, b]), axis=0)
    
    return emb    

  def embed_entity(self, s: Sample) -> np.array:
    """
    Retrieve the embedding of a string s.
    If multiple whitespace speareted tokens are present in s the
    embedding of the different components is obtained by averaging
    all the different values.

    Args:
        s (Sample): Sample to be checked against the available ones in the embedding method.

    Returns:
        np.array: Embedding using numpy vector.
    """
    kge_emb = self.kge.embed_entity(s)
    we_emb = self.we.embed_entity(s)
    emb = self._combine_embeddings(kge_emb, we_emb)
    return emb

  def embed_predicate(self, s: str) -> np.array:
    """
    A predicate is embedded equivalently to an entityt. 
    See ~embed_entity.

    Args:
        s (str): Input string

    Returns:
        np.array: Embedding using numpy vector.
    """
    kge_emb = self.kge.embed_predicate(s)
    we_emb = self.we.embed_predicate(s)
    emb = self._combine_embeddings(kge_emb, we_emb)
    return emb