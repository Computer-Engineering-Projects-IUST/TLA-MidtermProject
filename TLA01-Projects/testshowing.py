# import sys
# import json
# from visualize import visualize
# from FA.dfa import VisualDFA
# from FA.nfa import VisualNFA
# from utils import read_fa, create_standard_fa
# from automata.fa.nfa import NFA

# if __name__ == '__main__':
#     """ the main function for visualize the FA"""
#     args = sys.argv[1:]
#     #json_path = args[0]   # the relative path of the json file containing the dfa or nfa in the desired format
#     json_path = "samples/phase1-sample/in/test.json"#args[0]  
#     try:
#             read_fa(json_path)
#             fa = create_standard_fa(1)
#             # nfa = VisualNFA(fa)
#             # nfa.show_diagram()
#             # nfa = VisualNFA(fa)
#     except Exception as ex:
#         raise Exception("The input file is neither DFA nor NFA\nCheck whether you "
#                             "mentioned a correct file or its in the correct standard format")\
#             from ex

# DFA_fa=fa

# DFA_fa["states"]={'q0','q1-q2'}
# DFA_fa["transitions"]={
#       "q0": {
#         "a": {'q1-q2'}
#       },
#       "q1-q2": {
#         "b": {'q0'}
#       }
#     }

# DFA_fa["final_states"]= {'q1-q2'}
# nfa = VisualNFA(DFA_fa)
# nfa.show_diagram()


# # visualize(fa)
# print ("done test")
s={'q3','q1','q2'}
s=sorted(s)
s2='-'.join(s)
print(s2)