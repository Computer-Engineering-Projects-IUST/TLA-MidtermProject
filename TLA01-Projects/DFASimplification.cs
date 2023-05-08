using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using TLA_Library;
namespace Phase2
{
    public class DFAStateReduction
    {
        //DFS recursive function 
        static void DFS_Visit_Recursive(DFA dfa, NewState n, List<NewState> dfs_visit)
        {
            n.Visit = true;
            for (int i = 0; i < dfa.InputSymbols.inputs.Count; i++)
                if (n.transitions[dfa.InputSymbols.inputs[i]].Visit == false)
                {
                    dfs_visit.Add(n.transitions[dfa.InputSymbols.inputs[i]]);
                    DFS_Visit_Recursive(dfa, n.transitions[dfa.InputSymbols.inputs[i]], dfs_visit);
                }
        }
        public static DFA SimplificationDFA(DFA dfa)
        {

            List<NewState> dfs_visit = new List<NewState>();
            dfs_visit.Add(dfa.InitialState);

            //First we go through vertexes by DFS to define non-reachable states
            DFS_Visit_Recursive(dfa, dfa.InitialState, dfs_visit);
            dfa.States = dfs_visit;
            List<NewState> new_final_state = new List<NewState>();
            //Remove non-reachable states from DFA
            for (int i = 0; i < dfa.FinalStates.Count; i++)
            {
                if (dfs_visit.Contains(dfa.FinalStates[i]))
                    new_final_state.Add(dfa.FinalStates[i]);
            }
            dfa.FinalStates = new_final_state;
            
            //Construct zero_equivalence by seperating final and non-final states
            List<NewState> final = new List<NewState>();
            List<NewState> nonfinal  = new List<NewState>();
            for (int i = 0; i < dfa.States.Count; i++)
            {
                if (dfa.FinalStates.Contains(dfa.States[i]))
                    final.Add(dfa.States[i]);
                else
                    nonfinal.Add(dfa.States[i]);
            }

            //Define list for k_equivalence to reach k+1_equivalence(next equivalence table)
            List<List<NewState>> equal_state_k = new List<List<NewState>>();
            equal_state_k.Add(final);
            equal_state_k.Add(nonfinal);

            //Do this while loop till k+1_equivalence table is as same as k_equivalence
            while (true)
            {
                //Create states list as k+1_equivalence table   
                List<List<NewState>> equal_state_k_next = new List<List<NewState>>();
                for (int i = 0; i < equal_state_k.Count; i++)
                {
                    //For states that were equal in k_equivalence table we check equivalency in k+1_equivalence table
                    //Create a dictionary for seperating states that are in the same list in k_equivalence table 
                    Dictionary<string, List<NewState>> product_equal_states = new Dictionary<string, List<NewState>>();
                    //for states that were equal in k_equivalence table do this for loop
                    for (int j = 0; j < equal_state_k[i].Count; j++)
                    {
                        string x = "";
                        //Check whether we have 2 input symbols 
                        if (dfa.InputSymbols.inputs.Count == 2)
                        {
                            //Check whether for each input symbol which eqivalence list we reach + add first state of the previous list to x(string)
                            for (int k = 0; k < equal_state_k.Count; k++)
                            {
                                if (equal_state_k[k].Contains(equal_state_k[i][j].transitions[dfa.InputSymbols.inputs[0]]))
                                {
                                    x += equal_state_k[k][0].state_ID;
                                    break;
                                }
                            }
                            for (int k = 0; k < equal_state_k.Count; k++)
                            {
                                if (equal_state_k[k].Contains(equal_state_k[i][j].transitions[dfa.InputSymbols.inputs[1]]))
                                {
                                    x += equal_state_k[k][0].state_ID;
                                    break;
                                }
                            }
                        }
                        else if (dfa.InputSymbols.inputs.Count == 1)
                        {
                            //Check whether we have only 1 input symbol 
                            //Repeat previous operations for one input symbol
                            for (int k = 0; k < equal_state_k.Count; k++)
                            {
                                if (equal_state_k[k].Contains(equal_state_k[i][j].transitions[dfa.InputSymbols.inputs[0]]))
                                {
                                    x += equal_state_k[k][0].state_ID;
                                    break;
                                }
                            }
                        }
                        //if two states go through same euivalence list in k_equivalence table they have the same euivalence list in k+1_equivalence 
                        if (product_equal_states.ContainsKey(x))
                            product_equal_states[x].Add(equal_state_k[i][j]);
                        else
                        {
                            List<NewState> temp = new List<NewState>();
                            temp.Add(equal_state_k[i][j]);
                            product_equal_states.Add(x, temp);
                        }
                    }
                    //Construct k+1_equivalence table
                    foreach (var tmp in product_equal_states.Values)
                        equal_state_k_next.Add(tmp);

                }
                //Chekck whether k+1_equivalence and k_equivalence are the same if yes --> quit while loop if no --> go through next equivalenc table
                if (equal_state_k_next.Count == equal_state_k.Count)
                    break;

                equal_state_k = equal_state_k_next;
            }
            //For each equivalency list in k_equivalence table order the states by state ID
            for (int i = 0; i < equal_state_k.Count; i++)
                equal_state_k[i] = equal_state_k[i].OrderBy(x => x.state_ID.Replace("q", "")).ToList();

            //For every list in k_equivalence table order the states in each list by the first state of the list
            equal_state_k = equal_state_k.OrderBy(x => x[0].state_ID.Replace("q", "")).ToList();
            
            //Construct new DFA by the result of equivalence table
            List<NewState> new_dfa_states = new List<NewState>();
            for (int i = 0; i < equal_state_k.Count; i++)
            {
                string x = "";
                for (int j = 0; j < equal_state_k[i].Count; j++)
                    x += equal_state_k[i][j].state_ID;

                new_dfa_states.Add(new NewState(x));
            }
            ////////////////////////////////////////////////////
            List<NewState> new_dfa_final_states = new List<NewState>();
            for (int i = 0; i < equal_state_k.Count; i++)
            {
                if (dfa.FinalStates.Contains(equal_state_k[i][0]))
                    new_dfa_final_states.Add(new_dfa_states[i]);
            }
            NewState new_dfa_initial_state = null;
            for (int i = 0; i < equal_state_k.Count; i++)
            {
                if (equal_state_k[i].Contains(dfa.InitialState))
                {
                    new_dfa_initial_state = new_dfa_states[i];
                    break;
                }
            }
            DFA new_dfa = new DFA(0, new_dfa_states, dfa.InputSymbols, new_dfa_initial_state, new_dfa_final_states);
            if (dfa.InputSymbols.inputs.Count == 2)
            {
                for (int i = 0; i < equal_state_k.Count; i++)
                {
                    for (int k = 0; k < equal_state_k.Count; k++)
                    {
                        if (equal_state_k[k].Contains(equal_state_k[i][0].transitions[dfa.InputSymbols.inputs[0]]))
                        {
                            new_dfa_states[i].transitions[dfa.InputSymbols.inputs[0]] = new_dfa_states[k];
                            break;
                        }
                    }
                    for (int k = 0; k < equal_state_k.Count; k++)
                    {
                        if (equal_state_k[k].Contains(equal_state_k[i][0].transitions[dfa.InputSymbols.inputs[1]]))
                        {
                            new_dfa_states[i].transitions[dfa.InputSymbols.inputs[1]] = new_dfa_states[k];
                            break;
                        }
                    }
                }
            }
            else if (dfa.InputSymbols.inputs.Count == 1)
            {
                //Check whether we have only 1 input symbol 
                for (int i = 0; i < equal_state_k.Count; i++)
                {
                    for (int k = 0; k < equal_state_k.Count; k++)
                    {
                        if (equal_state_k[k].Contains(equal_state_k[i][0].transitions[dfa.InputSymbols.inputs[0]]))
                        {
                            new_dfa_states[i].transitions[dfa.InputSymbols.inputs[0]] = new_dfa_states[k];
                            break;
                        }
                    }
                }
            }
            return new_dfa;
        }
        public static void Main(string[] args)
        {
            var json_text = File.ReadAllText(@"../..");
            DFA dfa = ConvertJsonToFA.ConvertJsonToDFA(json_text);
            DFA result = SimplificationDFA(dfa);
            ConvertFAToJson.ConvertDFAToJson(result, @"../..");
        }
    }
}