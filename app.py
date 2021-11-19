from flask import Flask, render_template, Response, request
from cyk_sentences import *
#Initialize the Flask app
app = Flask(__name__)

def get_productions():
    f = open("cyk_grammar.txt", 'r')
    grammar = f.readlines()
    a = []
    append = False
    print(grammar)
    for i in grammar:
        if i == 'PRODUCTIONS:\n':
            append = True
        if append == True:
            a.append(i)
    append = False
    f.close()
    return ''.join(a)
@app.route('/')
def index():
    grammar = get_productions()
    return render_template('index.html', grammar = grammar, result = '')

@app.route('/cyk', methods = ['GET', 'POST'])
def cyk():
    grammar = get_productions()
    try:
        sentences = request.values.get('sentences')
        # grammar = request.values.get('grammar')
        terminals = getTerminals(GRAMMARPATH)
        variables = getVariables(GRAMMARPATH)
        productions = getProduction(GRAMMARPATH)
        goodResult = CYKAlgorithm(sentences, productions, variables, terminals)
        # badResult = CYKAlgorithm(INCORRECTTESTSTRING, productions, variables, terminals)
        return render_template('index.html', grammar = grammar, result = goodResult)
    except:
        return render_template('index.html', grammar = grammar, result = 'Cant analysis')

if __name__ == "__main__":
    app.run(debug=True)