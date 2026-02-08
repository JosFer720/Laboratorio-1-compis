# Laboratorio 1 - Compiladores

1.  **`regex_utils.py`**:
    *   Ordena las operaciones, como poner los operadores al final.

2.  **`estructuras.py`**:
    *   Define qué es un Nodo, una Posición y una Concatenación.
    *   Calcula cosas como el followpos.

3.  **`generador_automata.py`**:
    *   Thompson: Crea un autómata AFN.
    *   Subconjuntos: Convierte ese autómata en AFD.
    *   Minimización.

4.  **`main.py`**:
    *   Lee el código de ejemplo.
    *   Pide una keyword para analizar.
    *   Manda a hacer los gráficos.

5.  **`analizador_lexico.py`**:
    *   Lee el texto y lo separa en tokens.

## ¿Qué necesito?

*   Tener Python instalado.
*   Instalar la librería para graficar: `pip install graphviz`.
*   Tener el programa Graphviz instalado en la computadora.

## ¿Cómo lo uso?

Solo corre este comando en la terminal:

```bash
python main.py
```

El programa te mostrará lo que encontró y te pedirá una palabra. Escríbela y dale Enter. Luego, busca en la carpeta con el nombre de tu palabra los dibujos que generó.
