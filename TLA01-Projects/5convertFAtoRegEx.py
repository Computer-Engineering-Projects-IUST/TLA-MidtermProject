import sys
import re
import json
from visualize import visualize
from FA.dfa import VisualDFA
from FA.nfa import VisualNFA
from utils import read_fa, create_standard_fa
from automata.fa.nfa import NFA

if __name__ == '__main__':
    """ the main function for visualize the FA"""
    args = sys.argv[1:]
    #json_path = args[0]   # the relative path of the json file containing the dfa or nfa in the desired format
    jsonpath = "samples/phase5-sample/in/FA.json"#args[0] 
    isDFA=True 

    try:
            read_fa(jsonpath)
            fa = create_standard_fa()
            dfa = VisualDFA(fa)
            # dfa.show_diagram()
    except:
            try:
                isDFA=False
                read_fa(jsonpath)
                fa = create_standard_fa(1)
                dfa = VisualNFA(fa)
                # dfa.show_diagram()
            except Exception as ex:
                raise Exception("The input file is neither DFA nor NFA\nCheck whether you "
                                "mentioned a correct file or its in the correct standard format")\
                    from ex






if(isDFA):
    print("isDFA")

#    write the equation here1111111111
    # Step 1: Assign variables to each state
    variables = {s: f'x_{i}' for i, s in enumerate(dfa.states)}
    X = variables[dfa.initial_state]

    # Step 2: Write equations for each state
    equations = []
    for state in dfa.states:
        R = ''.join(f'{variables[next_state]}|' for symbol, next_state in dfa.transitions[state].items())
        R = f'({R[:-1]})'  # Remove the last | symbol
        L = '1' if state in dfa.final_states else '0'
        equations.append(f'{variables[state]}={R}{variables[state]}+{L}')

    # Step 3: Solve the set of equations
    regex = ''
    while len(equations) > 0:
        # Find an equation with only one variable
        # for i, eqn in enumerate(equations):
        #     if len(re.findall(f'\\b{variables[dfa.initial_state]}\\b', eqn)) == 0 and len(re.findall(f'\\b{variables[list(dfa.final_states)[0]]}\\b', eqn)) == 0 and len(re.findall('[a-z0-9()]+', eqn)) == 1:
        #         regex += eqn.split('=')[1]
        #         var_to_remove = variables[dfa.states[i]]
        #         break
        # else:
        #     raise ValueError("Can't solve equations")

        # Substitute variable in other equations
        equations = [re.sub(f'\\b{var_to_remove}\\b', f'({regex})', eqn) for eqn in equations]
        equations.pop(i)


else:
    #we will convert nfa to dfa and then check the string
    # states=list(nfa.states)
    # symbols=list(nfa.input_symbols)
    # symbols.sort()
    # states.sort()
    # newStart={nfa.initial_state}
    # newFinal={"0"}
    # newFinal.remove("0")

    # newTr={}

    # print(type(newTr))
    # print(type(nfa.transitions['q0']))

    # if("" in nfa.transitions[nfa.initial_state]):
    #     for ns in list(nfa.transitions[nfa.initial_state][""]):
    #         newStart.add(ns)


    # queue = [newStart]
    # dfa_states=[newStart]
    # while queue:
    #         currentSet = queue.pop(0)
    #         for symbol in symbols:
    #             next_states = {"a"}
    #             next_states.remove("a")
    #             for currentState in currentSet:
    #                 if(symbol in nfa.transitions[currentState]):
    #                     for temp in list(nfa.transitions[currentState][symbol]):
                            
    #                         next_states.add(temp)
    #                         Lstack=[]
    #                         if "" in nfa.transitions[temp]:
    #                             for lambdaT in list (nfa.transitions[temp][""] ):
    #                                 Lstack.append(lambdaT)
    #                                 next_states.add(lambdaT)
    #                             while( Lstack):
    #                                 Ltemp=Lstack[0]
    #                                 Lstack.remove(Ltemp)
    #                                 if "" in nfa.transitions[Ltemp]:
    #                                     for t in list (nfa.transitions[Ltemp][""] ):
    #                                         next_states.add(t)
    #                                         Lstack.append(t)
                            

    #             if next_states and next_states not in dfa_states:
    #                 dfa_states.append(next_states)
    #                 queue.append(next_states)
    #                 for x in nfa.final_states:
    #                     if(x in next_states):
    #                         newFinal.add(frozenset(next_states))
    #                         break
                
    #             if next_states:

    #                 if '-'.join(currentSet) in newTr:
    #                     newTr['-'.join(currentSet)].update({symbol:{'-'.join(next_states)}})
    #                 else:
    #                     newTr.update({'-'.join(currentSet):{symbol:{'-'.join(next_states)}}}) 

    #             else:
    #                 if {"trap"} in dfa_states:
    #                     if '-'.join(currentSet) in newTr:
    #                         newTr['-'.join(currentSet)].update({symbol:{"trap"}})
    #                     else:
    #                         newTr.update({'-'.join(currentSet):{symbol:{"trap"}}}) 
    #                 else:
    #                     dfa_states.append({"trap"})
    #                     newTr.update({"trap":{symbols[0]:{"trap"}}})
    #                     for trapS in symbols:
    #                         newTr["trap"].update({trapS:{"trap"}})

    #                     if '-'.join(currentSet) in newTr:
    #                         newTr['-'.join(currentSet)].update({symbol:{"trap"}})
    #                     else:
    #                         newTr.update({'-'.join(currentSet):{symbol:{"trap"}}}) 

    # stringStates=set()
    # for s in dfa_states:
    #     stringStates.add('-'.join(s))
    # fa["initial_state"]='-'.join(newStart)
    # fa["states"]=stringStates
    # StringFinalStates=set()
    # for s in newFinal:
    #     StringFinalStates.add('-'.join(s))
    # fa["final_states"]=StringFinalStates
    # fa["transitions"]=newTr

    # #end of converting to dfa

    # dfa = VisualNFA(fa)
    # dfa.show_diagram()

    
# new code: 00000000000000000000000000000




# def dfa_to_regex():
    # # Step 1: Assign variables to each state
    # variables = {s: f'x_{i}' for i, s in enumerate(fa.states)}
    # X = variables[fa.initial_state]

    # # Step 2: Write equations for each state
    # equations = []
    # for state in fa.states:
    #     R = ''.join(f'{variables[list(next_state)[0]]}|' for symbol, next_state in fa.transitions[state].items())
    #     R = f'({R[:-1]})'  # Remove the last | symbol
    #     L = '1' if state in fa.final_states else '0'
    #     equations.append(f'{variables[state]}={R}{variables[state]}+{L}')

    # # Step 3: Solve the set of equations
    # regex = ''
    # while len(equations) > 0:
    #     # Find an equation with only one variable
    #     for i, eqn in enumerate(equations):
    #         if len(re.findall(f'\\b{variables[fa.initial_state]}\\b', eqn)) == 0 and len(re.findall(f'\\b{variables[list(fa.final_states)[0]]}\\b', eqn)) == 0 and len(re.findall('[a-z0-9()]+', eqn)) == 1:
    #             regex += eqn.split('=')[1]
    #             var_to_remove = variables[fa.states[i]]
    #             break
    #     else:
    #         raise ValueError("Can't solve equations")

    #     # Substitute variable in other equations
    #     equations = [re.sub(f'\\b{var_to_remove}\\b', f'({regex})', eqn) for eqn in equations]
    #     equations.pop(i)

    #     # return regex




        # Step 1: Assign variables to each state

    variables = {s: f'x_{i}' for i, s in enumerate(dfa.states)}
    X = variables[dfa.initial_state]

    # Step 2: Write equations for each state
    equations = []
    for state in dfa.states:
        R=''
        for symbol in list(dfa.input_symbols):
            if(symbol in dfa.transitions[state]):
                for item in dfa.transitions[state][symbol]:
                    R = R+(f'{symbol}.{variables[item]}+' )
        
        # for symbol, next_state in dfa.transitions[state].items():
        #     for i in list(next_state):
        #         R = ''.join(f'{symbol}.{variables[i]}' )
        # R = f'({R[:-1]})'  # Remove the last | symbol
        L = '1' if state in dfa.final_states else '0'
        equations.append(f'{variables[state]}={R}{L}')

    # Step 3: Solve the set of equations
    ####################it has problem
    regex = ''
    while len(equations) > 0:
        # Find an equation with only one variable
        for i, eqn in enumerate(equations):
            if len(re.findall(f'\\b{variables[dfa.initial_state]}\\b', eqn)) == 0 and len(re.findall(f'\\b{variables[list(dfa.final_states)[0]]}\\b', eqn)) == 0 and len(re.findall('[a-z0-9()]+', eqn)) == 1:
                regex += eqn.split('=')[1]
                var_to_remove = variables[dfa.states[i]]
                break
        else:
            raise ValueError("Can't solve equations")

        # Substitute variable in other equations
        equations = [re.sub(f'\\b{var_to_remove}\\b', f'({regex})', eqn) for eqn in equations]
        equations.pop(i)