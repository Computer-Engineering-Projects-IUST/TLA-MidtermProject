import sys
from visualize import visualize
from FA.dfa import VisualDFA
from FA.nfa import VisualNFA
from utils import read_fa, create_standard_fa

from automata.fa.nfa import NFA

# from visual_automata.fa.nfa import VisualNFA


if __name__ == '__main__':
    """ the main function for visualize the FA"""
    args = sys.argv[1:]
    #json_path = args[0]   # the relative path of the json file containing the dfa or nfa in the desired format
    json_path = "samples/phase1-sample/in/input1.json"#args[0]  
    try:
            read_fa(json_path)
            fa = create_standard_fa(1)
            nfa = VisualNFA(fa)
    except Exception as ex:
        raise Exception("The input file is neither DFA nor NFA\nCheck whether you "
                            "mentioned a correct file or its in the correct standard format")\
            from ex

#     visualize(json_path)  # visualize the FA
#     print(nfa.initial_state)

    states=list(nfa.states)
    symbols=list(nfa.input_symbols)
    symbols.sort()
#     print(symbols)
    states.sort()
#     print (states)
#     table = []
#     needTrap=False
#     newStates=[['0','0']]
#     newStates.remove(['0','0'])
#     set=[]
#     newStart=set(nfa.initial_state)
newStart={nfa.initial_state}
newFinal={"0"}
newFinal.remove("0")


###test
newTr={ frozenset({'d1'}): {
        'name': {'bob'},
        'place': {'lawn'},
        'animal': {'man'}
    }}
newTr.clear()

print(type(newTr))
print(type(nfa.transitions['q0']))
###



#    print(nfa.transitions[states[0]][symbols[0]])
if("" in nfa.transitions[nfa.initial_state]):
        newStart.union(set(nfa.transitions[nfa.initial_state][""]))
        # print(newStart)


queue = [newStart]
dfa_states=[newStart]
print(dfa_states)

while queue:
        currentSet = queue.pop(0)
        # newTr[currentSet]={{"df"}:{"ff"}}
        # newTr[currentSet].clear()
        # for currentState in currentSet:
                
        
        # For each input symbol:
        for symbol in symbols:
            # Find set of states reachable from current state on 
            # input symbol by taking epsilon closures and following 
            # transitions
            next_states = {"a"}
            next_states.remove("a")
            for currentState in currentSet:
                if(symbol in nfa.transitions[currentState]):
                        
                    temp=list(nfa.transitions[currentState][symbol])[0]
                    next_states.add(temp)
                    while( "" in nfa.transitions[temp]):
                        next_states.add(list(nfa.transitions[temp][""])[0])
                        temp=list(nfa.transitions[temp][""])[0]

                # next_states |= nfa.transitions.get((state, symbol), set())
                # next_states |= nfa.epsilon_closure(next_states)
                
            
            # If this set is not already in the set of DFA states, add it 
            # to the set and add it to the queue
            if next_states and next_states not in dfa_states:
                dfa_states.append(next_states)
                queue.append(next_states)
                for x in nfa.final_states:
                    if(x in next_states):
                        newFinal.add(frozenset(next_states))
                        break
            
            # Add a transition from current state on input symbol to 
            # this new set of states in DFA transition table
            if next_states:
                ############################error :can not add transition
                if frozenset(currentSet) in newTr:
                    newTr[frozenset(currentSet)].update({symbol:next_states})
                else:
                     newTr.update({frozenset(currentSet):{symbol:next_states}}) 
                # newTr[frozenset(currentSet)][symbol]=next_stfates
                # fa["transitions"][state][key] = eval(fa["transitions"][state][key])
                # nfa.add[(currentSet, symbol)] = frozenset(next_states)
                # print ("if is running")
            else:
                if {"trap"} in dfa_states:
                    if frozenset(currentSet) in newTr:
                        newTr[frozenset(currentSet)].update({symbol:{"trap"}})
                    else:
                        newTr.update({frozenset(currentSet):{symbol:{"trap"}}}) 
                    # newTr.update({frozenset(currentSet):{symbol:{"trap"}}}) 
                else:
                    dfa_states.append({"trap"})
                    if frozenset(currentSet) in newTr:
                        newTr[frozenset(currentSet)].update({symbol:{"trap"}})
                    else:
                        newTr.update({frozenset(currentSet):{symbol:{"trap"}}}) 

                    # newTr.update({frozenset(currentSet):{symbol:{"trap"}}})

# for state in dfa_states:
#     for symbol in symbols:
#         if symbol not in newTr[frozenset(state)]:
#             if {"trap"} in dfa_states:
#                newTr.update({frozenset(state):{symbol:{"trap"}}}) 
#             else:
#                 dfa_states.append({"trap"})
#                 newTr.update({frozenset(state):{symbol:{"trap"}}}) 
print("this is the end")



#     for state in states:
#         line=[]
#         #check for lamda transition
#         if("" in nfa.transitions[state]):
#                 newStates.append([state,list(nfa.transitions[state][""])[0]])

#         for s in symbols:
#                 if(s in nfa.transitions[state]):
#                         #what if there were two a in transitions
#                         line.append(set(nfa.transitions[state][s]))
#                 else:
#                         line.append(0)
#                         needTrap=True
#         table.append(line)

#     for ns in newStates:
#         for item in ns:
#                 if("" in nfa.transitions[item]):
#                         if not (list(nfa.transitions[item][""])[0] in ns):
#                                 ns.append(list(nfa.transitions[item][""])[0])
#         line=[]
#         for j in range(symbols.__len__()):
#                 ans=[]
#                 for i in ns:
#                         if(table[states.index(i)][j]):
#                                 ans.append(table[states.index(i)][j])
#                 if(ans.__len__):
#                         line.append(ans)
#                 else:
#                         line.append(0)

#         for s in ns:
#                 states.remove(s)
#         states.append(ns)
#         for i in table:
#                 for j in i:
#                         print("hey")

        
                







#     print("end")





