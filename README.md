# (Semi)Automatic Vossian Antonomasias generation

The (Semi)Automatic Vossian Antonomasia generation method harnesses the power of Knowledge Graph Embeddings (KGE) trained on Wikidata to generate Vossian Antonomasias. Vossian Antonomasia (VA) is a figure of speech that refers to the substitution of a proper name with a common noun or vice versa. This technique can be used to create memorable and impactful expressions, making it popular in literature, rhetoric, and creative writing.

## How it Works
A VA is generally of the type 

```
A is (or was) the B of C
```

where `A` is the target entity that is going to be substituted by a different, popular name. In our setting, `A` is an *arbitrary* Wikidata individual and `B` is a *popular* Wikidata individual. We classify individuals as popular if they have a wide coverage of Wikipedia articles among different languages.
`C` is the context that allows a VA to convey a similarity relation in a creative way. In our case, it is always equal to the profession of an entity.
It should hold that `A` and `B` can be classified as similar individual. However, with `C` the profession of `A` it should hold that `C` **is not** the profession of `B`.

For intance, in the VA *Floyd Mayweather is the Michael Jordan of boxing.* [1, 2], we have that `A = Floyd Mayweather`, `B = Micheal Jordan` and `C = boxing`.

## Installation

Clone the repository locally with

```
git clone git@github.com:MordorISWS23/antonomasia.git
```

and install the python requirements with

```
pip install -r requirements.txt
```


In order to use KGE, the pretrained models on Wikidata needs to be downloaded. We rely on the model shared by [GraphVite](https://graphvite.io/) 
available via the following [link](https://udemontreal-my.sharepoint.com/:u:/g/personal/zhaocheng_zhu_umontreal_ca/EX4c1Ud8M61KlDUn2U_yz_sBP_bXNuFnudfhRnYzWUFA2A?download=1).
Currently, only the TransE model is supported. Download the model locally in order to use them.
On Linux and MacOS, this can be done using

```
wget https://udemontreal-my.sharepoint.com/:u:/g/personal/zhaocheng_zhu_umontreal_ca/EX4c1Ud8M61KlDUn2U_yz_sBP_bXNuFnudfhRnYzWUFA2A?download=1 -O transe.pkl
```

## Usage

The script `antonomasia.py` can be used to generate VA.

```
usage: antonomasia.py [-h] -b B_POOL -a A [--num NUM] [--confidence] [--funny-first] {kge,we,meta} ...

Generate a Vossian Antonomasia

positional arguments:
  {kge,we,meta}         Method specific parameters
    kge                 Use Knowledge Graph Embeddings
    we                  Use Word Embeddings
    meta                Use Meta Embeddings

options:
  -h, --help            show this help message and exit
  -b B_POOL, --b_pool B_POOL
                        Path to the file containing the csv for the set of B entities.
  -a A                  A entity expressed as Wikidata ID - e.g. Q76.
  --num NUM             Number of sentences to generate.
  --confidence          Add a confidence score to each generated sentence.
```

### KGE
```
usage: antonomasia.py kge [-h] -i INPUT -p {translate,project}

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to the KGE weigths.
  -p {translate,project}, --projection {translate,project}
                        Projection method to use.
```

### Word Embedding
```
usage: antonomasia.py we [-h] -m {word2vec,glove} -p {translate,project}

options:
  -h, --help            show this help message and exit
  -m {word2vec,glove}, --model {word2vec,glove}
                        Word embedding method to use.
  -p {translate,project}, --projection {translate,project}
                        Projection method to use.
```

### Meta-embedding
```
usage: antonomasia.py meta [-h] -kge KGE -we {word2vec,glove} -p {translate,project} -c {concatenate,average}

options:
  -h, --help            show this help message and exit
  -kge KGE              Path to the KGE weigths.
  -we {word2vec,glove}  Word embedding method to use.
  -p {translate,project}, --projection {translate,project}
                        Projection method to use.
  -c {concatenate,average}, --combination {concatenate,average}
                        Combination method to use.
```

## Examples

TBD

## References

[1] https://vossanto.weltliteratur.net/emnlp-ijcnlp2019/vossantos.html

[2] https://www.nytimes.com/2007/05/03/sports/othersports/03boxing.html