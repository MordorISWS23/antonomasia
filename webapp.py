import streamlit as st
import csv
from antonomasia.embeddings import KGE, WordEmbedding, MetaEmbedding
from antonomasia.generation import AntonomasiaGenerator
from antonomasia.verbalizer import Verbalizer
from antonomasia.utils import Sample
from SPARQLWrapper import SPARQLWrapper, JSON
from streamlit_extras.add_vertical_space import add_vertical_space
from style import write_footer, hide_menu_style, custom_style

st.set_page_config(page_title="Vossian Generarion", page_icon="🦜",
                   layout="wide", initial_sidebar_state="collapsed", menu_items=None)
# add custom style
st.markdown(custom_style, unsafe_allow_html=True)
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.title("Vossian Antonomasias")
add_vertical_space(1)

st.subheader("Do you want to get creative suggestions for Vossian Antonomasias?")

add_vertical_space(2)

with st.expander("What are Vossian Antonomasias?"):
    st.markdown('<p style="font-size: 16px;">Vossian antonomasias refer to someone by a special '
                'characteristic instead of their name.  \
                 <br>   For example, calling Bill Gates "the Henry Ford of the computer age" '
                'highlights his influence as entrepeneur and his effect on the development of technology. \
                 <br> It is a way to describe someone by an important quality they possess. </p>',
                unsafe_allow_html=True)
add_vertical_space(2)
st.markdown('<p style="font-size: 20px;"><b>This is how it works:</b></p>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 18px;"><b>1. Select an entity you want to describe '
            'with a Vossian Antonomasia.</b></p>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 18px;"><b>2. Select the number of sentences to be generated.</b></p>',
             unsafe_allow_html=True)
st.markdown('<p style="font-size: 18px;"><b>3. Select the method and other parameters for the generation.</b></p>',
             unsafe_allow_html=True)
sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
sparql.setReturnFormat(JSON)
QUERY = """
SELECT ?pic ?description
WHERE {
  wd:%s wdt:P18 ?pic ;
        schema:description ?description .
  FILTER(LANG(?description) = "en")
}
"""
write_footer()

with open("data/pool_of_b.csv", "r", encoding="utf-8") as csvfile:
  csv_reader = csv.reader(csvfile)
  pool_of_b = [Sample(row[0].split("/")[-1], row[1], row[-1].split("_")) for row in csv_reader]

@st.cache_resource
def load_models():
  kge = KGE("data/transe_wikidata5m.pkl")
  word2vec = WordEmbedding("word2vec")
  glove = WordEmbedding("glove")
  
  return {
    "kge": kge, "word2vec": word2vec, "glove": glove,
    "meta_w2v_conc": MetaEmbedding(word2vec, kge, method="concatenate"),
    "meta_w2v_average": MetaEmbedding(word2vec, kge, method="average"),
    "meta_glove_conc": MetaEmbedding(glove, kge, method="concatenate"),
    "meta_glove_average": MetaEmbedding(glove, kge, method="average"),
  }

models = load_models()
method_model_map = {
  "kge": "Knowledge Graph Embeddings",
  "word2vec": "word2vec",
  "glove": "GloVe",
  "meta_w2v_conc": "Meta embedding: KGE and word2vec concatenation",
  "meta_w2v_average": "Meta embedding: KGE and word2vec average",
  "meta_glove_conc": "Meta embedding: KGE and GloVe concatenation",
  "meta_glove_average": "Meta embedding: KGE and GloVe average",
}

tab_gen, tab_config = st.tabs(["Generation", "Configuration"])

with tab_config:
  method = st.selectbox("Select the method", list(method_model_map.keys()), format_func=method_model_map.get)
  projection_method = st.radio("Embedding search method", ("translate", "project"))
  distance = st.radio("Distance function", ("cosine", "euclidean"))
  creative_sort = st.checkbox("Most creative first", True)

with tab_gen:
  select_a = st.selectbox("Select the A entity", pool_of_b, format_func=lambda s: s.label, index=2162)
  k = st.number_input("Number of sentences to generate", min_value=1, max_value=10, value=1, step=1)

  generator = AntonomasiaGenerator(models[method], pool_of_b)
  verb = Verbalizer()
  profession_pred = "P106"

  a_emb, b_emb, b_ids, c_emb = generator.embed_a_b_c(select_a, profession_pred)

  if projection_method == "translate":
    a, b = generator.translate_embeddings(a_emb, b_emb, c_emb)
  else:
    a, b = generator.project_embeddings(a_emb, b_emb, c_emb)

  top_k, sim = generator.top_k(a, b, k=k, similarity_fn=distance, magnitude_sort=creative_sort)

  pbar = st.progress(0, text="Generating the sentences...")
  for i, (idx, conf) in enumerate(zip(top_k, sim)):
    b = b_ids[idx]
    sentence = verb.generate_sentence(select_a, b, profession_pred)

    A = sentence.split(" is")[0] if "is the" in sentence else sentence.split(" was")[0]
    A_id = next(filter(lambda x: x.label == A, pool_of_b)).wikidata_iri

    B = sentence.split("the ")[-1].split(" of")[0]
    B_id = next(filter(lambda x: x.label == B, pool_of_b)).wikidata_iri

    with st.expander(f"[{A}](https://www.wikidata.org/wiki/{A_id}){sentence.split(A)[-1].split(B)[0]}[{B}](https://www.wikidata.org/wiki/{B_id}){sentence.split(B)[-1]}"):
      
      left, right = st.columns(2)
      
      with left:
        sparql.setQuery(QUERY % A_id)
        ret = sparql.queryAndConvert()
        pic = ret["results"]["bindings"][0]["pic"]["value"]
        desc = ret["results"]["bindings"][0]["description"]["value"]
        st.image(pic, caption=desc)

      with right:
        sparql.setQuery(QUERY % B_id)
        ret = sparql.queryAndConvert()
        pic = ret["results"]["bindings"][0]["pic"]["value"]
        desc = ret["results"]["bindings"][0]["description"]["value"]
        st.image(pic, caption=desc)
      
      if 0 <= conf <= 1:
        st.progress(float(conf), text=f"Confidence {conf:0.2f}")

    pbar.progress((i + 1) / len(top_k), text="Generating the sentences...")
