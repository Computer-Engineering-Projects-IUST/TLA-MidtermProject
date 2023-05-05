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


def Union (states1, symbols1, Trans1, start_state1, final_states1, states2, symbols2, Trans2, start_state2, final_states2):
    new_dict1 = dict(Trans1)
    new_dict2 = dict(Trans2)
    Result_dict = new_dict1.copy()

    Result_States = states1.copy()
    #print(states1)
    # print(Result_States)
    #print(new_dict2)
    # print ('q' + str(len(states1)))
    # Result_States.append('q' + str(len(states1)))
    # print(Result_States)
    new_dict2_copy = new_dict2.copy()
    for state in states2:
        New_state = 'q' + str(len(Result_States))
        Result_States.append(New_state)
        new_dict2_copy[New_state] = new_dict2[state]
        #del new_dict2_copy[state]
        # print(f'State is: {state} and New_state is: {New_state}')
        #print(f'new_dict2[state] is: {new_dict2[state]}')
    #     print(f'new_dict2_copy[New_state] is: {new_dict2_copy[New_state]}')
    #     print("==================")
    # print(new_dict2_copy)
    # print(Result_States)
    #print (states1)
    for state in states1:
        #print(state)
        del new_dict2_copy[state]

    #print(new_dict2_copy)
    Result_dict.update(new_dict2_copy)
    #print(Result_dict)
    # New_Start_State = 'q' + str(len(states))
    # states.append(New_Start_State)
    # states.sort()

    # New_Final_State = 'q' + str(len(states))
    # states.append(New_Final_State)
    # states.sort()
    # print (states)

    # # ConnectToStart = frozendict({"":frozenset({start_state})})
    # # new_dict[New_Start_State] = ConnectToStart
    # new_dict[New_Start_State] = AddLambda(New_Start_State, start_state, new_dict)

    # for FinalState in final_states:
    #     try:                                        # already has a lambda transition
    #         # temp = set(new_dict[FinalState][""])
    #         # temp.add(New_Final_State)
    #         # temp = frozenset(temp)
    #         # ConnectFinalToFinal = frozendict({"":temp})
    #         # new_dict[FinalState] = ConnectFinalToFinal
    #         new_dict[FinalState] = AppendLambda(FinalState, New_Final_State, new_dict)
        
    #     except:                                     # Does not have a lambda transition
    #         # ConnectToFinal = frozendict({"":frozenset({New_Final_State})})
    #         # new_dict[FinalState] = ConnectToFinal
    #         new_dict[FinalState] = AddLambda(FinalState, New_Final_State, new_dict)


    # # temp = set(new_dict[New_Start_State][""])
    # # temp.add(New_Final_State)
    # # temp = frozenset(temp)
    # # ConnectStartToFinal = frozendict({"":temp})
    # # new_dict[New_Start_State] = ConnectStartToFinal
    # new_dict[New_Start_State] = AppendLambda(New_Start_State, New_Final_State, new_dict)

    # # ConnectFinalToStart = frozendict({"":frozenset({New_Start_State})})
    # # new_dict[New_Final_State] = ConnectFinalToStart
    # new_dict[New_Final_State] = AddLambda(New_Final_State, New_Start_State, new_dict)

    # new_frozendict = frozendict(new_dict)

    # print(new_frozendict)

if __name__ == '__main__':
    #Star
    # """ the main function for visualize the FA"""
    # args = sys.argv[1:]
    # #json_path = args[0]   # the relative path of the json file containing the dfa or nfa in the desired format
    # json_path = "samples/phase4-sample/star/in/FA.json"
    # try:
    #         read_fa(json_path)
    #         fa = create_standard_fa(1)
    #         nfa = VisualNFA(fa)
    # except Exception as ex:
    #     raise Exception("The input file is neither DFA nor NFA\nCheck whether you "
    #                         "mentioned a correct file or its in the correct standard format")\
    #         from ex

    # states=list(nfa.states)
    # states.sort()
    # #print(states)

    # symbols=list(nfa.input_symbols)
    # symbols.sort()
    # #print(symbols)
    
    # Trans = nfa.transitions
    # #print(Trans)

    # start_state = nfa.initial_state
    # #print (f'starting state: {start_state}')
    # final_states = nfa.final_states
    # #print (final_states)
    # Star(states, symbols, Trans, start_state, final_states)
    
    #Union
    """ the main function for visualize the FA"""
    args = sys.argv[1:]
    #json_path = args[0]   # the relative path of the json file containing the dfa or nfa in the desired format
    json_path1 = "samples/phase4-sample/union/in/FA1.json"
    json_path2 = "samples/phase4-sample/union/in/FA2.json"
    try:
            read_fa(json_path1)
            fa = create_standard_fa(1)
            nfa1 = VisualNFA(fa)

            read_fa(json_path2)
            fa = create_standard_fa(1)
            nfa2 = VisualNFA(fa)
    except Exception as ex:
        raise Exception("The input file is neither DFA nor NFA\nCheck whether you "
                            "mentioned a correct file or its in the correct standard format")\
            from ex

    states1=list(nfa1.states)
    states1.sort()
    #print(states1)

    symbols1=list(nfa1.input_symbols)
    symbols1.sort()
    #print(symbols1)
    
    Trans1 = nfa1.transitions
    #print(Trans1)

    start_state1 = nfa1.initial_state
    #print (f'starting state1: {start_state1}')
    final_states1 = nfa1.final_states
    #print (final_states1)


    states2=list(nfa2.states)
    states2.sort()
    #print(states2)

    symbols2=list(nfa2.input_symbols)
    symbols2.sort()
    #print(symbols2)
    
    Trans2 = nfa2.transitions
    #print(Trans2)

    start_state2 = nfa2.initial_state
    #print (f'starting state2: {start_state2}')
    final_states2 = nfa2.final_states
    #print (final_states2)

    Union(states1, symbols1, Trans1, start_state1, final_states1, states2, symbols2, Trans2, start_state2, final_states2)
