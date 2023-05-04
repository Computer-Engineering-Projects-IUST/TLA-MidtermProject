from frozendict import frozendict
from typing import FrozenSet, List, Tuple
import sys
from visualize import visualize
from FA.dfa import VisualDFA
from utils import read_fa, create_standard_fa
from collections import deque

def simplify_dfa(states: List[str], symbols: List[str], transitions: frozendict, start_state: str, final_states: FrozenSet[str]) -> Tuple[List[str], frozendict, FrozenSet[str]]:
    # Step 1: Identify indistinguishable states
    distinguishable = set()
    for state1 in states:
        for state2 in states:
            if state1 != state2 and (state1 not in final_states) != (state2 not in final_states):
                distinguishable.add((state1, state2))
    changed = True
    while changed:
        changed = False
        for (state1, state2) in distinguishable.copy():
            for symbol in symbols:
                next_state1 = transitions[state1][symbol]
                next_state2 = transitions[state2][symbol]
                if (next_state1, next_state2) in distinguishable:
                    distinguishable.remove((state1, state2))
                    changed = True
                    break

    # Step 2: Group states into equivalence classes
    groups = []
    # Group the initial state first
    initial_group = {start_state}
    groups.append(initial_group)
    for state in states:
        if state == start_state:
            continue
        found = False
        for group in groups:
            if state in group:
                found = True
                break
            elif all((state, other) not in distinguishable for other in group):
                group.add(state)
                found = True
                break
        if not found:
            new_group = {state}
            groups.append(new_group)

    # Step 3: Perform reachability analysis to remove unreachable states
    reachable_states = set()
    visited_states = set()
    def dfs(state):
        visited_states.add(state)
        reachable_states.add(state)
        for symbol in symbols:
            if state in transitions:
                next_state = transitions[state][symbol]
                if next_state not in visited_states:
                    dfs(next_state)
    dfs(start_state)
    unreachable_states = set(states) - reachable_states
    if unreachable_states:
        for state in unreachable_states:
            if state == start_state:
                raise ValueError("Initial state is unreachable.")
            elif state in final_states:
                raise ValueError("Final state is unreachable.")
        states = list(filter(lambda s: s not in unreachable_states, states))
        final_states = frozenset(filter(lambda s: s not in unreachable_states, final_states))
        transitions = frozendict({(s, c): t for (s, c), t in transitions.items() if s not in unreachable_states})

    # Step 4: Construct new DFA with simplified states
    new_states = []
    new_final_states = set()
    new_transitions = {}
    for group in groups:
        state = next(iter(group))
        new_states.append(state)
        if state in final_states:
            new_final_states.add(state)
        for symbol in symbols:
            next_state = transitions[state][symbol]
            for other_group in groups:
                if next_state in other_group:
                    new_transitions[(state, symbol)] = next(iter(other_group))
                    break
    new_start_state = next(iter(initial_group))

    return new_states, frozendict(new_transitions), frozenset(new_final_states)

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


# states = list(dfa.states)
# states.sort()
# # print(type(states))
# #print(states)

# symbols = list(dfa.input_symbols)
# symbols.sort()
# #print(symbols)

# start_state = dfa.initial_state
# #print(type(start_state))
# final_states = dfa.final_states
# #print(type(final_states))

# Trans = dfa.transitions
#print (Trans['q0']['0'])


# dfa = DFA(symbols, Trans, final_states, start_states)
#print(transition)

# dfa = DFA()
# print(dfa.states)
# print(dfa.symbols)
# print(dfa.transitions)
# print(dfa.start_state)
# print(dfa.final_states)




# NewDFA = simplify_dfa(dfa)
# print(NewDFA.states)
# print(NewDFA.symbols)
# print(NewDFA.transitions)
# print(NewDFA.start_state)
# print(NewDFA.final_states)

# Define the states and symbols of the DFA
states = ['q0', 'q1', 'q2', 'q3', 'q4']
symbols = ['0', '1']

# Define the transition function as a frozendict of frozendict values
Trans = frozendict({
    'q0': frozendict({'0': 'q1', '1': 'q3'}),
    'q1': frozendict({'0': 'q2', '1': 'q4'}),
    'q2': frozendict({'0': 'q1', '1': 'q4'}),
    'q3': frozendict({'0': 'q2', '1': 'q4'}),
    'q4': frozendict({'0': 'q4', '1': 'q4'})
})

# Define the start state and final states of the DFA
start_state = 'q0'
final_states = {'q4'}

# print('Old DFA:')
# # dfa = DFA(states, symbols, transitions, start_state, final_states)
# print(states)
# print(symbols)
# print(Trans)
# print(start_state)
# print(final_states)


print('New DFA:')
NewDFA = simplify_dfa(states, symbols, Trans, start_state, final_states)
print(NewDFA)


# # Remove all unreachable states from the DFA
# reachable_states = dfa.find_reachable_states()
# #print(reachable_states)
# final_states = dfa.final_states.intersection(reachable_states)
# #print(final_states)
# non_final_states = reachable_states - final_states
# #print(non_final_states)