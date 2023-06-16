from typing import Tuple, Dict
import numpy as np
import pickle


class KGE(object):
  def __init__(self, model_path: str):
    """
    Load a KGE embedding model from graphvite [1].

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

  def __contains__(self, identifier: str) -> bool:
    return identifier in self.e2id

  def embed_entity(self, identifier: str) -> np.array:
    """
    Retrieve the embedding of an entity.

    Args:
        identifier (str): Wikidata identifier of the entity

    Returns:
        np.array: Embedding using numpy vector.
    """
    return self.ee[self.e2id[identifier]]

  def embed_predicate(self, identifier: str) -> np.array:
    """
    Retrieve the embedding of a predicate.

    Args:
        identifier (str): Wikidata identifier of a predicate

    Returns:
        np.array: Embedding using numpy vector.
    """
    return self.pe[self.p2id[identifier]]
