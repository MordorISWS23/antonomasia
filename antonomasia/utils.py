from collections import namedtuple
from wikidata.client import Client

Sample = namedtuple("Sample", ["wikidata_iri", "label", "classes"])
client = Client()

def get_sample(wikidata_iri: str, class_iri: str) -> Sample:
  """
  Retrieve a sample from its Wikidata IRI only

  Args:
      wikidata_iri (str): IRI of the Wikidata entity.
      class_iri (str): IRI of the classification property.deleter

  Returns:
      Sample: The built sample.
  """
  a_entity = client.get(wikidata_iri, load=True)
  c_entity = client.get(class_iri, load=True)
  classes = set([str(e.label) for e in a_entity.getlist(c_entity)])
  return Sample(wikidata_iri, str(a_entity.label), classes)
    
