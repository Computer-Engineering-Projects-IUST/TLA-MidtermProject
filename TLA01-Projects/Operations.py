import sys
from visualize import visualize
from FA.dfa import VisualDFA
from FA.nfa import VisualNFA
from utils import read_fa, create_standard_fa
from frozendict import frozendict


def ChangeTransition (OldTransition, GoalState, Symbol):
    #print(OldTransition)
    new_set = frozenset({GoalState})
    new_dict = frozendict({Symbol: new_set})
    #for key, value in OldTransition.items():
        # print(f'value is: {value}')
        # print(f'new_dict is: {new_dict}')
        # OldTransition.remove(value)
        # OldTransition.update(new_dict)
    return new_dict


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


def StarMain (): #Star
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


def Star (states, symbols, Trans, start_state, final_states):
    new_dict = dict(Trans)

    New_Start_State = 'q' + str(len(states))
    states.append(New_Start_State)
    states.sort()

    New_Final_State = 'q' + str(len(states))
    states.append(New_Final_State)
    states.sort()
    #print (states)

    new_dict[New_Start_State] = AddLambda(New_Start_State, start_state, new_dict)

    for FinalState in final_states:
        try:                                        # already has a lambda transition
            new_dict[FinalState] = AppendLambda(FinalState, New_Final_State, new_dict)
        
        except:                                     # Does not have a lambda transition
            new_dict[FinalState] = AddLambda(FinalState, New_Final_State, new_dict)

    new_dict[New_Start_State] = AppendLambda(New_Start_State, New_Final_State, new_dict)

    new_dict[New_Final_State] = AddLambda(New_Final_State, New_Start_State, new_dict)

    new_frozendict = frozendict(new_dict)

    #print(new_frozendict)








def UnionMain ():
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
    #print(type(start_state1))
    final_states1 = set(nfa1.final_states)
    #print (type(final_states1))


    states2=list(nfa2.states)
    states2.sort()
    #print(type(states2))

    symbols2=list(nfa2.input_symbols)
    symbols2.sort()
    #print(symbols2)
    
    Trans2 = nfa2.transitions
    #print(Trans2)

    start_state2 = nfa2.initial_state
    #print (f'starting state2: {start_state2}')
    final_states2 = set(nfa2.final_states)
    #print (final_states2)

    Union(states1, symbols1, Trans1, start_state1, final_states1, states2, symbols2, Trans2, start_state2, final_states2)


def Union (states1, symbols1, Trans1, start_state1, final_states1, states2, symbols2, Trans2, start_state2, final_states2):
    new_dict1 = dict(Trans1)
    new_dict2 = dict(Trans2)
    Result_dict = new_dict1.copy()
    Result_States = states1.copy()

    New_Start_State = 'q' + str(len(states1) + len(states2))
    Result_States.append(New_Start_State)
    Result_States.sort()
    Result_dict[New_Start_State] = AddLambda(New_Start_State, start_state1, Result_dict)
    

    New_Final_State = 'q' + str(len(states1) + len(states2) + 1)
    Result_States.append(New_Final_State)
    Result_States.sort()
    #print (Result_States)
    for FinalState in final_states1:
        try:                                        # already has a lambda transition
            Result_dict[FinalState] = AppendLambda(FinalState, New_Final_State, Result_dict)
        
        except:                                     # Does not have a lambda transition
            Result_dict[FinalState] = AddLambda(FinalState, New_Final_State, Result_dict)


    new_dict2_copy = new_dict2.copy()
    changedStart2 = False
    StatesRelationDict = {}
    #print(StatesRelationDict)
    for state in states2:
        New_state = 'q' + str(len(Result_States) - len(states2) + 1)
        StatesRelationDict[state]= New_state
        #print (StatesRelationDict)
        Result_States.append(New_state)
        #new_dict2_copy[New_state] = ChangeTransition(new_dict2[state], New_state, 'b')
        #print(new_dict2_copy[New_state])
        if state == start_state2 and changedStart2 == False:
            #print(f'state is: {state} and start state2 is:  {start_state2} and new state is: {New_state}')
            start_state2 = New_state
            changedStart2 = True
        if state in final_states2:
            final_states2.remove(state)
            final_states2.update(New_state)

    # print(new_dict2)
    # for state in states2:
    #     #print(set(new_dict2[state]['b']))
    #     # if ('q1' in set(new_dict2[state]['b'])):
    #     #     print ('state in set(new_dict2[state][''])')
    #     for sym in symbols2:
    #         #print(f'current symbol is: {sym}')
    #         try:
    #             tempset = set(new_dict2[state][sym])
    #             tempset_copy = tempset.copy()
    #             #print(f'1. temp set is: {tempset}')
    #             for st in tempset_copy:
    #                 #print(f'state is {st}')
    #                 tempset.remove(st)
    #                 newst = StatesRelationDict[st]
    #                 #print(f'type of newst is: {type(newst)}')
    #                 tempset.add(newst)
    #                 #print('tempst updated')
    #             #print(f'2. temp set is: {tempset}')
    #             #print (type(new_dict2[state][sym]))
    #             tempset = frozenset(tempset)
    #             connection = frozendict({sym:tempset})
    #             print(connection)
    #             print(f'Version 1 of new_dict2_copy[state] : {new_dict2_copy[state]}')
    #             new_dict2_copy[state] = connection
    #             print(f'Version 2 of new_dict2_copy[state] : {new_dict2_copy[state]}')
    #             print(tempset)
    #         except Exception as e:
    #             #print(f'Error is: {e}')
    #             print()
    #         #print("*********************")
# """
#     temp = set(Dict[Source][""])
#     temp.add(Dest)
#     temp = frozenset(temp)
#     ConnectSRCToFinal = frozendict({"":temp})
#     Dict[Source] = ConnectSRCToFinal
#     return Dict[Source]
# """
    # print("*************")
    # print(new_dict2_copy)
    for state in states1:
        del new_dict2_copy[state]

    
    Result_dict.update(new_dict2_copy)
    #print(f'Start State2: {start_state2}   and final state2: {final_states2}')
    
    Result_dict[New_Start_State] = AppendLambda(New_Start_State, start_state2, Result_dict)
    for FinalState in final_states2:
        try:                                        # already has a lambda transition
            Result_dict[FinalState] = AppendLambda(FinalState, New_Final_State, Result_dict)
        
        except:                                     # Does not have a lambda transition
            Result_dict[FinalState] = AddLambda(FinalState, New_Final_State, Result_dict)

    print(Result_dict)

if __name__ == '__main__':
    
    #StarMain()
    UnionMain()

    
