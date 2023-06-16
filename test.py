import numpy as np
import pickle
import argparse

from antonomasia.embeddings import KGE
from antonomasia.generation import AntonomasiaGenerator
from antonomasia.verbalizer import Verbalizer

from multiprocessing import Pool

import csv
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

from wikidata.client import Client
from multiprocessing import Pool

client = Client()

def get_profession(row):
    e = client.get(row[0].split("/")[-1], load=True)
    p = client.get("P106", load=True)
    
    professions = e.getlist(p)
    professions_label = []
    for p in professions:
        try:
            professions_label.append(str(p.label))
        except:
            pass
    return professions_label
  
with open('original_pool.csv', 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    #pool_of_b = [row[0].split("/")[-1] for row in csv_reader]
    
    with open("pool_of_b.csv", "w") as newout:
        csv_writer = csv.writer(newout)
        rows = list(csv_reader)
        
        professions = process_map(get_profession, rows, max_workers=50)

        for row, profession in zip(rows, professions):
            if profession == []:
                print(row)
            csv_writer.writerow(row + ["_".join(profession)])


#kge = KGE("transe_wikidata5m.pkl")
#generator = AntonomasiaGenerator(kge, pool_of_b)
#
#verb = Verbalizer(kge)
#bs, conf = generator.project_topk("Q76", "P106", 10)
#sentence = verb.generate_sentence("Q76", bs[0], "P106")
#print(sentence)


#parser = argparse.ArgumentParser()
#parser.add_argument("-p", "--path", required=True)



# def load_model(model_path: str):
#     with open("transe_wikidata5m.pkl", "rb") as fin:
#         model = pickle.load(fin)
#         entity2id = model.graph.entity2id
#         relation2id = model.graph.relation2id
#         entity_embeddings = model.solver.entity_embeddings
#         relation_embeddings = model.solver.relation_embeddings
#     return model, entity2id, relation2id, entity_embeddings, relation_embeddings


# model, entity2id, relation2id, entity_embeddings, relation_embeddings = load_model("transe_wikidata5m.pkl")
# id2entity = { v:k for k, v in entity2id.items() }

# get_entity_embedding = lambda x: entity_embeddings[entity2id[x]]
# get_rel_embeddings = lambda x: relation_embeddings[relation2id[x]]

# def transh_translation_sample(a, b, c, k: int = 10):
#     target = a - c
#     sim = cosine_similarity(target.reshape(1, -1), b).reshape(-1)
#     top_k = np.argsort(sim)[::-1][:k]
#     return top_k, sim[top_k]

# def projection_sample(a, b, c, k: int = 10):
#     a_proj = a - (c * (np.dot(a, c) / np.dot(c, c)))
#     b_proj = b - (c * (np.dot(b, c) / np.dot(c, c)).reshape(-1, 1))
#     sim = cosine_similarity(a_proj.reshape(1, -1), b_proj).reshape(-1)
#     top_k = np.argsort(sim)[::-1][:k]
#     return top_k, sim[top_k]

# b_pool = load_b_pool("pool_of_b.txt")

# A_label = "Q76"
# A = get_entity_embedding(A_label)

# B_labels = b_pool
# B = np.stack([get_entity_embedding(b) for b in B_labels])

# C_label = "P106"
# C = get_rel_embeddings(C_label)

# top_k, sim_top_k = projection_sample(A, B, C, 2)

# for t, s in zip(top_k, sim_top_k):
#     print(f"{A_label} is the {B_labels[t]} of (property {C_label} defines the context)) - Confidence: {s}")



# #print(np.array(b_pool)[top_k], sim_top_k)
