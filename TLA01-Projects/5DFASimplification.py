import json
import re
import sys
from visualize import visualize
from FA.dfa import VisualDFA
from FA.nfa import VisualNFA
from utils import read_fa, create_standard_fa
from automata.fa.nfa import NFA

def DFS_Visit_Recursive(Visited, state, dfs_visit, InputSymbols, transitions):
    Visited[state] = True
    for i in range(len(InputSymbols)):
        try:
            if Visited[transitions[state][InputSymbols[i]]] == False:
                dfs_visit.append(transitions[state][InputSymbols[i]])
                DFS_Visit_Recursive(Visited, transitions[state][InputSymbols[i]], dfs_visit, InputSymbols, transitions)
        except:
            print()


if __name__ == '__main__':
    """ the main function for visualize the FA"""
    args = sys.argv[1:]
    #json_path = args[0]   # the relative path of the json file containing the dfa or nfa in the desired format
    json_path = "samples/phase2-sample/in/input3.json"
    try:
            read_fa(json_path)
            fa = create_standard_fa(0)
            dfa = VisualDFA(fa)
            dfa.show_diagram()

    except Exception as ex:
        raise Exception("The input file is neither DFA nor NFA\nCheck whether you "
                            "mentioned a correct file or its in the correct standard format")\
            from ex

    states=list(dfa.states)
    states.sort()

    symbols=list(dfa.input_symbols)
    symbols.sort()
    #print(symbols1)
    
    Transitions = dfa.transitions
    #print(Trans1)

    initialState = dfa.initial_state
    #print (f'starting state1: {start_state1}')
    #print(type(start_state1))
    finalStates = list(dfa.final_states)

    dfs_visit=[]
    dfs_visit.append(initialState)
    Visited = {}
    for s in states:
        Visited[s] = False
    DFS_Visit_Recursive(Visited,initialState,dfs_visit,symbols,Transitions)
    print("dfs is done")
    states=dfs_visit

    new_final_state = []
    # Remove non-reachable states from DFA
    for i in range(len(finalStates)):
        if finalStates[i] in dfs_visit:
            new_final_state.append(finalStates[i])
    finalStates = new_final_state

    #create accepting and non accepting statesd
    nonFinalStates=[]
    for state in states:
        if(state not in finalStates):
            nonFinalStates.append(state)
    currentStates=[set(nonFinalStates),set(finalStates)]
    CurrentStatesIndex={}
    for s in finalStates:
        CurrentStatesIndex[s]=1
    for s in nonFinalStates:
        CurrentStatesIndex[s]=0



    while(True):
        newGroups=[{}]
        newGroups.remove({})
        newGroupsIndex={}
        for states in currentStates:
            for currentState1 in states:
                if(currentState1 not in newGroupsIndex):
                    newGroupsIndex[currentState1]=len(newGroups)
                    newGroups.append({currentState1})
                for currentState2 in states:
                    same=True
                    for symbol in symbols:
                        if(CurrentStatesIndex[Transitions[currentState1][symbol]]!=CurrentStatesIndex[Transitions[currentState2][symbol]]):
                            same=False
                            break
                    if(same):
                        newGroups[newGroupsIndex[currentState1]].add(currentState2)
                        newGroupsIndex[currentState2]=newGroupsIndex[currentState1]
                    else:
                        if(currentState2 not in newGroupsIndex):
                            newGroupsIndex[currentState2]=len(newGroups)
                            newGroups.append({currentState2})
        if(len(newGroups)==len(currentStates)):
            break
        else:
            currentStates=newGroups
            CurrentStatesIndex=newGroupsIndex
print("done")

            










