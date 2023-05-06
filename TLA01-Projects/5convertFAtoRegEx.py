



def fa_to_regex(fa):
    # Step 1: Assign variables to each state
    variables = {s: f'x_{i}' for i, s in enumerate(fa.states)}
    X = variables[fa.start_state]

    # Step 2: Write equations for each state
    equations = []
    for state in fa.states:
        R = ''.join(f'{variables[next_state]}|' for symbol, next_state in fa.transitions[state].items())
        R = f'({R[:-1]})'  # Remove the last | symbol
        L = '1' if state in fa.final_states else '0'
        equations.append(f'{variables[state]}={R}{variables[state]}+{L}')

    # Step 3: Solve the set of equations
    regex = ''
    while len(equations) > 0:
        # Find an equation with only one variable
        for i, eqn in enumerate(equations):
            if len(re.findall(f'\\b{variables[fa.start_state]}\\b', eqn)) == 0 and len(re.findall(f'\\b{variables[fa.final_states[0]]}\\b', eqn)) == 0 and len(re.findall('[a-z0-9()]+', eqn)) == 1:
                regex += eqn.split('=')[1]
                var_to_remove = variables[fa.states[i]]
                break
        else:
            raise ValueError("Can't solve equations")

        # Substitute variable in other equations
        equations = [re.sub(f'\\b{var_to_remove}\\b', f'({regex})', eqn) for eqn in equations]
        equations.pop(i)

    return regex