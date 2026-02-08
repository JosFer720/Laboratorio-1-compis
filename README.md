# Laboratorio 1 - Compiladores

## Video Explicativo



[Ver Explicación del Código](Explicacion%20del%20codigo.mp4)

> **Nota:** Intenté subir el video a YouTube, pero debido a que dura más de 15 minutos, no me permitió hacerlo. Por eso se incluye el archivo de video directamente en este repositorio.




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

## ¿Qué se necesita?

*   Tener Python instalado.
*   Instalar la librería para graficar: `pip install graphviz`.
*   Tener el programa Graphviz instalado en la computadora.

## ¿Cómo se usa?

Solo corre `main.py` en la terminal:

```bash
python main.py
```

El programa pedirá una palabra. Escríbela y dale Enter. Luego, busca en la carpeta con el nombre de tu palabra los diagramas que generó.