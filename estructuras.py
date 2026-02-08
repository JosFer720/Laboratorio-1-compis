# arbol sintactico
# define clases para los nodos del arbol de sintaxis abstracta
class Node:
    def __init__(self):
        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()
        self.id = None

class Position(Node):
    def __init__(self, symbol, pos):
        super().__init__()
        self.symbol = symbol
        self.pos = pos
        self.firstpos = {pos}
        self.lastpos = {pos}
        self.nullable = False
        self.id = f"P{pos}"

class Cat(Node):
    def __init__(self, left, right, cid):
        super().__init__()
        self.left = left
        self.right = right
        self.nullable = left.nullable and right.nullable
        self.firstpos = left.firstpos | right.firstpos if left.nullable else left.firstpos
        self.lastpos = left.lastpos | right.lastpos if right.nullable else right.lastpos
        self.id = f"C{cid}"

def calculate_followpos(n, followpos_table):
    if isinstance(n, Cat):
        for i in n.left.lastpos:
            followpos_table[i].update(n.right.firstpos)
        calculate_followpos(n.left, followpos_table)
        calculate_followpos(n.right, followpos_table)
