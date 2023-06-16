# antonomasia

First download a KGE embedding in the same directory of the code from https://graphvite.io/docs/latest/pretrained_model.html#id1 (download TransE for now).

Install the requirements with 
`pip install -r requirements.txt`

Generate an antonomasia with `python antonomasia.py -a Q22686 --emb transe_wikidata5m.pkl`. 
Replace `Q22686` with the wikidata entity and `transe_wikidata5m.pkl` with the actual embedding.
You can add the `--funny-first` parameter to enable magnitude sort.