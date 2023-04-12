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
    states.sort()
    table = []
    needTrap=False
    newStates=[['0','0']]
    newStates.remove(['0','0'])


#     print(nfa.transitions[states[0]][symbols[0]])
#     print(nfa.transitions[states[0]]['a'])

    for state in states:
        line=[]
        #check for lamda transition
        if("" in nfa.transitions[state]):
                newStates.append([state,list(nfa.transitions[state][""])[0]])

        for s in symbols:
                if(s in nfa.transitions[state]):
                        #what if there were two a in transitions
                        line.append(set(nfa.transitions[state][s]))
                else:
                        line.append(0)
                        needTrap=True
        table.append(line)

    for ns in newStates:
        for item in ns:
                if("" in nfa.transitions[item]):
                        if not (list(nfa.transitions[item][""])[0] in ns):
                                ns.append(list(nfa.transitions[item][""])[0])
        line=[]
        for j in range(symbols.__len__()):
                ans=[]
                for i in ns:
                        if(table[states.index(i)][j]):
                                ans.append(table[states.index(i)][j])
                if(ans.__len__):
                        line.append(ans)
                else:
                        line.append(0)

        for s in ns:
                states.remove(s)
        states.append(ns)
        for i in table:
                for j in i:
                        print("hey")

        
                







    print("end")





