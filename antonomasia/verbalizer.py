from antonomasia.embeddings import KGE
from wikidata.client import Client

vossians = [["Berlusconi", "Jesus Christ", "Politics"],
            ["Taylor Swift", "Mozart", "Modern Pop Music"],
            ["Greta Thunberg", "Rosa Parks", "climate change"],
            ["J.K. Rowling", "Shakespeare", "fantasy literature"]]

A_ids = ["Q11860", "Q26876", "Q56434717", "Q34660"]
  # id for property of being dead already


class Verbalizer(object):
  def __init__(self, kge: KGE):
    self.client = Client()  # doctest: +SKIP
    self.kge = kge

  def generate_sentence(self, A_id: str, B_id: str, C_id: str):
    A_entity = self.client.get(A_id, load=True)
    A_label = A_entity.label
    A_props = A_entity.lists()

    try:
      B_entity = self.client.get(B_id, load=True)
      B_label = B_entity.label
    except:
      B_label = B_id

    C_entity = self.client.get(C_id, load=True)
    wikicommons_category = self.client.get("P373", load=True)
    C_label = A_entity[C_entity][wikicommons_category].lower()

    is_dead_prop = self.client.get("P570", load=True)

    verb = "was" if is_dead_prop in A_entity else "is"

    return f"{A_label} {verb} the {B_label} of {C_label}"



# def alive_or_dead(vossians, ent_props):
#     for item, elem in zip(vossians, ent_props):
#         is_alive = True
#         for prop in elem:
#             if str(prop).find(prop_death) != -1:
#                 item.append("dead")
#                 is_alive = False
#                 break
#         if is_alive:
#             item.append("alive")
#     return vossians


# def generate_sentence(ids, prop_death, vossians):
#     entities = get_entities(A_ids)
#     ent_props = get_ent_props(entities)
#     vossians_new = alive_or_dead(vossians, ent_props)
#     verb = ""
#     for elem in vossians_new:
#         if elem[3] == "alive":
#             verb = "is"
#         if elem[3] == "dead":
#             verb = "was"
#         template = f"{elem[0]} {verb} the {elem[1]} of {elem[2]}"
#         print(template)


# generate_sentence(A_ids, prop_death, vossians)

