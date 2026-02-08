import os
from graphviz import Digraph

# construccion de thompson
# convierte la expresion regular en un automata finito no determinista
class NFAState:
    def __init__(self):
        self.trans = {}
        self.epsilon = []

class NFAFragment:
    def __init__(self, start, accepts):
        self.start = start
        self.accepts = accepts

def thompson(postfix):
    stack = []

    for c in postfix:
        if c == 'L':
            s0 = NFAState()
            s1 = NFAState()
            s0.trans.setdefault('L', []).append(s1)
            stack.append(NFAFragment(s0, [s1]))

        elif c == '.':
            f2 = stack.pop()
            f1 = stack.pop()
            for a in f1.accepts:
                a.epsilon.append(f2.start)
            stack.append(NFAFragment(f1.start, f2.accepts))

    return stack.pop()

# afn a afd
# construccion de subconjuntos
# convierte el automata no determinista a uno determinista
def epsilon_closure(states):
    stack = list(states)
    closure = set(states)
    while stack:
        s = stack.pop()
        for t in s.epsilon:
            if t not in closure:
                closure.add(t)
                stack.append(t)
    return closure

def move(states, symbol):
    result = set()
    for s in states:
        result.update(s.trans.get(symbol, []))
    return result

# minimizacion de afd
# particion de estados
# reduce el numero de estados del automata determinista
def minimize_dfa(states, alphabet, start, finals, trans):
    P = [set(finals), set(states) - set(finals)]
    P = [p for p in P if p]

    changed = True
    while changed:
        changed = False
        newP = []

        for group in P:
            buckets = {}
            for s in group:
                sig = tuple(
                    next((i for i, g in enumerate(P)
                          if trans.get((s, a)) in g), None)
                    for a in alphabet
                )
                buckets.setdefault(sig, set()).add(s)

            if len(buckets) > 1:
                changed = True
                newP.extend(buckets.values())
            else:
                newP.append(group)

        P = newP

    return P

def subset_construction(nfa):
    start = frozenset(epsilon_closure([nfa.start]))
    dfa_states = {start: "S0"}
    finals = set()
    trans = {}
    queue = [start]
    idx = 1

    while queue:
        state = queue.pop(0)
        name = dfa_states[state]

        if any(s in nfa.accepts for s in state):
            finals.add(name)

        target = frozenset(epsilon_closure(move(state, 'L')))
        if target:
            if target not in dfa_states:
                dfa_states[target] = f"S{idx}"
                idx += 1
                queue.append(target)
            trans[(name, 'L')] = dfa_states[target]
            
    return dfa_states, trans, finals
