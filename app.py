from os import name
from re import L
import os
from flask import Flask, render_template, request
from nltk import tree
from config import *
from grammar import EarleyParser, NltkGrammar, CYKParser
import asyncio
import time
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    default_value = ""
    sentence = request.form.get('sentence_input', default_value)
    alg = request.form.get('alg', "CYK")
    nltkGrammar = NltkGrammar('grammar.cfg')
    img_paths = []
    try:
        if alg == "CYK":
            parser = CYKParser(nltkGrammar.read_grammar())
        elif alg == "Earley":
            parser = EarleyParser(nltkGrammar.read_grammar())
        trees = parser.parse(sentence)
        json_trees = parser.get_tree_json(trees)
        img_paths = parser.to_image(json_trees)
    except:
        img_paths = []
    return render_template(index_template, img_paths = img_paths, sentence = sentence, alg = alg)
    
@app.route("/grammar")
def change_grammar():
    nltkGrammar = NltkGrammar('grammar.cfg')
    list_prod_left, list_prod_right = nltkGrammar.get_productions()
    return render_template(change_grammar_template, list_prod_left = list_prod_left, 
                                            list_prod_right = list_prod_right, len = len(list_prod_left))


if __name__ == "__main__":
    app.run()
