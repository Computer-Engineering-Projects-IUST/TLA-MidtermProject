using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;

class DfaSimplifier
{
    public static (List<string> States, ImmutableDictionary<string, ImmutableDictionary<string, string>> Transitions, ImmutableHashSet<string> FinalStates) SimplifyDfa(
        List<string> states, List<string> symbols, ImmutableDictionary<string, ImmutableDictionary<string, string>> transitions, string startState, ImmutableHashSet<string> finalStates)
    {
        // Step 1: Identify indistinguishable states
        var distinguishable = new HashSet<(string, string)>();
        for (int i = 0; i < states.Count; i++)
        {
            for (int j = i + 1; j < states.Count; j++)
            {
                if ((finalStates.Contains(states[i]) && !finalStates.Contains(states[j])) || (!finalStates.Contains(states[i]) && finalStates.Contains(states[j])))
                {
                    distinguishable.Add((states[i], states[j]));
                }
            }
        }
        bool changed;
        do
        {
            changed = false;
            foreach (var pair in distinguishable.ToList())
            {
                foreach (var symbol in symbols)
                {
                    var next1 = transitions[pair.Item1][symbol];
                    var next2 = transitions[pair.Item2][symbol];
                    if (distinguishable.Contains((next1, next2)) || distinguishable.Contains((next2, next1)))
                    {
                        distinguishable.Remove(pair);
                        changed = true;
                        break;
                    }
                }
            }
        } while (changed);

        // Step 2: Group states into equivalence classes
        var groups = states.Select(s => new HashSet<string> { s }).ToList();
        foreach (var pair in distinguishable)
        {
            var group1 = groups.FirstOrDefault(g => g.Contains(pair.Item1));
            var group2 = groups.FirstOrDefault(g => g.Contains(pair.Item2));
            if (group1 != group2)
            {
                group1.UnionWith(group2);
                groups.Remove(group2);
            }
        }

        // Step 3: Remove unreachable states
        var reachableStates = new HashSet<string>();
        var visitedStates = new HashSet<string>();
        void Dfs(string state)
        {
            visitedStates.Add(state);
            reachableStates.Add(state);
            foreach (var symbol in symbols)
            {
                if (transitions.TryGetValue(state, out var transitionsForState) && transitionsForState.TryGetValue(symbol, out var nextState))
                {
                    if (!visitedStates.Contains(nextState))
                    {
                        Dfs(nextState);
                    }
                }
            }
        }
        Dfs(startState);
        states = reachableStates.ToList();
        finalStates = finalStates.Intersect(reachableStates).ToImmutableHashSet();
        transitions = transitions
            .Where(kvp => reachableStates.Contains(kvp.Key))
            .ToImmutableDictionary(kvp => kvp.Key, kvp => kvp.Value.Where(kv => reachableStates.Contains(kv.Value)).ToImmutableDictionary());

        // Step 4: Construct new DFA
        var newTransitions = new Dictionary<string, Dictionary<string, string>>();
        foreach (var group in groups)
        {
            var representative = group.First();
            newTransitions[representative] = new Dictionary<string, string>();
            foreach (var symbol in symbols)
            {
                var nextState = transitions[representative][symbol];
                var nextGroup = groups.First(g => g.Contains(nextState));
                var representativeOfNextGroup = nextGroup.First();
                newTransitions[representative][symbol] = representativeOfNextGroup;
            }
        }

        return (states, newTransitions.ToImmutableDictionary(), finalStates);
    }
}