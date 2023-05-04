import sys
from visualize import visualize
from FA.dfa import VisualDFA
from utils import read_fa, create_standard_fa

class DFA:
        def __init__(self, symbols, transitions, final_states, initial_state):
                self.symbols = symbols
                self.transitions = transitions
                self.final_states = final_states
                self.initial_state = initial_state

        def is_final(self, state):
                return state in self.final_states

        def is_valid_symbol(self, symbol):
                return symbol in self.symbols

        def simulate(self, input_string):
                current_state = self.initial_state
                for symbol in input_string:
                        if not self.is_valid_symbol(symbol):
                                raise ValueError(f"Symbol '{symbol}' not in DFA symbols")
                        current_state = self.transitions[current_state][symbol]
                return self.is_final(current_state)

        def find_reachable_states(self):
                reachable_states = set()
                added_states = set([self.initial_state])
                reachable_states.add(self.initial_state) #####
                while added_states:
                        new_states = set()
                        for state in added_states:
                                for symbol in self.symbols:
                                        next_state = self.transitions[state][symbol]
                                        if next_state not in reachable_states:
                                                new_states.add(next_state)
                        reachable_states.update(new_states)
                        added_states = new_states
                return reachable_states

        def merge_states(self, state1, state2):
                return f"{state1},{state2}"

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


states = list(dfa.states)
states.sort()
# print(type(states))
#print(states)

symbols = list(dfa.input_symbols)
symbols.sort()
#print(symbols)

start_states = dfa.initial_state
#print(InitialState)
final_states = dfa.final_states
#print(FinalStates)

Trans = dfa.transitions
#print (Trans['q0']['0'])


# transition = lambda state, symbol : {
#         ('q0', '0'): 'q1',
#         ('q0', '1'): 'q3',
#         ('q1', '0'): 'q2',
#         ('q1', '1'): 'q4',
#         ('q2', '0'): 'q1',
#         ('q2', '1'): 'q4',
#         ('q3', '0'): 'q2',
#         ('q3', '1'): 'q4',
#         ('q4', '0'): 'q4',
#         ('q4', '1'): 'q4',
# }[(state, symbol)]
# final_states = {'q4'}
# start_states = 'q0'

dfa = DFA(symbols, Trans, final_states, start_states)
#print(transition)



# Remove all unreachable states from the DFA
reachable_states = dfa.find_reachable_states()
#print(reachable_states)
final_states = dfa.final_states.intersection(reachable_states)
#print(final_states)
non_final_states = reachable_states - final_states
#print(non_final_states)


# # Initialize a table with all pairs of states
# table = {}
# for i, state_i in enumerate(non_final_states):
#     for j, state_j in enumerate(final_states):
#         table[(state_i, state_j)] = True
#         print((state_i, state_j))
# print(table)

# table = {}
# for i, state_i in enumerate(states):
#         for j, state_j in enumerate(states):
#                 table[(state_i, state_j)] = True
# #print (table)

# # Mark all pairs that lead to different states as distinguished
# distinguished = {}
# for state_i in states:
#     for state_j in states:
#         if dfa.transitions(state_i, '0') != dfa.transitions(state_j, '0'):
#             distinguished[(state_i, state_j)] = True
#         else:
#             distinguished[(state_i, state_j)] = False
# print(distinguished)

GroupTuple = (0,0)
table = {}
for i, state_i in enumerate(states):
        for j, symb in enumerate(symbols):
                # print (state_i)
                # print (symb)
                # print()
                table[(state_i, symb)] = Trans[state_i][symb]
print (table)


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


