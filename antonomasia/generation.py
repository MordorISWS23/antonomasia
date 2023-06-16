from typing import Tuple
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from wikidata.client import Client

from antonomasia.embeddings import KGE

class AntonomasiaGenerator(object):

  def __init__(self, kge: KGE, b_pool):
    self.kge = kge
    self.b_pool = [b for b in b_pool if b[0] in self.kge]
    self.client = Client()

  def project_topk(self, a: str, c: str, k: int = 10, magnitude_sort: bool = False) -> Tuple[np.array, np.array]:
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
    a_professions = set([str(e.label) for e in a_entity.getlist(c_entity)])
    filtered_b_pool = np.array([b for b, p in self.b_pool if len(a_professions.intersection(p)) == 0])

    b_emb = np.stack([self.kge.embed_entity(x) for x in filtered_b_pool])
    c_emb = self.kge.embed_predicate(c)

    a_proj = a_emb - (c_emb * (np.dot(a_emb, c_emb) / np.dot(c_emb, c_emb)))
    b_proj = b_emb - (c_emb * (np.dot(b_emb, c_emb) / np.dot(c_emb, c_emb)).reshape(-1, 1))
    
    cos_sim = cosine_similarity(a_proj.reshape(1, -1), b_proj).reshape(-1)
    
    top_k = np.argsort(cos_sim)[::-1][1:(k + 1)]
    
    #if magnitude_sort:
    #b_proj[top_k]

    return filtered_b_pool[top_k], cos_sim[top_k]
