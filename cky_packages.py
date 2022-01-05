#!/usr/bin/env python
# coding: utf-8



import nltk
from nltk.tree import Tree

grammar = nltk.data.load("grammars/large_grammars/atis.cfg")
cng_grammar = grammar.chomsky_normal_form()


# # ### Test Sentences

# # In[4]:


# s = nltk.data.load("grammars/large_grammars/atis_sentences.txt")
# test_sent = nltk.parse.util.extract_test_sentences(s)

#%%
def find_children(nt,trees):
    child = []
    for tree in trees:
        if tree.label() == nt:
            child.append(tree)
    return child


# In[25]:


def find_lhs(non_term_list1,non_term_list2,tree_up,tree_down,flag):
    
    non_term_list = []
    trees = []
    for nt in non_term_list1: # for each non terminal in first cell
        prod = cng_grammar.productions(rhs = nt)

        for pr in prod:
        
            if pr.rhs()[1] in non_term_list2:
                non_term_list.append(pr.lhs())
                if flag == True:
                    left = find_children(nt,tree_up)
                    right = find_children(pr.rhs()[1],tree_down)
                    
                    for l_tree in left:
                        for r_tree in right:
                            x = Tree(pr.lhs(),[l_tree,r_tree])
                            if x not in trees:                        
                                trees.append(x)

    return non_term_list ,trees

    


# In[29]:


def cky(grammar,sent,flag):
    
    
    n = len(sent)

    try:
        grammar.check_coverage(sent)
    except ValueError:
        print("Grammar does not cover all the tokens")
        return [],[]
    
  

    chart = [[ set() for i in range(n+1)] for i in range(n+1)]
    nodes_back = [[[] for i in range(n+1)] for i in range(n+1)]

  # diagonals 
    for i in range(n):
    
        for prod in grammar.productions(rhs = sent[i]):
            
        
            chart[i][i+1].add(prod.lhs())
            if flag == True:
                nodes_back[i][i+1].append(Tree(prod.lhs(),[prod.rhs()]))
        
    



    for width in range(2,n+1):
        for i in range(0,n-width+1):
            for j in range(1,width):
                
                prods,trees = find_lhs(chart[i][i+j],chart[i+j][i+width],nodes_back[i][i+j],nodes_back[i+j][i+width],flag)

                for pr in prods:
                    chart[i][i+width].add(pr)
                if flag == True :    
                    for tree in trees:
                        nodes_back[i][i+width].append(tree)

    return chart,nodes_back


# In[23]:


def get_trees(trees,start):
    count = 0
    total_trees = []
    for tree in trees:
        if tree.label() == start:
            count += 1
            total_trees.append(tree)
            # tree.draw()
    return total_trees

# In[31]:


       
def cky_wrapper(sent_list, grammar, flag):
    cng_grammar = grammar.chomsky_normal_form()
    for sent in sent_list :
        print(sent)
        chart,nodes_back = cky(cng_grammar,sent[0],flag)
        if len(chart) == 0:
            continue
        start = cng_grammar.start()
        n = len(sent[0])
        if start in chart[0][n]:
            return get_trees(nodes_back[0][n], start)
        else:
            return []
    

# 
# test = []
# test.append(test_sent[89])
# print(test_sent[89])
# print("parsing the sentence : ")
# for tree in cky_wrapper(test,grammar, True):
#     print(test_sent[89])