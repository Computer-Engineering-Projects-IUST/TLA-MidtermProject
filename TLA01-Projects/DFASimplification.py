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

def DFS_Visit_Recursive(Visited, state, dfs_visit, InputSymbols, transitions):
    Visited[state] = True
    for i in range(len(InputSymbols)):
        try:
            # print(transitions[state])
            # print(InputSymbols[i])
            # print(transitions[state][InputSymbols[i]])

            if Visited[transitions[state][InputSymbols[i]]] == False:
                dfs_visit.append(transitions[state][InputSymbols[i]])
                DFS_Visit_Recursive(Visited, transitions[state][InputSymbols[i]], dfs_visit, InputSymbols, transitions)
        except:
            print()

def SimplificationDFA(states, symbols, FrozTrans, InitialState, FinalStates):
    Trans = dict(FrozTrans)
    FinalStates = list(FinalStates)
    dfs_visit = []
    dfs_visit.append(InitialState)
    Visited = {}
    for s in states:
        Visited[s] = False
    # First we go through vertexes by DFS to define non-reachable states
    DFS_Visit_Recursive(Visited, InitialState, dfs_visit, symbols, Trans)
    #print(f'Visited is: {Visited}')
    states = dfs_visit
    
    new_final_state = []
    # Remove non-reachable states from DFA
    for i in range(len(FinalStates)):
        if FinalStates[i] in dfs_visit:
            new_final_state.append(FinalStates[i])
    FinalStates = new_final_state

    # Construct zero_equivalence by separating final and non-final states
    final = []
    nonfinal = []
    for i in range(len(states)):
        if states[i] in FinalStates:
            final.append(states[i])
        else:
            nonfinal.append(states[i])

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
            Current_equal_state_k = equal_state_k[i]
            for j in range(len(Current_equal_state_k)):
                x = ""
                # Check whether we have 2 input symbols 
                if len(symbols) == 2:
                    # Check whether for each input symbol which equivalence list we reach + add first state of the previous list to x(string)
                    for k in range(len(equal_state_k)):
                        # print(f"Trans[equal_state_k[i][j]][symbols[0]] is : {Trans[equal_state_k[i][j]][symbols[0]]}")
                        # print(f"equal_state_k[k] is : {equal_state_k[k]}")
                        CurrentTrans = Trans[equal_state_k[k]][symbols[0]]
                        try:
                            #  if Trans[equal_state_k[i][j]][symbols[0]] in equal_state_k[k]:
                            #     # print("Entered HERE 1")
                            #     x += Trans[equal_state_k[i][j]][symbols[0]][]
                            #     break
                           
                            if symbols[0] in CurrentTrans:
                                # print("Entered HERE 1")
                                x += Trans[Current_equal_state_k[j]][symbols[0]]
                                break
                        except:
                            # print("Key not found in 1")
                            print()
                    for k in range(len(equal_state_k)):
                        CurrentTrans = Trans[equal_state_k[k]]
                        try:
                           if symbols[1] in CurrentTrans:
                                # print("Entered HERE 1")
                                x += Trans[Current_equal_state_k[j]][symbols[1]]
                                break
                        except:
                            # print("Key not found in 2")
                            print()
                elif len(dfa.InputSymbols) == 1:
                    # Check whether we have only 1 input symbol 
                    # Repeat previous operations for one input symbol
                    for k in range(len(equal_state_k)):
                        CurrentTrans = Trans[equal_state_k[k]]
                        try:
                            if symbols[0] in CurrentTrans:
                                # print("Entered HERE 1")
                                x += Trans[Current_equal_state_k[j]][symbols[0]]
                                break
                        except:
                            # print("Key not found in 3")
                            print()

                # If two states go through same equivalence list in k_equivalence table they have the same equivalence list in k+1_equivalence 
                if x in product_equal_states:
                    product_equal_states[x].append(equal_state_k[i][j])
                else:
                    temp = []
                    temp.append(equal_state_k[i][j])
                    product_equal_states[x] = temp

            # Construct k+1_equivalence table
            for tmp in product_equal_states:
                equal_state_k_next.append(tmp)

        # Check whether k+1_equivalence and k_equivalence are the same if yes --> quit while loop if no --> go through next equivalence table
        if len(equal_state_k_next) == len(equal_state_k):
            break

        equal_state_k = equal_state_k_next
    print(equal_state_k)

    # For each equivalence list in k_equivalence table order the states by state ID
    for i in range(len(equal_state_k)):
        equal_state_k[i] = sorted(equal_state_k[i], key=lambda x: re.sub("q", "", x)) #################################
    print(equal_state_k)
    # For every list in k_equivalence table order the states in each list by the first state of the list
    equal_state_k = sorted(equal_state_k, key=lambda x: re.sub("q", "", x[0]))  ##############################

    # Construct new DFA by the result of equivalence table
    new_dfa_states = []
    print(equal_state_k)
    for i in range(len(equal_state_k)):
        x = ""
        for j in range(len(equal_state_k[i])):
            x += equal_state_k[i][j]
        print(f'x is: {x}')
        new_dfa_states.append(x)
    print(new_dfa_states)
    ###########################################################
    new_dfa_final_states = []
    for i in range (len(equal_state_k)):
        if equal_state_k[i][0] in FinalStates :
            new_dfa_final_states.append(new_dfa_states[i])

    new_dfa_initial_state=None
    for i in range(len(equal_state_k)):
        if(InitialState in equal_state_k[i]):
            new_dfa_initial_state=new_dfa_states[i]
            break
    
    #new_dfa = DFA(0, new_dfa_states, symbols, new_dfa_initial_state, new_dfa_final_states)
    if len(symbols) == 2:
        for i in range (len(equal_state_k)):
            for k in range (len(equal_state_k)):
                try:
                    if Trans[equal_state_k[i][j]][symbols[0]] in equal_state_k[k]:
                        # print("Entered HERE 4")
                        Trans[new_dfa_states[i]][symbols[0]] = new_dfa_states[k]
                        # print("Entered HERE 5")
                        break
                except:
                    # print("Key not found in 4")
                    print()
            for k in range (len(equal_state_k)):
                try:
                    if Trans[equal_state_k[i][0]][symbols[1]] in equal_state_k[k]:
                        # print("Entered HERE 6")
                        Trans[new_dfa_states[i]][symbols[1]] = new_dfa_states[k]
                        # print("Entered HERE 7")
                        break
                except:
                    # print("Key not found in 5")
                    print()

    elif len(symbols) == 1:
        for i in range (len(equal_state_k)):
            for k in range (len(equal_state_k)):
                if Trans[equal_state_k[i][0]][symbols[0]] in equal_state_k[k]:
                    # print("Entered HERE 9")
                    Trans[new_dfa_states[i]][symbols[0]] = new_dfa_states[k]
                    # print("Entered HERE 10")
                    break
    # print(Trans)
    #return new_dfa
        

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


    #print (type(final_states1))
    SimplificationDFA(states, symbols, Trans, start_state, final_states)
    # visualize(json_path)  # visualize the FA
