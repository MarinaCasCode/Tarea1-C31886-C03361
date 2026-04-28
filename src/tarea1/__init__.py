# -*- coding: utf-8 -*-
"""
Programa principal para utilizar el modelo Función.

Programado por Braulio José Solano Rojas.
"""

import sys

from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from tarea1.funcion import Funcion
from tarea1.listaordenadadinamica import ListaOrdenadaDinámica
from tarea1.listaordenadaestatica import ListaOrdenadaEstática
from tarea1.tablahashabierta import TablaHashAbierta
console = Console()


# =====================
# Utilidades de pantalla
# =====================


def panel_contenido(
    texto: str, *, titulo: str = "Función", width: int | None = None
) -> None:
    """Imprime un Panel con doble línea y fondo azul."""
    console.clear()
    if width is None:
        # Mantener proporción similar a 80 columnas del original
        width = min(80, max(40, console.size.width - 4))
    panel = Panel(
        Align.left(texto),
        title=titulo,
        title_align="center",
        padding=(1, 4),
        box=box.DOUBLE,
        width=width,
        style="white on blue",
    )
    console.print(panel, justify="left")


def pausa(msg: str = "Pulse [bold]Enter[/] para continuar…") -> None:
    Prompt.ask(msg, default="", show_default=False)


def leer_hilera(pregunta: str) -> str:
    """Lee una hilera similar a TDato (máx. 20 chars)."""
    s = Prompt.ask(pregunta).strip()
    return s[:20]


# =====================
# Lectura de una tecla (sin Enter)
# =====================


def leer_tecla(validos: str) -> str:
    """Lee una sola tecla y la devuelve sin requerir Enter.

    - En Windows usa `msvcrt.getwch()`.
    - En Unix usa `termios` + `tty` en modo raw.
    Ignora teclas fuera de `validos`.
    """
    try:
        import msvcrt  # type: ignore
    except Exception:
        msvcrt = None  # type: ignore

    if msvcrt is not None:  # Windows
        while True:
            ch = msvcrt.getwch()
            # Descartar prefijos de teclas especiales (setas, F1, etc.)
            if ch in ("\x00", "\xe0"):
                _ = msvcrt.getwch()
                continue
            if ch in validos:
                console.print(ch, end="")  # eco visual como en Pascal
                return ch
    else:  # Unix
        import termios
        import tty

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch in validos:
                    console.print(ch, end="")
                    return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


# =====================
# Operaciones de menú
# =====================


def agregar(funcion: Funcion) -> None:
    texto = "Digite la llave que desea agregar:"
    panel_contenido(texto)
    llave = leer_hilera("")
    texto = "Digite su valor:"
    panel_contenido(texto)
    valor = leer_hilera("")
    funcion.asigne(llave, valor)
    console.print("[green]Relación asignada.[/]")
    pausa()


def borrar(funcion: Funcion) -> None:
    texto = "Digite la llave que desea borrar:"
    panel_contenido(texto)
    llave = leer_hilera("")
    funcion.elimine(llave)
    console.print("[red]La relación fue eliminada.[/]")
    pausa()


def existencia(funcion: Funcion) -> None:
    texto = "Digite la llave que desea buscar:"
    panel_contenido(texto)
    llave = leer_hilera("")
    valor = funcion.obtenga(llave)
    if valor is not None:
        console.print(f"[green]La llave existe. Su valor es {valor}[/]")
    else:
        console.print("[red]La llave NO existe.[/]")
    pausa()


def imprimir(funcion: Funcion) -> None:
    """
    Función que imprime un objeto de clase Funcion.

    Args:
        funcion (Funcion): Implementación abstracta del modelo Función.
    """    
    panel_contenido("Imprimir la funcion")
    funcion.imprima()
    pausa()


def limpiar(funcion: Funcion) -> None:
    funcion.limpie()
    panel_contenido("Función limpia, sin relaciones.")
    pausa()


# ============
# Menúes
# ============

def render_menu_etapa() -> None:
    cuerpo = (
        "\n"  # deja un margen superior dentro del panel
        "            Etapa\n\n"
        "[1] Menú Función (entregas 1 y 2)\n"
        "[2] Pruebas de rendimiento ([italic]benchmarking[/])\n"
        "[3] [red]Salir del programa[/]\n\n"
        "Digite una opción [_]"
    )
    panel_contenido(cuerpo)


def render_menu_clase() -> None:
    """_summary_
    """    
    cuerpo = (
        "\n"  # deja un margen superior dentro del panel
        "            Clase Funcion\n\n"
        "[1] ListaOrdenadaDinámica\n"
        "[2] ListaOrdenadaEstática\n"
        "[3] TablaHashAbierta\n"
        "[4] ABBPunteros\n"
        "[5] ABBVectorHeap\n"
        "[6] TriePunteros\n"
        "[7] TrieArreglos\n\n"
        "[8] [red]Salir del programa[/]\n\n"
        "Digite una opción [_]"
    )
    panel_contenido(cuerpo)


def render_menu_funcion() -> None:
    cuerpo = (
        "\n"  # deja un margen superior dentro del panel
        "            Funcion\n\n"
        "[1] Agregar una relación a Funcion\n"
        "[2] Borrar una relación de Funcion\n"
        "[3] Existencia de una relación en Funcion\n"
        "[4] Imprimir el objeto de clase Funcion\n"
        "[5] Limpiar el objeto de clase Funcion\n"
        "[6] Salir\n\n"
        "Digite una opción [_]"
    )
    panel_contenido(cuerpo)


def menu_etapa() -> str:
    try:
        while True:
            render_menu_etapa()
            # leer una sola tecla válida y eco inmediato
            return leer_tecla("123")
    except BaseException:
        raise ValueError("No se pudo devolver una opción.")


def menu_clase() -> Funcion:
    try:
        while True:
            render_menu_clase()
            # leer una sola tecla válida y eco inmediato
            opcion = leer_tecla("1234567")
            match opcion:
                case "1":
                    return ListaOrdenadaDinámica()
                case "2":
                    return ListaOrdenadaEstática(100)
                case "3":
                    return TablaHashAbierta()
                case "4":
                    pass
                case "5":
                    pass
                case "6":
                    pass
                case "7":
                    pass
    except BaseException:
        raise ValueError("No se pudo instanciar una clase Funcion.")


def menu_funcion(funcion: Funcion) -> None:
    try:
        while True:
            render_menu_funcion()
            # leer una sola tecla válida y eco inmediato
            opcion = leer_tecla("123456")
            # pequeña pausa visual como en Pascal
            # (no Delay, pero el eco ya se ve)
            match opcion:
                case "1":
                    agregar(funcion)
                case "2":
                    borrar(funcion)
                case "3":
                    existencia(funcion)
                case "4":
                    imprimir(funcion)
                case "5":
                    limpiar(funcion)
                case "6":
                    console.clear()
                    break
    finally:
        del funcion


def main() -> None:
    opcion = menu_etapa()
    match opcion:
        case "1":
            funcion = menu_clase()
            menu_funcion(funcion)
        case "2":
            pass


if __name__ == "__main__":
    main()