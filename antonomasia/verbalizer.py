from antonomasia.embeddings import KGE
from wikidata.client import Client

from antonomasia.utils import Sample
from wikidata.datavalue import DatavalueError


class Verbalizer(object):
    def __init__(self):
        """
    Initialize verbalizer
    """
        self.client = Client()

    def generate_sentence(self, a: Sample, b: Sample, c: str) -> str:
        """
    Generate a sentence starting from sample A, B and c context.

    Args:
        a (Sample): Entity A
        b (Sample): Entity B
        c (str): Context C

    Returns:
        str: Generated sentence. Take into account if A is dead.
    """
        a_entity = self.client.get(a.wikidata_iri, load=True)
        c_entity = self.client.get(c, load=True)
        wikicommons_category = self.client.get("P373", load=True)
        try:
            c_label = a_entity[c_entity][wikicommons_category].lower()
        except KeyError:
            prof = a_entity[c_entity]
            prof_label = prof.label
            c_label = f"{str(prof_label).lower()}s"
        # catch exeption resutling from different calendar model
        try:
            is_dead_prop = self.client.get("P570", load=True)
            verb = "was" if is_dead_prop in a_entity else "is"
        except DatavalueError:
            verb = "was"
        return f"{a.label} {verb} the {b.label} of {c_label}."
