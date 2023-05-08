from typing import List, Dict
import json
import re
import sys
from visualize import visualize
from FA.dfa import VisualDFA
from FA.nfa import VisualNFA
from utils import read_fa, create_standard_fa

from automata.fa.nfa import NFA
class NewState:
    def __init__(self, state_ID: str):
        self.state_ID = state_ID
        self.transitions = { }
        self.Visit = False

class DFA:
    def __init__(self, ID: int, states: List[NewState], InputSymbols: List[str], InitialState: NewState, FinalStates: List[NewState]):
        self.ID = ID
        self.States = states
        self.InputSymbols = InputSymbols
        self.InitialState = InitialState
        self.FinalStates = FinalStates

def DFS_Visit_Recursive(Visited, dfa, n: NewState, dfs_visit: List[NewState]):
    n.Visit = True
    for i in range(len(InputSymbols)):
        if n.transitions[InputSymbols[i]].Visit == False:
            dfs_visit.append(n.transitions[dfa.InputSymbols[i]])
            DFS_Visit_Recursive(dfa, n.transitions[dfa.InputSymbols[i]], dfs_visit)

def SimplificationDFA(InitialState, ) -> DFA:
    dfs_visit = []
    dfs_visit.append(InitialState)

    # First we go through vertexes by DFS to define non-reachable states
    DFS_Visit_Recursive(dfa, InitialState, dfs_visit)
    dfa.States = dfs_visit

    new_final_state = []
    # Remove non-reachable states from DFA
    for i in range(len(dfa.FinalStates)):
        if dfa.FinalStates[i] in dfs_visit:
            new_final_state.append(dfa.FinalStates[i])
    dfa.FinalStates = new_final_state

    # Construct zero_equivalence by separating final and non-final states
    final = []
    nonfinal = []
    for i in range(len(dfa.States)):
        if dfa.States[i] in dfa.FinalStates:
            final.append(dfa.States[i])
        else:
            nonfinal.append(dfa.States[i])

    # Define list for k_equivalence to reach k+1_equivalence(next equivalence table)
    equal_state_k = []
    equal_state_k.append(final)
    equal_state_k.append(nonfinal)

    # Do this while loop till k+1_equivalence table is as same as k_equivalence
    while True:
        # Create states list as k+1_equivalence table   
        equal_state_k_next = []
        for i in range(len(equal_state_k)):
            # For states that were equal in k_equivalence table we check equivalency in k+1_equivalence table
            # Create a dictionary for separating states that are in the same list in k_equivalence table 
            product_equal_states = { }
            # For states that were equal in k_equivalence table do this for loop
            for j in range(len(equal_state_k[i])):
                x = ""
                # Check whether we have 2 input symbols 
                if len(dfa.InputSymbols) == 2:
                    # Check whether for each input symbol which equivalence list we reach + add first state of the previous list to x(string)
                    for k in range(len(equal_state_k)):
                        if equal_state_k[k].count(equal_state_k[i][j].transitions[dfa.InputSymbols[0]]) != 0:
                            x += equal_state_k[k][0].state_ID
                            break
                    for k in range(len(equal_state_k)):
                        if equal_state_k[k].count(equal_state_k[i][j].transitions[dfa.InputSymbols[1]]) != 0:
                            x += equal_state_k[k][0].state_ID
                            break
                elif len(dfa.InputSymbols) == 1:
                    # Check whether we have only 1 input symbol 
                    # Repeat previous operations for one input symbol
                    for k in range(len(equal_state_k)):
                        if equal_state_k[k].count(equal_state_k[i][j].transitions[dfa.InputSymbols[0]]) != 0:
                            x += equal_state_k[k][0].state_ID
                            break

                # If two states go through same equivalence list in k_equivalence table they have the same equivalence list in k+1_equivalence 
                if x in product_equal_states:
                    product_equal_states[x].append(equal_state_k[i][j])
                else:
                    temp = []
                    temp.append(equal_state_k[i][j])
                    product_equal_states[x] = temp

            # Construct k+1_equivalence table
            for tmp in product_equal_states.values():
                equal_state_k_next.append(tmp)

        # Check whether k+1_equivalence and k_equivalence are the same if yes --> quit while loop if no --> go through next equivalence table
        if len(equal_state_k_next) == len(equal_state_k):
            break

        equal_state_k = equal_state_k_next

    # For each equivalence list in k_equivalence table order the states by state ID
    for i in range(len(equal_state_k)):
        equal_state_k[i] = sorted(equal_state_k[i], key=lambda x: re.sub("q", "", x.state_ID))

    # For every list in k_equivalence table order the states in each list by the first state of the list
    equal_state_k = sorted(equal_state_k, key=lambda x: re.sub("q", "", x[0].state_ID))

    # Construct new DFA by the result of equivalence table
    new_dfa_states = []
    for i in range(len(equal_state_k)):
        x = ""
        for j in range(len(equal_state_k[i])):
            x += equal_state_k[i][j].state_ID

        new_dfa_states.append(NewState(x))
    ###########################################################
    new_dfa_final_states = []
    for i in range (len(equal_state_k)):
        if equal_state_k[i][0] in dfa.FinalStates :
            new_dfa_final_states.append(new_dfa_states[i])

    new_dfa_initial_state=None
    for i in range(len(equal_state_k)):
        if(dfa.InitialState in equal_state_k[i]):
            new_dfa_initial_state=new_dfa_states[i]
            break
    
    new_dfa = DFA(0, new_dfa_states, dfa.InputSymbols, new_dfa_initial_state, new_dfa_final_states)
    if len(dfa.InputSymbols.inputs) == 2:
        for i in range (len(equal_state_k)):
            for k in range (len(equal_state_k)):
                if equal_state_k[i][0].transitions[dfa.InputSymbols.inputs[0]] in equal_state_k[k]:
                    new_dfa_states[i].transitions[dfa.InputSymbols.inputs[0]] = new_dfa_states[k]
                    break
            for k in range (len(equal_state_k)):
                if equal_state_k[i][0].transitions[dfa.InputSymbols.inputs[1]] in equal_state_k[k]:
                    new_dfa_states[i].transitions[dfa.InputSymbols.inputs[1]] = new_dfa_states[k]
                    break

    elif len(dfa.InputSymbols.inputs) == 1:
        for i in range (len(equal_state_k)):
            for k in range (len(equal_state_k)):
                if equal_state_k[i][0].transitions[dfa.InputSymbols.inputs[0]] in equal_state_k[k]:
                    new_dfa_states[i].transitions[dfa.InputSymbols.inputs[0]] = new_dfa_states[k]
                    break

    return new_dfa
        

if __name__ == '__main__':
    """ the main function for visualize the FA"""
    args = sys.argv[1:]
    #json_path = args[0]   # the relative path of the json file containing the dfa or nfa in the desired format
    json_path = "samples/phase2-sample/in/input1.json"
    try:
            read_fa(json_path)
            fa = create_standard_fa(0)
            dfa = VisualDFA(fa)
            # init_state = NewState(fa["initial_state"])
            # input=DFA(0,list(fa["states"]),list(fa["input_symbols"]), init_state,list(fa["final_states"]))

    except Exception as ex:
        raise Exception("The input file is neither DFA nor NFA\nCheck whether you "
                            "mentioned a correct file or its in the correct standard format")\
            from ex

    states1=list(dfa.states)
    states1.sort()
    #print(states1)

    symbols1=list(dfa.input_symbols)
    symbols1.sort()
    #print(symbols1)
    
    Trans1 = dfa.transitions
    #print(Trans1)

    start_state1 = dfa.initial_state
    #print (f'starting state1: {start_state1}')
    #print(type(start_state1))
    final_states1 = set(dfa.final_states)
    #print (type(final_states1))
    SimplificationDFA(input)
    # visualize(json_path)  # visualize the FA
