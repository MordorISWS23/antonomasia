from antonomasia.embeddings import KGE
from wikidata.client import Client

from antonomasia.utils import Sample

class Verbalizer(object):
  def __init__(self):
    self.client = Client()

  def generate_sentence(self, a: Sample, b: Sample, c: str):
    a_entity = self.client.get(a.wikidata_iri, load=True)
    c_entity = self.client.get(c, load=True)
    wikicommons_category = self.client.get("P373", load=True)
    c_label = a_entity[c_entity][wikicommons_category].lower()

    is_dead_prop = self.client.get("P570", load=True)

    verb = "was" if is_dead_prop in a_entity else "is"

    return f"{a.label} {verb} the {b.label} of {c_label}"