import sys
from visualize import visualize
from FA.dfa import VisualDFA
from utils import read_fa, create_standard_fa

if __name__ == '__main__':
    """ the main function for visualize the FA"""
    args = sys.argv[1:]
    #json_path = args[0]   # the relative path of the json file containing the dfa or nfa in the desired format
    json_path = "samples/phase2-sample/in/input1.json"#args[0]  
    try:
            read_fa(json_path)
            fa = create_standard_fa(0)
            dfa = VisualDFA(fa)
    except Exception as ex:
        raise Exception("The input file is neither DFA nor NFA\nCheck whether you "
                            "mentioned a correct file or its in the correct standard format")\
            from ex
    

    # # Remove all unreachable states from the DFA
    # reachable_states = find_reachable_states(dfa)
    # accepting_states = dfa.accepting_states.intersection(reachable_states)
    # non_accepting_states = reachable_states - accepting_states
    
    # # Initialize a table with all pairs of states
    # table = {}
    # for i, state_i in enumerate(non_accepting_states):
    #     for j, state_j in enumerate(accepting_states):
    #         table[(state_i, state_j)] = True
    
    # # Mark all pairs that lead to different states as distinguished
    # distinguished = {}
    # for state_i in non_accepting_states:
    #     for state_j in accepting_states:
    #         if dfa.transition(state_i, '0') != dfa.transition(state_j, '0'):
    #             distinguished[(state_i, state_j)] = True
    #         else:
    #             distinguished[(state_i, state_j)] = False
                
    # # Repeat until no new pairs are marked as distinguished
    # while True:
    #     new_distinguished = {}
    #     for (state_i, state_j), is_distinguished in distinguished.items():
    #         if is_distinguished:
    #             continue
    #         for symbol in dfa.alphabet:
    #             next_state_i = dfa.transition(state_i, symbol)
    #             next_state_j = dfa.transition(state_j, symbol)
    #             if (next_state_i, next_state_j) in distinguished and distinguished[(next_state_i, next_state_j)]:
    #                 new_distinguished[(state_i, state_j)] = True
    #                 break
    #         else:
    #             new_distinguished[(state_i, state_j)] = False
                
    #     if new_distinguished == distinguished:
    #         break
            
    #     distinguished = new_distinguished
        
    # # Merge all undistinguished pairs of states into a single state
    # equivalence_classes = {}
    # for state in reachable_states:
    #     if state in accepting_states:
    #         equivalence_classes[state] = 'A'
    #     else:
    #         equivalence_classes[state] = 'NA'
            
    # for (state_i, state_j), is_distinguished in distinguished.items():
    #     if not is_distinguished:
    #         equivalence_classes[state_i] += state_j
            
    # new_states = set()
    # for class_label in set(equivalence_classes.values()):
    #     states = [state for state, label in equivalence_classes.items() if label == class_label]
    #     new_state = states[0]
    #     for state in states[1:]:
    #         new_state = merge_states(new_state, state)
    #     new_states.add(new_state)
        
    # # Create the minimized DFA
    # new_dfa = DFA(new_states, dfa.alphabet, dfa.transition, new_states.intersection(dfa.accepting_states), new_states.intersection(dfa.start_states))


