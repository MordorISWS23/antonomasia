from typing import List, Tuple, Callable
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

from antonomasia.embeddings import BaseEmbedding
from antonomasia.utils import Sample

class AntonomasiaGenerator(object):

  def __init__(self, emb: BaseEmbedding, b_pool: List[Tuple[str, List[str]]]):
    """
    Initialise the generator using an embedding method and a pool of candidates.

    Args:
        emb (BaseEmbedding): The embedding method used to obtain vectorial representations.
        b_pool (List[Tuple[str, List[str]]]): List B candidates to draw from in the form of tuples.
          The format is (Wikidata IRI, classifying features) where the classifying features 
          are a list of strings that classify an entity, e.g. its profession.
    """
    self.emb = emb
    self.b_pool = [b for b in b_pool if b in self.emb]

  def top_k(self, a: np.array, b: np.array, 
            k: int = 10, 
            magnitude_sort: bool = False, 
            similarity_fn: str = "cosine") -> Tuple[np.array, np.array]:
    """
    Computes the similarity between the vector a and the set of vectors b.
    The similarity is then used to retrieve the top-k b vectors that maximises
    the similarity with a.

    Args:
        a (np.array): Vectorial representation of A.
        b (np.array): Set of vectors representing the possible Bs.
        k (int, optional): Number of top results. Defaults to 10.
        magnitude_sort (bool, optional): Further sort the top-k values according 
          to the magnitude of their vectors. If set to True, higher values are
          supposed to be more surprising from a creative point of view.
          Defaults to False.
        similarity_fn (str, optional): Set the similarity function.
          Defaults to scipy's implementation of cosine similarity.

    Returns:
        Tuple[np.array, np.array]: A tuple containing the index of the top-k 
          results together with their similarity score.
    """
    if similarity_fn == "cosine":
      similarity_fn = cosine_similarity
      reverse = True
    elif similarity_fn == "euclidean":
      similarity_fn = euclidean_distances
      reverse = False
    else:
      raise ValueError(f"similarity function {similarity_fn} is not supported!")

    sim = similarity_fn(a.reshape(1, -1), b).reshape(-1)
    
    top_k = np.argsort(sim)[::-1] if reverse else np.argsort(sim)
    top_k = top_k[1:k + 1]
    
    if magnitude_sort:
      top_k = top_k[np.argsort(np.abs(b[top_k]).sum(axis=1))[::-1]]
    
    return top_k, sim

  def embed_a_b_c(self, a: Sample, c: str) -> Tuple[np.array, np.array, np.array]:
    """
    Compute the embeddings for a and c and filter the possible b accordingly to
    make sure that the classifying features of a and b are different.

    Args:
        a (Sample): Entity a sample
        c (str): Predicate for c

    Returns:
        Tuple[np.array, List[str], np.array, np.array]: Tuple containing,
          embedding of a, the filtered set of bs, embedding for those bs, and embedding for c.
    """
    a_emb = self.emb.embed_entity(a)

    # exclude entities with the same profession
    filtered_b_pool = [
      b for b in self.b_pool
      if len(set(a.classes).intersection(b.classes)) == 0
    ]

    b_emb = np.stack([self.emb.embed_entity(x) for x in filtered_b_pool])
    c_emb = self.emb.embed_predicate(c)

    return a_emb, b_emb, filtered_b_pool, c_emb

  def project_embeddings(self, a: np.array, b: np.array, c: np.array) -> Tuple[np.array, np.array]:
    """
    Compute the embeddings for a and c by projecting a and al the b to a 
    plane that is orthogonal to c. 
    The similarity between a and b is hence going to be computed in such a way
    that the characteristic c is ignored.

    Args:
        a (np.array): Embedding for a
        b (np.array): Embedding for b
        c (np.array): Embedding for c

    Returns:
        Tuple[np.array, np.array]: The embedding of a and b in the projected space
    """
    a_proj = a - (c * (np.dot(a, c) / np.dot(c, c)))
    b_proj = b - (c * (np.dot(b, c) / np.dot(c, c)).reshape(-1, 1))
    return a_proj, b_proj

  def translate_embeddings(self, a: np.array, b: np.array, c: np.array) -> Tuple[np.array, np.array]:
    """
    Compute the embeddings for a and c by removing c from both and and b to ignore
    the influence of c in the similarity computation.
    
    Args:
      a (np.array): Embedding for a
      b (np.array): Embedding for b
      c (np.array): Embedding for c

    Returns:
        Tuple[np.array, np.array]: The embedding of a and b in the projected space
    """
    a_proj = a - c
    b_proj = b - c.reshape((1, -1))
    return a_proj, b_proj

