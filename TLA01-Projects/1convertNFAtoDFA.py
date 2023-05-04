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
    json_path = "samples/phase1-sample/in/input2.json"#args[0]  
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
        for symbol in symbols:
            next_states = {"a"}
            next_states.remove("a")
            for currentState in currentSet:
                if(symbol in nfa.transitions[currentState]):
                        
                    temp=list(nfa.transitions[currentState][symbol])[0]
                    next_states.add(temp)
                    while( "" in nfa.transitions[temp]):
                        next_states.add(list(nfa.transitions[temp][""])[0])
                        temp=list(nfa.transitions[temp][""])[0]
                
            if next_states and next_states not in dfa_states:
                dfa_states.append(next_states)
                queue.append(next_states)
                for x in nfa.final_states:
                    if(x in next_states):
                        newFinal.add(frozenset(next_states))
                        break
            
            if next_states:

                if '-'.join(currentSet) in newTr:
                    newTr['-'.join(currentSet)].update({symbol:{'-'.join(next_states)}})
                else:
                     newTr.update({'-'.join(currentSet):{symbol:{'-'.join(next_states)}}}) 

            else:
                if {"trap"} in dfa_states:
                    if '-'.join(currentSet) in newTr:
                        newTr['-'.join(currentSet)].update({symbol:{"trap"}})
                    else:
                        newTr.update({'-'.join(currentSet):{symbol:{"trap"}}}) 
                else:
                    dfa_states.append({"trap"})
                    if '-'.join(currentSet) in newTr:
                        newTr['-'.join(currentSet)].update({symbol:{"trap"}})
                    else:
                        newTr.update({'-'.join(currentSet):{symbol:{"trap"}}}) 

print("this is the end of DFA")

stringStates=set()
for s in dfa_states:
    stringStates.add('-'.join(s))
fa["initial_state"]='-'.join(newStart)
fa["states"]=stringStates
StringFinalStates=set()
for s in newFinal:
    StringFinalStates.add('-'.join(s))
fa["final_states"]=StringFinalStates
fa["transitions"]=newTr

nfa = VisualNFA(fa)
nfa.show_diagram()
print("done")







