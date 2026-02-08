import os
from graphviz import Digraph
from analizador_lexico import AnalizadorLexico
from regex_utils import RegexConverter
from estructuras import Node, Position, Cat, calculate_followpos
from generador_automata import thompson, epsilon_closure, move, minimize_dfa, subset_construction

# se define el codigo fuente en una variable
source_code = """
public class PotionBrewer {
    // costo de los ingredientes en monedas de oro
    private static final double HERB_PRICE = 5.50;
    private static final int MUSHROOM_PRICE = 3;
    private String brewerName;
    private double goldCoins;
    private int potionsBrewed;

    public PotionBrewer(String name, double startingGold) {
        this.brewerName = name;
        this.goldCoins = startingGold;
        this.potionsBrewed = 0;
    }

    public static void main(String[] args) {
        PotionBrewer wizard = new PotionBrewer("Gandalf, the Wise", 100.0);
        String[] ingredients = {"Mandrake Root", "Dragon Scale", "Phoenix Feather"};

        wizard.brewHealthPotion(3, 2);
        wizard.brewHealthPotion(5, 4);

        wizard.printStatus();
    }

    /* crea una pocion si tenemos suficiente oro */
    public void brewHealthPotion(int herbCount, int mushroomCount) {
        double totalCost = (herbCount * HERB_PRICE) + (mushroomCount * MUSHROOM_PRICE);
        if (totalCost <= this.goldCoins) {
            this.goldCoins -= totalCost;
            this.potionsBrewed++;
            System.out.println("Success! Potion brewed for " + totalCost + " gold.");
        } else {
            System.out.println("Not enough gold! Need: " + totalCost);
        }
    }

    // imprime el estado actual del creador de pociones
    public void printStatus() {
        System.out.println("=== Brewer Status ===");
        System.out.println("Name: " + this.brewerName);
        System.out.println("Gold remaining: " + this.goldCoins);
        System.out.println("Potions brewed: " + this.potionsBrewed);
    }
}
"""

if __name__ == "__main__":

    # tokenizacion
    # se muestran solo palabras clave y operadores
    print("\nTOKENIZACIÓN\n")

    lexer = AnalizadorLexico(source_code)
    tokens = []

    while True:
        t = lexer.siguiente_token()
        if t is None:
            break
        tokens.append(t)
        if t.tipo in {"KEYWORD", "OPERATOR"}:
            print(t)

    # analisis de lexema
    # verifica si el lexema ingresado es una palabra clave
    lexema = input("\nLexema (keyword) a analizar: ")

    es_keyword = any(
        tok.tipo == "KEYWORD" and tok.valor == lexema
        for tok in tokens
    )

    if not es_keyword:
        print(f"\n'{lexema}' No aparece como KEYWORD en el código.")
        print("→ RECHAZADO")
        exit()

    # conversion de regex a automata
    # se genera el directrio de salida y se crean graficos
    out_dir = lexema
    os.makedirs(out_dir, exist_ok=True)

    regex = " . ".join(['L' for _ in lexema]) + " . #"
    postfix = RegexConverter.shunting_yard(regex)

    # construccion del arbol
    stack, pos, cid = [], 1, 1
    nodes_list = []

    for c in postfix:
        if c in ['L', '#']:
            node = Position(c, pos)
            nodes_list.append(node)
            stack.append(node)
            pos += 1
        elif c == '.':
            b, a = stack.pop(), stack.pop()
            stack.append(Cat(a, b, cid))
            cid += 1
    root = stack.pop()

    # calculo de followpos
    # posiciones siguientes
    # determina que nodos pueden seguir a otros
    followpos_table = {n.pos: set() for n in nodes_list}

    calculate_followpos(root, followpos_table)

    # impresion de tablas de resultado
    
    # tabla de posiciones
    print("\n" + "="*40)
    print("      TABLA DE POSICIONES      ")
    print("="*40)
    print(f"{'Node':<5} | {'Symbol':<8} | {'Nullable':<10} | {'Firstpos':<15} | {'Lastpos':<15}")
    print("-" * 65)
    for n in nodes_list:
        print(f"{n.pos:<5} | {n.symbol:<8} | {str(n.nullable):<10} | {str(sorted(n.firstpos)):<15} | {str(sorted(n.lastpos)):<15}")

    # tabla de followpos
    print("\n" + "="*40)
    print("      TABLA DE FOLLOWPOS      ")
    print("="*40)
    print(f"{'Node':<5} | {'Symbol':<8} | {'Followpos':<20}")
    print("-" * 40)
    for n in nodes_list:
        fp = sorted(followpos_table[n.pos])
        print(f"{n.pos:<5} | {n.symbol:<8} | {str(fp):<20}")
    print("="*40 + "\n")

    # generar grafico del arbol
    dot = Digraph()
    def walk(n):
        dot.node(
            n.id,
            f"{n.id}\n"
            f"nullable: {n.nullable}\n"
            f"firstpos: {sorted(n.firstpos)}\n"
            f"lastpos: {sorted(n.lastpos)}"
        )
        if isinstance(n, Cat):
            walk(n.left)
            walk(n.right)
            dot.edge(n.id, n.left.id)
            dot.edge(n.id, n.right.id)
    walk(root)
    dot.render(os.path.join(out_dir, f"arbol_{lexema}"))

    # algoritmo de thompson
    postfix_thompson = ('L' * len(lexema)) + ('.' * (len(lexema) - 1))
    nfa = thompson(postfix_thompson)

    # construccion de subconjuntos
    # afd
    dfa_states, trans, finals = subset_construction(nfa)

    # generar grafico del afd
    dot = Digraph()
    dot.attr(rankdir="LR")
    for s in dfa_states.values():
        dot.node(s, shape="doublecircle" if s in finals else "circle")
    dot.node("start", shape="point")
    dot.edge("start", "S0")
    for (o, a), d in trans.items():
        dot.edge(o, d, label=a)
    dot.render(os.path.join(out_dir, f"afd_{lexema}"))

    # minimizacion del automata
    minP = minimize_dfa(
        states=dfa_states.values(),
        alphabet={'L'},
        start="S0",
        finals=finals,
        trans=trans
    )

    # generar grafico del afd minimizado
    dot = Digraph()
    dot.attr(rankdir="LR")
    mapping = {}
    for i, g in enumerate(minP):
        name = f"Q{i}"
        for s in g:
            mapping[s] = name
        dot.node(name, str(g), shape="doublecircle" if g & finals else "circle")
    dot.node("start", shape="point")
    dot.edge("start", mapping["S0"])
    for (o, a), d in trans.items():
        dot.edge(mapping[o], mapping[d], label=a)
    dot.render(os.path.join(out_dir, f"afd_min_{lexema}"))

    print(f"\nArchivos generados en '{lexema}/'")
