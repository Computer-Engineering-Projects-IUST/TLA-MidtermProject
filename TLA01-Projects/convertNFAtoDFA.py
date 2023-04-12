import sys
from visualize import visualize
from FA.dfa import VisualDFA
from FA.nfa import VisualNFA
from utils import read_fa, create_standard_fa

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



# def nfa_to_dfa(nfa):
    # Step 1: Create an empty set of states for the DFA
    dfa_states = set(set())
    
    # Step 2: Create a new start state for the DFA containing 
    #         epsilon closure of start state of NFA
    #start_state = frozenset()

    tran=list(nfa.transitions)

    if("" in nfa.transitions[nfa.initial_state]):
        start_state=frozenset([nfa.initial_state,list(nfa.transitions[nfa.initial_state][""])[0]])
    else:
        start_state={nfa.initial_state}

    dfa_states|=(start_state)
    # Step 3: Create a queue of states to be processed, starting 
    #         with new start state
    queue = [start_state]

    symbols=list(nfa.input_symbols)
    symbols.sort()
    
    # Step 4: While there are states in queue:
    while queue:
        current_state = queue.pop(0)
        
        # For each input symbol:
        for symbol in symbols:
            # Find set of states reachable from current state on 
            # input symbol by taking epsilon closures and following 
            # transitions
            next_states = set()
            for state in current_state:
                if(symbol in nfa.transitions[state]):
                    temp=list(nfa.transitions[state][symbol])[0]
                    next_states.add(temp)
                    if( "" in nfa.transitions[temp]):
                        next_states.add(list(nfa.transitions[temp][""])[0])

                # next_states |= nfa.transitions.get((state, symbol), set())
                # next_states |= nfa.epsilon_closure(next_states)
                
            
            # If this set is not already in the set of DFA states, add it 
            # to the set and add it to the queue
            if next_states and frozenset(next_states) not in dfa_states:
                dfa_states.add(frozenset(next_states))
                queue.append(frozenset(next_states))
            
            # Add a transition from current state on input symbol to 
            # this new set of states in DFA transition table
            if next_states:
                ############################error :can not add transition
                fa["transitions"][state][key] = eval(fa["transitions"][state][key])
                nfa.add[(current_state, symbol)] = frozenset(next_states)
    
    # Step 5: Mark any sets containing an accepting state of NFA as 
    #         accepting states in DFA
    dfa_final_states=set()
    for state in dfa_states:
        if any(nfa.final_states & state):
            dfa_final_states.add(state)
    
    # return nfa