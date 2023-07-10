from itertools import product
from more_itertools import flatten
import subprocess

set_of_a = [
  "Q937", # Einstein
  "Q5284", # Bill gates
  "Q7245", # Mark Twain
  "Q9960", # Ronals Raegan
  "Q567", # Angela Merkel
  "Q8023", # Nelson Mandela
]

method = {
  "kge": {
    "-i": ["data/transe_wikidata5m.pkl",],
    "-p": ["translate", "project"],
  },
  "we": {
    "-m": ["word2vec", "glove"],
    "-p": ["translate", "project"],
  },
  "meta": {
    "-kge": ["data/transe_wikidata5m.pkl",],
    "-we": ["word2vec", "glove"],
    "-c": ["concatenate", "average"],
    "-p": ["translate", "project"],
  }
}

for a in set_of_a:
  for d in ["cosine", "euclidean"]:
    cmd = f"python antonomasia.py -b data/pool_of_b.csv -a {a} --distance {d} "
    for m, params in method.items():
      method_cmd = f"{cmd} {m}"
      combs = product(*params.values())
      for comb in combs:
        filename = f"{a}_{m}_{d}_" + "_".join(comb)
        filename = filename.replace("/", "_")
        filename = filename.replace(".", "")
        filename += ".txt"
        comb = " ".join(flatten(zip(params.keys(), comb)))
        
        final_cmd = f"{method_cmd} {comb} > output/{filename}"
        print(final_cmd)
        subprocess.call(final_cmd, shell=True)
