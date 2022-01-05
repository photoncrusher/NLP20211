from nltk import grammar
import nltk
from nltk.grammar import CFG
from nltk import EarleyChartParser
from nltk.util import pr
from cky_packages import cky, cky_wrapper
import json
from nltk.tree import Tree
import sys
import re
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget
from PIL import Image
import os
def tree2dict(tree):
    return {str(tree.label()): [tree2dict(t)  if isinstance(t, Tree) else t
                        for t in tree]}


class NltkGrammar:
    def __init__(self, grammar_file) -> None:
        self.grammar_file  = grammar_file
    
    def read_grammar(self):
        return nltk.data.load(self.grammar_file)
    
    def get_productions(self):
        list_prod_left = []
        list_prod_right = []
        productions = self.read_grammar().productions()
        for production in productions:
            list_prod_left.append(production.lhs())
            list_prod_right.append(production.rhs())
        return list_prod_left, list_prod_right

class Parser:
    def __init__(self, grammar) -> None:
        self.grammar = grammar 

    def parse(self):
        pass

    def get_tree_json(self, trees):
        json_trees = trees
        # json_trees = []
        # for tree in trees:
        #     # json_tree = str(tree)
        #     # print(str(tree))
        #     d = tree2dict(tree)
        #     json_tree = json.dumps(d)
        #     json_tree = str(json_tree)
        #     # json_tree = re.sub(' ', ':', json_tree)
        #     json_trees.append(json_tree)
        return json_trees
    
    def to_image(self, trees):
        for img_path in os.listdir('static/parse_img/'):
            os.unlink('static/parse_img/' + img_path)
            print(img_path)
        img_paths = []
        for i in range(len(trees)):
            cf = CanvasFrame()
            t = trees[i]
            tc = TreeWidget(cf.canvas(),t)
            tc['node_font'] = 'arial 14 bold'
            tc['leaf_font'] = 'arial 14'
            tc['node_color'] = '#005990'
            tc['leaf_color'] = '#3F8F57'
            tc['line_color'] = '#175252'
            cf.add_widget(tc,10,10) # (10,10) offsets
            cf.print_to_file('tree.ps')
            psimage=Image.open('tree.ps')
            psimage.save('static/parse_img/tree_'+str(i)+'.png')
            psimage.close()
            img_path = 'parse_img/tree_'+str(i)+'.png'
            img_paths.append(img_path)
        return img_paths

class EarleyParser(Parser):
    def __init__(self, grammar) -> None:
        super().__init__(grammar)

    def parse(self, sentences):
        earley = EarleyChartParser(grammar=self.grammar)
        return earley.parse_all(sentences.split(' '))

class CYKParser(Parser):
    def __init__(self, grammar) -> None:
        super().__init__(grammar)

    def parse(self, sentences):
        sentences = nltk.parse.util.extract_test_sentences(sentences)
        return cky_wrapper([sentences[0]], self.grammar, True)

# nltkGrammar = NltkGrammar('grammar.cfg')

# print(nltkGrammar.get_productions()[0])
# earleyParser = EarleyParser(nltkGrammar.read_grammar())
# for tree in earleyParser.parse("what are the costs ."):
#     print(tree)

# for tree in ckyParser.parse("what are the costs ."):
#     # print(str(tree.label))
#     d = tree2dict(tree)
#     json.dump(d, sys.stdout)
