from cyk_parser import *
from nltk import Tree
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget
import re
import os
from PIL import Image



class SentencesParser:
    def __init__(self) -> None:
        self.algorithm_name = 'CYK'
        self.grammar_name = 'Default'
        self.grammar = open('cyk_grammar.txt', 'r').read()
        pass

    def parser(self, sentence):
        
        CYK = Parser('cyk_grammar.txt', sentence = sentence)
        CYK.parse()
        return CYK.print_tree()
    
    def to_image(self, str_trees):
        for i in range(len(str_trees)):
            str_tree = str_trees[i]
            str_tree = re.sub('\[', '(', str(str_tree))
            
            str_tree = re.sub('\]', ')', str_tree)
            cf = CanvasFrame()
            t = Tree.fromstring(str_tree)
            tc = TreeWidget(cf.canvas(),t)
            cf.add_widget(tc,10,10) # (10,10) offsets
            cf.print_to_file('tree.ps')
            cf.destroy()
            psimage=Image.open('tree.ps')
            psimage.save('static/img/tree_'+str(i)+'.png')
