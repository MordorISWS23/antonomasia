from typing import Tuple
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from wikidata.client import Client

from antonomasia.embeddings import KGE

class AntonomasiaGenerator(object):

  def __init__(self, kge: KGE, b_pool):
    self.kge = kge
    self.b_pool = np.array([b for b in b_pool if b[0] in self.kge])
    self.client = Client()

  def project_topk(self, a: str, c: str, k: int = 10) -> Tuple[np.array, np.array]:
    """
    Retrieve the top k candidates similar to a projected in a space orthogonal to c.

    Args:
        a (str): Identifier of the A entity.
        c (str): Identifier of the C predicate.
        k (int, optional): Number of candidates. Defaults to 10.

    Returns:
        Tuple[np.array, np.array]: Tuple containing the top k B candidates and their similarity score.
    """
    a_emb = self.kge.embed_entity(a)

    # exclude entities with the same profession
    a_entity = self.client.get(a, load=True)
    c_entity = self.client.get(c, load=True)
    a_profession = str(a_entity[self.client.get(c, load=True)].label)
    filtered_b_pool = np.array([b for b, p in self.b_pool if p != a_profession])

    b_emb = np.stack([self.kge.embed_entity(x) for x in filtered_b_pool])
    c_emb = self.kge.embed_predicate(c)

    a_proj = a_emb - (c_emb * (np.dot(a_emb, c_emb) / np.dot(c_emb, c_emb)))
    b_proj = b_emb - (c_emb * (np.dot(b_emb, c_emb) / np.dot(c_emb, c_emb)).reshape(-1, 1))
    
    sim = cosine_similarity(a_proj.reshape(1, -1), b_proj).reshape(-1)
    top_k = np.argsort(sim)[::-1][1:(k + 1)]
    return filtered_b_pool[top_k], sim[top_k]
