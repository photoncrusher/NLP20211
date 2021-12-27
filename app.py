from flask import Flask, render_template, Response, request
from sentences_parser import *

app = Flask(__name__)
sentencesParser = SentencesParser()

@app.route('/')
def index():
    algorithm_name = sentencesParser.algorithm_name
    grammar_name = sentencesParser.grammar_name
    return render_template('index.html', algorithm_name = algorithm_name, grammar_name = grammar_name)

@app.route('/start_parser', methods = ['POST'])
def start_parser():
    sentence = request.form['sentences']
    str_trees = sentencesParser.parser(sentence)
    sentencesParser.to_image(str_trees)
    idx = len(str_trees)
    filename = []
    for i in range(0, idx):
        fn = 'img/tree_'+str(i)+'.png'
        filename.append(fn)
    return render_template('start_parser.html', sentence = sentence, filename=filename)

@app.route('/edit_grammar')
def edit_grammar():
    # sentence = request.form['sentences']
    grammar = sentencesParser.grammar
    return render_template('edit_grammar.html', grammar = grammar)

@app.route('/edit_algo')
def edit_algo():
    # sentence = request.form['sentences']
    return render_template('edit_algo.html')

# @app.route('/cyk', methods = ['GET', 'POST'])
# def cyk():
#     grammar = get_productions()
#     try:
#         sentences = request.values.get('sentences')
#         # grammar = request.values.get('grammar')
#         terminals = getTerminals(GRAMMARPATH)
#         variables = getVariables(GRAMMARPATH)
#         productions = getProduction(GRAMMARPATH)
#         goodResult = CYKAlgorithm(sentences, productions, variables, terminals)
#         # badResult = CYKAlgorithm(INCORRECTTESTSTRING, productions, variables, terminals)
#         return render_template('index.html', grammar = grammar, result = goodResult)
#     except:
#         return render_template('index.html', grammar = grammar, result = 'Cant analysis')

if __name__ == "__main__":
    app.run(debug=True)