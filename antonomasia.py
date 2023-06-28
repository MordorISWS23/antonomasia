import numpy as np
import pickle
import argparse
import csv

from antonomasia.embeddings import KGE, WordEmbedding, MetaEmbedding
from antonomasia.generation import AntonomasiaGenerator
from antonomasia.verbalizer import Verbalizer
from antonomasia.utils import Sample, get_sample

argparser = argparse.ArgumentParser(description="Generate a Vossian Antonomasia")
argparser.add_argument("-b", "--b_pool", required=True, help="Path to the file containing the csv for the set of B entities.")
argparser.add_argument("-a", required=True, help="A entity expressed as Wikidata ID - e.g. Q76.")
argparser.add_argument("--num", required=False, default=10, type=int, help="Number of sentences to generate.")
argparser.add_argument("--confidence", action="store_true", default=False, help="Add a confidence score to each generated sentence.")
argparser.add_argument("--funny-first", action="store_true", default=False)

subparsers = argparser.add_subparsers(dest="method", help="Method specific parameters")

subparsers_kge = subparsers.add_parser("kge", help="Use Knowledge Graph Embeddings")
subparsers_kge.add_argument("-i", "--input", required=True, help="Path to the KGE weigths.")
subparsers_kge.add_argument("-p", "--projection", required=True, help="Projection method to use.", choices=["translate", "project"])

subparsers_kge = subparsers.add_parser("we", help="Use Word Embeddings")
subparsers_kge.add_argument("-m", "--model", required=True, help="Word embedding method to use.", choices=["word2vec", "glove"])
subparsers_kge.add_argument("-p", "--projection", required=True, help="Projection method to use.", choices=["translate", "project"])

subparsers_kge = subparsers.add_parser("meta", help="Use Meta Embeddings")
subparsers_kge.add_argument("-kge", required=True, help="Path to the KGE weigths.")
subparsers_kge.add_argument("-we", required=True, help="Word embedding method to use.", choices=["word2vec", "glove"])
subparsers_kge.add_argument("-p", "--projection", required=True, help="Projection method to use.", choices=["translate", "project"])
subparsers_kge.add_argument("-c", "--combination", required=True, help="Combination method to use.", choices=["concatenate", "average"])

if __name__ == "__main__":
    args = argparser.parse_args()
    
    with open(args.b_pool, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        pool_of_b = [Sample(row[0].split("/")[-1], row[1], row[-1].split("_")) for row in csv_reader]

    if args.method == "kge":
        emb = KGE(args.input)
    elif args.method == "we":
        emb = WordEmbedding(args.model)
    elif args.method == "meta":
        kge = KGE(args.kge)
        we = WordEmbedding(args.we)
        emb = MetaEmbedding(we, kge, method=args.combination)

    generator = AntonomasiaGenerator(emb, pool_of_b)
    verb = Verbalizer()
    
    profession_pred = "P106"
    a_sample = get_sample(args.a, profession_pred)
    a_emb, b_emb, b_ids, c_emb = generator.embed_a_b_c(a_sample, profession_pred)

    if args.projection == "translate":
        a, b = generator.translate_embeddings(a_emb, b_emb, c_emb)
    elif args.projection == "project":
        a, b = generator.project_embeddings(a_emb, b_emb, c_emb)

    top_k, sim = generator.top_k(a, b, k=args.num, magnitude_sort=args.funny_first)

    for idx, conf in zip(top_k, sim):
        b = b_ids[idx]
        sentence = verb.generate_sentence(a_sample, b, profession_pred)
        if args.confidence:
            print(f"Confidence: {conf} - ", end="")
        print(f"{sentence}")