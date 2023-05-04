
import sys
from visualize import visualize
from FA.dfa import VisualDFA
from FA.nfa import VisualNFA
from utils import read_fa, create_standard_fa
from frozendict import frozendict


def Star (states, symbols, Trans, start_state, final_states):
    new_dict = dict(Trans)

    #print('q' + str(len(states)))
    New_Start_State = 'q' + str(len(states))
    states.append(New_Start_State)
    states.sort()

    New_Final_State = 'q' + str(len(states))
    states.append(New_Final_State)
    states.sort()
    print (states)

    ConnectToStart = frozendict({"":frozenset({start_state})})
    new_dict[New_Start_State] = ConnectToStart
    #print(f'type of new_dict[New_Start_State] is : {type (new_dict[New_Start_State])}')
    for FinalState in final_states:
        print(FinalState)
        #ConnectToFinal = frozendict({"":frozenset({New_Final_State})})
        #print(f"ToBeAdded: {toBeAdded}")
        # temp = dict(new_dict[FinalState])
        # #new_dict[FinalState]= ConnectToFinal ############################################
        # # temp.append(ConnectToFinal)
        # # temp_frozen = frozendict(temp)
        # # new_dict[FinalState] = temp_frozen
        # #print(new_dict[FinalState])
        # # print (FinalState)
        # # print(type(new_dict[FinalState]))
        # temp[""] = frozenset({New_Final_State})
        # temp = set(new_dict[FinalState][""])
        # temp.add(New_Final_State)
        # temp = frozenset(temp)
        # ConnectFinalToFinal = frozendict({"":temp})
        # new_dict[FinalState] = ConnectFinalToFinal
        try:                                        # already has a lambda transition
            temp = set(new_dict[FinalState][""])
            temp.add(New_Final_State)
            temp = frozenset(temp)
            ConnectFinalToFinal = frozendict({"":temp})
            new_dict[FinalState] = ConnectFinalToFinal
        except:                                     # Does not have a lambda transition
            ConnectToFinal = frozendict({"":frozenset({New_Final_State})})
            new_dict[FinalState] = ConnectToFinal

    #print(new_dict)
    # ConnectStartToFinal = frozendict({"":frozenset({New_Final_State})})
    # new_dict[New_Start_State] = ConnectStartToFinal #########################################
    # print("Connected start to final")
    temp = set(new_dict[New_Start_State][""])
    temp.add(New_Final_State)
    temp = frozenset(temp)
    ConnectStartToFinal = frozendict({"":temp})
    new_dict[New_Start_State] = ConnectStartToFinal

    ConnectFinalToStart = frozendict({"":frozenset({New_Start_State})})
    new_dict[New_Final_State] = ConnectFinalToStart
    print("Connected final to start")

    new_frozendict = frozendict(new_dict)
    print(new_frozendict)

if __name__ == '__main__':
    """ the main function for visualize the FA"""
    args = sys.argv[1:]
    #json_path = args[0]   # the relative path of the json file containing the dfa or nfa in the desired format
    json_path = "samples/phase4-sample/star/in/FA.json"
    try:
            read_fa(json_path)
            fa = create_standard_fa(1)
            nfa = VisualNFA(fa)
    except Exception as ex:
        raise Exception("The input file is neither DFA nor NFA\nCheck whether you "
                            "mentioned a correct file or its in the correct standard format")\
            from ex

    states=list(nfa.states)
    states.sort()
    #print(states)

    symbols=list(nfa.input_symbols)
    symbols.sort()
    #print(symbols)
    
    Trans = nfa.transitions
    #print(Trans)

    start_state = nfa.initial_state
    #print (f'starting state: {start_state}')
    final_states = nfa.final_states
    #print (final_states)
    Star(states, symbols, Trans, start_state, final_states)
    
    