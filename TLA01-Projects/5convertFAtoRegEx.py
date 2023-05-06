import sys
import re
import json
from visualize import visualize
from FA.dfa import VisualDFA
from FA.nfa import VisualNFA
from utils import read_fa, create_standard_fa
from automata.fa.nfa import NFA

if __name__ == '__main__':
    """ the main function for visualize the FA"""
    args = sys.argv[1:]
    #json_path = args[0]   # the relative path of the json file containing the dfa or nfa in the desired format
    jsonpath = "samples/phase5-sample/in/FA.json"#args[0] 
    isDFA=True 

    try:
            read_fa(jsonpath)
            FA = create_standard_fa()
            dfa = VisualDFA(FA)
            dfa.show_diagram()
    except:
            try:
                isDFA=False
                read_fa(jsonpath)
                fa = create_standard_fa(1)
                nfa = VisualNFA(fa)
                nfa.show_diagram()
            except Exception as ex:
                raise Exception("The input file is neither DFA nor NFA\nCheck whether you "
                                "mentioned a correct file or its in the correct standard format")\
                    from ex


fa=nfa
fa.transitions


# def dfa_to_regex():
    # Step 1: Assign variables to each state
variables = {s: f'x_{i}' for i, s in enumerate(fa.states)}
X = variables[fa.initial_state]

# Step 2: Write equations for each state
equations = []
for state in fa.states:
    R = ''.join(f'{variables[list(next_state)[0]]}|' for symbol, next_state in fa.transitions[state].items())
    R = f'({R[:-1]})'  # Remove the last | symbol
    L = '1' if state in fa.final_states else '0'
    equations.append(f'{variables[state]}={R}{variables[state]}+{L}')

# Step 3: Solve the set of equations
regex = ''
while len(equations) > 0:
    # Find an equation with only one variable
    for i, eqn in enumerate(equations):
        if len(re.findall(f'\\b{variables[fa.initial_state]}\\b', eqn)) == 0 and len(re.findall(f'\\b{variables[list(fa.final_states)[0]]}\\b', eqn)) == 0 and len(re.findall('[a-z0-9()]+', eqn)) == 1:
            regex += eqn.split('=')[1]
            var_to_remove = variables[fa.states[i]]
            break
    else:
        raise ValueError("Can't solve equations")

    # Substitute variable in other equations
    equations = [re.sub(f'\\b{var_to_remove}\\b', f'({regex})', eqn) for eqn in equations]
    equations.pop(i)

    # return regex