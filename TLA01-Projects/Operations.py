import sys
from visualize import visualize
from FA.dfa import VisualDFA
from FA.nfa import VisualNFA
from utils import read_fa, create_standard_fa
from frozendict import frozendict


def AddLambda (Source, Dest, Dict):     # Does not have a lambda transition
    ConnectToSRC = frozendict({"":frozenset({Dest})})
    Dict[Source] = ConnectToSRC
    return Dict[Source]

def AppendLambda(Source, Dest, Dict):   # already has a lambda transition
    temp = set(Dict[Source][""])
    temp.add(Dest)
    temp = frozenset(temp)
    ConnectSRCToFinal = frozendict({"":temp})
    Dict[Source] = ConnectSRCToFinal
    return Dict[Source]



def Star (states, symbols, Trans, start_state, final_states):
    new_dict = dict(Trans)

    New_Start_State = 'q' + str(len(states))
    states.append(New_Start_State)
    states.sort()

    New_Final_State = 'q' + str(len(states))
    states.append(New_Final_State)
    states.sort()
    print (states)

    new_dict[New_Start_State] = AddLambda(New_Start_State, start_state, new_dict)

    for FinalState in final_states:
        try:                                        # already has a lambda transition
            new_dict[FinalState] = AppendLambda(FinalState, New_Final_State, new_dict)
        
        except:                                     # Does not have a lambda transition
            new_dict[FinalState] = AddLambda(FinalState, New_Final_State, new_dict)

    new_dict[New_Start_State] = AppendLambda(New_Start_State, New_Final_State, new_dict)

    new_dict[New_Final_State] = AddLambda(New_Final_State, New_Start_State, new_dict)

    new_frozendict = frozendict(new_dict)

    print(new_frozendict)


# def Union (states1, symbols, Trans1, start_state1, final_states1, states2, Trans2, start_state2, final_states2):
#     new_dict = dict(Trans)

#     New_Start_State = 'q' + str(len(states))
#     states.append(New_Start_State)
#     states.sort()

#     New_Final_State = 'q' + str(len(states))
#     states.append(New_Final_State)
#     states.sort()
#     print (states)

#     # ConnectToStart = frozendict({"":frozenset({start_state})})
#     # new_dict[New_Start_State] = ConnectToStart
#     new_dict[New_Start_State] = AddLambda(New_Start_State, start_state, new_dict)

#     for FinalState in final_states:
#         try:                                        # already has a lambda transition
#             # temp = set(new_dict[FinalState][""])
#             # temp.add(New_Final_State)
#             # temp = frozenset(temp)
#             # ConnectFinalToFinal = frozendict({"":temp})
#             # new_dict[FinalState] = ConnectFinalToFinal
#             new_dict[FinalState] = AppendLambda(FinalState, New_Final_State, new_dict)
        
#         except:                                     # Does not have a lambda transition
#             # ConnectToFinal = frozendict({"":frozenset({New_Final_State})})
#             # new_dict[FinalState] = ConnectToFinal
#             new_dict[FinalState] = AddLambda(FinalState, New_Final_State, new_dict)


#     # temp = set(new_dict[New_Start_State][""])
#     # temp.add(New_Final_State)
#     # temp = frozenset(temp)
#     # ConnectStartToFinal = frozendict({"":temp})
#     # new_dict[New_Start_State] = ConnectStartToFinal
#     new_dict[New_Start_State] = AppendLambda(New_Start_State, New_Final_State, new_dict)

#     # ConnectFinalToStart = frozendict({"":frozenset({New_Start_State})})
#     # new_dict[New_Final_State] = ConnectFinalToStart
#     new_dict[New_Final_State] = AddLambda(New_Final_State, New_Start_State, new_dict)

#     new_frozendict = frozendict(new_dict)

#     print(new_frozendict)

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
    
    