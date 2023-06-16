import numpy as np
import pickle
import argparse
import csv

from antonomasia.embeddings import KGE, WordEmbedding
from antonomasia.generation import AntonomasiaGenerator
from antonomasia.verbalizer import Verbalizer

argparser = argparse.ArgumentParser()
argparser.add_argument("--b_pool", required=False, default="pool_of_b.csv")
argparser.add_argument("-a", required=True)
argparser.add_argument("--emb", required=True)
argparser.add_argument("--num", required=False, default=10)
argparser.add_argument("--funny-first", action="store_true", default=False)


if __name__ == "__main__":
    args = argparser.parse_args()


    if args.emb == "word2vec":
        with open(args.b_pool, "r") as csvfile:
            csv_reader = csv.reader(csvfile)
            pool_of_b = [(row[1], row[-1].split("_")) for row in csv_reader]

        emb = WordEmbedding("word2vec")
    else:
        with open(args.b_pool, "r") as csvfile:
            csv_reader = csv.reader(csvfile)
            pool_of_b = [(row[0].split("/")[-1], row[-1].split("_")) for row in csv_reader]
        
        emb = KGE(args.emb)
    
    generator = AntonomasiaGenerator(emb, pool_of_b)

    verb = Verbalizer(emb)
    profession_pred = "P106"

    try:
        top_k = generator.project_topk(args.a, profession_pred, args.num, magnitude_sort=args.funny_first)
        for b, conf in zip(*top_k):
            sentence = verb.generate_sentence(args.a, b, profession_pred)
            print(f"Confidence: {conf} - {sentence}")        
    except:
        print(f"ERROR: The entity {args.a} is not available in the embeddings {args.emb}")
