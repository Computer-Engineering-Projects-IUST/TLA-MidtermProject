from frozendict import frozendict
from typing import FrozenSet, List, Tuple
import sys
from visualize import visualize
from FA.dfa import VisualDFA
from utils import read_fa, create_standard_fa

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
    for state in states:
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
            groups.append({state})

    # Step 3: Remove unreachable states
    reachable_states = set()
    visited_states = set()
    def dfs(state):
        visited_states.add(state)
        reachable_states.add(state)
        for symbol in symbols:
            if state not in transitions or symbol not in transitions[state]:
                continue
            next_state = transitions[state][symbol]
            if next_state not in visited_states:
                dfs(next_state)
    dfs(start_state)
    states = list(reachable_states)
    final_states = frozenset(state for state in final_states if state in reachable_states)
    transitions = frozendict((s, frozendict((c, t) for c, t in ts.items() if t in reachable_states)) for s, ts in transitions.items() if s in reachable_states)

    # Step 4: Create new DFA with simplified states
    new_states, new_final_states = set(), set()
    for group in groups:
        if any(state in reachable_states for state in group):
            new_state = '_'.join(sorted(list(group)))
            new_states.add(new_state)
            if any(state in final_states for state in group):
                new_final_states.add(new_state)

    # Step 5: Create new transitions
    new_transitions = {}
    for group in groups:
        if any(state in reachable_states for state in group):
            group_states = [state for state in group if state in reachable_states]
            for symbol in symbols:
                next_state = new_transitions.get(('_'.join(sorted(group_states)), symbol), '_error')
                for new_group in groups:
                    if any(state in new_group for state in group_states) and all(state in reachable_states for state in new_group):
                        new_transitions[('_'.join(sorted(group_states)), symbol)] = '_'.join(sorted(list(new_group)))
                        break
                else:
                    new_transitions[('_'.join(sorted(group_states)), symbol)] = '_error'

    # Step 6: Create new start state
    new_start_state = start_state
    for group in groups:
        if start_state in group and any(state in reachable_states for state in group):
            new_start_state = '_'.join(sorted(list(group)))
            break

    # Step 7: Create new DFA and return
    new_transitions_dict = {}
    for state in new_states:
        new_transitions_dict[state] = frozendict((symbol, new_transitions.get((state, symbol), '_error')) for symbol in symbols)
    new_transitions = frozendict(new_transitions_dict)
    new_dfa = (sorted(new_states), new_transitions, new_final_states)

    return new_dfa

def is_no_more_grouping_possible(states: List[str], symbols: List[str], transitions: frozendict, final_states: FrozenSet[str]) -> bool:
    distinguishable = set()
    for state1 in states:
        for state2 in states:
            if state1 != state2 and (state1 not in final_states) != (state2 not in final_states):
                distinguishable.add((state1, state2))

    while distinguishable:
        (state1, state2) = distinguishable.pop()
        for symbol in symbols:
            next_state1 = transitions[state1][symbol]
            next_state2 = transitions[state2][symbol]
            if (next_state1, next_state2) in distinguishable:
                continue
            elif (next_state1, next_state2) not in distinguishable:
                distinguishable.add((next_state1, next_state2))
            if (next_state1 in final_states) != (next_state2 in final_states):
                return False

    return True


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

# while is_no_more_grouping_possible(states, symbols, Trans, final_states) == False:
#         print('New DFA:')
#         NewDFA = simplify_dfa(states, symbols, Trans, start_state, final_states)
#         print(NewDFA)
#         states = NewDFA[0]
#         Trans = NewDFA[1]
#         final_states = NewDFA[2]


print('New DFA:')
NewDFA = simplify_dfa(states, symbols, Trans, start_state, final_states)
print(NewDFA)
states = NewDFA[0]
print(states)
Trans = NewDFA[1]
print(Trans)
final_states = NewDFA[2]
print(final_states)
NewDFA = simplify_dfa(states, symbols, Trans, start_state, final_states)
print(NewDFA)

# NewDFA = simplify_dfa(states, symbols, Trans, start_state, final_states)
# print(type(NewDFA))

# # Remove all unreachable states from the DFA
# reachable_states = dfa.find_reachable_states()
# #print(reachable_states)
# final_states = dfa.final_states.intersection(reachable_states)
# #print(final_states)
# non_final_states = reachable_states - final_states
# #print(non_final_states)
