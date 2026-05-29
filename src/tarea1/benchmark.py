"""
benchmark.py - Análisis empírico de tiempos y uso de espacio.
"""
from __future__ import annotations

import csv
import os
import random
import statistics
import string
import sys
import time
import tracemalloc
from contextlib import redirect_stdout
from io import StringIO
from typing import Callable

from tarea1.listaordenadadinamica import ListaOrdenadaDinámica
from tarea1.listaordenadaestatica import ListaOrdenadaEstática
from tarea1.tablahashabierta import TablaHashAbierta
from tarea1.abbpunteros import AbbPunteros
from tarea1.abbvectorheap import ABBVectorHeap
from tarea1.triepunteros import TriePunteros
from tarea1.triearreglos import TrieArreglos

# Constantes

CORRIDAS = 10

# Tamaños requeridos por el enunciado
TAMAÑOS_MAIN = [100, 50_000, 1_000_000]

# La Lista Ordenada hace O(n) por inserción → construir es O(n²).
# Por encima de este límite, los experimentos se omiten y se documenta
# la limitación en el reporte.
LIMITE_LO = 5_000

# El Trie genera hasta O(n × L) nodos Python (L = largo máx. de llave = 20).
# A n=1M eso son ~11M objetos → varios GB de RAM → swap o OOM.
# Por encima de este límite, los experimentos se omiten.
LIMITE_TRIE = 50_000

# La Tabla Hash SIN redistribución acumula todos los pares en m=11 cubetas fijas.
# Cada asigne escanea O(n/m) elementos → construir es O(n²/m) ≈ O(n²).
# Idéntico problema a la Lista Ordenada: impracticable por encima de este límite.
LIMITE_HASH_SR = 50_000

# Tamaños adicionales para mostrar la tendencia de la Lista Ordenada
TAMAÑOS_LO_EXTRA = [1_000, 5_000]

# Límite para ABB con inserciones ordenadas (VectorHeap no se prueba
# con llaves ordenadas por el crecimiento exponencial de sus índices)
LIMITE_ABB_ORDENADO = 500

CHARS_LLAVE = string.ascii_letters + string.digits
CHARS_VALOR = string.ascii_lowercase

CSV_SALIDA = "resultados_benchmark.csv"

# Definición de estructuras
# Cada entrada: etiqueta legible, factory, límite_n (None = sin límite)

ESTRUCTURAS: dict[str, tuple[str, Callable, int | None]] = {
    "lo_din":   ("LO dinámica",               lambda: ListaOrdenadaDinámica(),                   LIMITE_LO),
    "lo_est":   ("LO estática",               lambda: ListaOrdenadaEstática(),                   LIMITE_LO),
    "hash_sr":  ("Tabla Hash (sin redist.)",  lambda: TablaHashAbierta(redistribuir=False),       LIMITE_HASH_SR),
    "hash":     ("Tabla Hash",                lambda: TablaHashAbierta(),                         None),
    "abb_ptr":  ("ABB punteros",              lambda: AbbPunteros(),                              None),
    "abb_vh":   ("ABB vector heap",           lambda: ABBVectorHeap(),                            None),
    "trie_ptr": ("Trie punteros",             lambda: TriePunteros(),                             LIMITE_TRIE),
    "trie_arr": ("Trie arreglos",             lambda: TrieArreglos(),                             LIMITE_TRIE),
}

# 7 parejas requeridas por el enunciado
PAREJAS: list[tuple[str, str, str]] = [
    ("lo_din",  "lo_est",   "LO dinámica  vs  LO estática"),
    ("abb_ptr", "abb_vh",   "ABB punteros  vs  ABB vector heap"),
    ("trie_ptr","trie_arr", "Trie punteros  vs  Trie arreglos"),
    ("lo_din",  "hash_sr",  "LO dinámica  vs  Tabla Hash (sin redist.)"),
    ("lo_din",  "abb_ptr",  "LO dinámica  vs  ABB punteros"),
    ("lo_din",  "trie_ptr", "LO dinámica  vs  Trie punteros"),
    ("hash_sr", "trie_ptr", "Tabla Hash (sin redist.)  vs  Trie punteros"),
]


# Generadores de pares llave-valor

def _gen_llave(min_len: int = 3, max_len: int = 20) -> str:
    return "".join(random.choices(CHARS_LLAVE, k=random.randint(min_len, max_len)))


def _gen_valor() -> str:
    return "".join(random.choices(CHARS_VALOR, k=20))


def _pares_unicos(n: int, gen_fn: Callable[[], str]) -> list[tuple[str, str]]:
    """Genera n pares con llaves únicas usando gen_fn."""
    vistos: set[str] = set()
    pares: list[tuple[str, str]] = []
    while len(pares) < n:
        k = gen_fn()
        if k not in vistos:
            vistos.add(k)
            pares.append((k, _gen_valor()))
    return pares


def gen_aleatorio(n: int) -> list[tuple[str, str]]:
    """Llaves alfanuméricas aleatorias de largo 3–20 (caso base)."""
    return _pares_unicos(n, _gen_llave)


def gen_prefijo_comun(n: int, largo: int = 10) -> list[tuple[str, str]]:
    """Llaves que comparten un prefijo de `largo` caracteres (favorece Trie)."""
    prefijo = "".join(random.choices(CHARS_LLAVE, k=largo))
    suf_max = 20 - largo
    return _pares_unicos(
        n,
        lambda: prefijo + "".join(random.choices(CHARS_LLAVE, k=random.randint(1, suf_max))),
    )


def gen_sin_prefijo(n: int) -> list[tuple[str, str]]:
    """Llaves cortas de 1–3 chars (casi sin prefijos comunes, perjudica Trie)."""
    return _pares_unicos(n, lambda: _gen_llave(min_len=1, max_len=3))


def gen_ordenados(n: int) -> list[tuple[str, str]]:
    """Llaves en orden lexicográfico → ABB totalmente desbalanceado."""
    return sorted(gen_aleatorio(n), key=lambda p: p[0])


# Funciones de medición

def _poblar(e: object, pares: list[tuple[str, str]]) -> None:
    for k, v in pares:
        e.asigne(k, v)  # type: ignore[attr-defined]


def medir_assign(
    factory: Callable, pares: list[tuple[str, str]], corridas: int = CORRIDAS
) -> tuple[float, float]:
    """
    Tiempo promedio por operación Assign (μs).
    Cada corrida construye la estructura desde cero e inserta todos los pares.
    Retorna (media_μs, desviación_μs).
    """
    n = len(pares)
    tiempos: list[float] = []
    for _ in range(corridas):
        e = factory()
        t0 = time.perf_counter()
        for k, v in pares:
            e.asigne(k, v)  # type: ignore[attr-defined]
        t1 = time.perf_counter()
        tiempos.append((t1 - t0) / n * 1e6)
        del e
    media = statistics.mean(tiempos)
    desvio = statistics.stdev(tiempos) if corridas > 1 else 0.0
    return media, desvio


def medir_lookup(
    factory: Callable, pares: list[tuple[str, str]], corridas: int = CORRIDAS
) -> tuple[float, float]:
    """
    Tiempo promedio por operación Lookup (μs).
    Construye la estructura una vez y repite n búsquedas por corrida.
    Retorna (media_μs, desviación_μs).
    """
    n = len(pares)
    e = factory()
    _poblar(e, pares)
    llaves = [k for k, _ in pares]
    tiempos: list[float] = []
    for _ in range(corridas):
        random.shuffle(llaves)
        t0 = time.perf_counter()
        for k in llaves:
            e.obtenga(k)  # type: ignore[attr-defined]
        t1 = time.perf_counter()
        tiempos.append((t1 - t0) / n * 1e6)
    del e
    media = statistics.mean(tiempos)
    desvio = statistics.stdev(tiempos) if corridas > 1 else 0.0
    return media, desvio


UMBRAL_MUESTRA_UNASSIGN = 10_000  # por encima de este n, usa muestra en vez de reconstruir
TAMAÑO_MUESTRA_UNASSIGN = 1_000   # cantidad de deletes por corrida en modo muestra

def medir_unassign(
    factory: Callable, pares: list[tuple[str, str]], corridas: int = CORRIDAS
) -> tuple[float, float]:
    """
    Tiempo promedio por operación Unassign (us).

    Para n <= UMBRAL_MUESTRA_UNASSIGN: reconstruye la estructura en cada corrida
    y elimina todos los pares (medición exacta).

    Para n > UMBRAL_MUESTRA_UNASSIGN: construye una vez y en cada corrida mide
    el tiempo de eliminar/reinsertar TAMAÑO_MUESTRA_UNASSIGN pares al azar.
    Esto da el tiempo por operación en una estructura de tamaño n sin el costo
    de 10 reconstrucciones.
    """
    n = len(pares)
    tiempos: list[float] = []

    if n <= UMBRAL_MUESTRA_UNASSIGN:
        # Modo exacto: rebuild por corrida
        for _ in range(corridas):
            llaves = [k for k, _ in pares]
            random.shuffle(llaves)
            e = factory()
            _poblar(e, pares)
            t0 = time.perf_counter()
            for k in llaves:
                e.elimine(k)  # type: ignore[attr-defined]
            t1 = time.perf_counter()
            tiempos.append((t1 - t0) / n * 1e6)
            del e
    else:
        # Modo muestra: construye una vez, mide sobre TAMAÑO_MUESTRA_UNASSIGN deletes
        e = factory()
        _poblar(e, pares)
        todas_llaves = [k for k, _ in pares]
        valores = dict(pares)
        m = TAMAÑO_MUESTRA_UNASSIGN
        for _ in range(corridas):
            muestra = random.sample(todas_llaves, m)
            t0 = time.perf_counter()
            for k in muestra:
                e.elimine(k)  # type: ignore[attr-defined]
            t1 = time.perf_counter()
            # Restaurar la muestra para la siguiente corrida
            for k in muestra:
                e.asigne(k, valores[k])  # type: ignore[attr-defined]
            tiempos.append((t1 - t0) / m * 1e6)
        del e

    media = statistics.mean(tiempos)
    desvio = statistics.stdev(tiempos) if corridas > 1 else 0.0
    return media, desvio


def medir_print(factory: Callable, pares: list[tuple[str, str]]) -> float:
    """Segundos que tarda un Print completo (salida descartada a /dev/null)."""
    e = factory()
    _poblar(e, pares)
    with open(os.devnull, "w", encoding="utf-8") as null_f, redirect_stdout(null_f):
        t0 = time.perf_counter()
        e.imprima()  # type: ignore[attr-defined]
        t1 = time.perf_counter()
    del e
    return t1 - t0


def medir_done(factory: Callable, pares: list[tuple[str, str]]) -> float:
    """Segundos que tarda destruir (del/__del__) la estructura."""
    e = factory()
    _poblar(e, pares)
    t0 = time.perf_counter()
    del e
    t1 = time.perf_counter()
    return t1 - t0


def medir_memoria(factory: Callable, pares: list[tuple[str, str]]) -> float:
    """KB de memoria en uso por la estructura con n pares (medido con tracemalloc)."""
    tracemalloc.start()
    e = factory()
    _poblar(e, pares)
    actual, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del e
    return actual / 1024


# Experimento por estructura

Resultado = dict[str, object]


def experimento(
    nombre: str,
    factory: Callable,
    pares: list[tuple[str, str]],
    limite: int | None,
    corridas: int = CORRIDAS,
    incluir_extra: bool = False,
) -> Resultado:
    """
    Ejecuta todas las mediciones para una estructura y un conjunto de pares dado.
    Si n > limite, el experimento se omite y los campos quedan en None.
    Con incluir_extra=True mide también Print y Done (para n grande).
    """
    n = len(pares)
    r: Resultado = {
        "estructura": nombre,
        "n": n,
        "assign_media_us":   None,
        "assign_desvio_us":  None,
        "lookup_media_us":   None,
        "lookup_desvio_us":  None,
        "unassign_media_us": None,
        "unassign_desvio_us":None,
        "print_seg":         None,
        "done_seg":          None,
        "memoria_kb":        None,
    }

    if limite is not None and n > limite:
        if limite == LIMITE_LO:
            razon = "O(n²) impracticable"
        elif limite == LIMITE_HASH_SR:
            razon = "O(n²/m) impracticable sin redistribucion"
        else:
            razon = "uso de memoria O(n·L) impracticable"
        print(f"    {nombre:<30} n={n:>10,}  OMITIDO (n > límite {limite:,} — {razon})")
        return r

    print(f"    {nombre:<30} n={n:>10,} ", end="", flush=True)

    m, d = medir_assign(factory, pares, corridas)
    r["assign_media_us"], r["assign_desvio_us"] = m, d
    print(f"  A={m:9.4f}us", end="", flush=True)

    m, d = medir_lookup(factory, pares, corridas)
    r["lookup_media_us"], r["lookup_desvio_us"] = m, d
    print(f"  L={m:9.4f}us", end="", flush=True)

    m, d = medir_unassign(factory, pares, corridas)
    r["unassign_media_us"], r["unassign_desvio_us"] = m, d
    print(f"  U={m:9.4f}us", end="", flush=True)

    if incluir_extra:
        r["print_seg"] = medir_print(factory, pares)
        r["done_seg"]  = medir_done(factory, pares)
        print(f"  P={r['print_seg']:.3f}s  D={r['done_seg']:.4f}s", end="", flush=True)

    r["memoria_kb"] = medir_memoria(factory, pares)
    print(f"  M={r['memoria_kb']:,.0f}KB")
    return r


# Runner principal

def ejecutar_benchmark(corridas: int = CORRIDAS) -> list[Resultado]:
    """
    Ejecuta el benchmark completo:
      1. Las 7 comparaciones requeridas con llaves aleatorias (3 tamaños).
      2. Tendencia de Lista Ordenada en tamaños intermedios.
      3. Casos especiales: prefijo común, sin prefijo, ABB desbalanceado.
    Retorna la lista de todos los resultados y los guarda en CSV.
    """
    # Aumentar límite de recursión para ABB con árboles profundos
    sys.setrecursionlimit(10_000)

    sep = "─" * 74
    print(f"\n{'='*74}")
    print("  BENCHMARK — Tarea Programada 1 — CI-0116")
    print(f"  Corridas por experimento: {corridas}   |   Límite LO: n ≤ {LIMITE_LO:,}")
    print(f"{'='*74}")

    # Generar datos (una sola vez por tamaño)
    print("\n[Generando datos aleatorios...]  ", end="", flush=True)
    pares_std: dict[int, list[tuple[str, str]]] = {
        n: gen_aleatorio(n) for n in TAMAÑOS_MAIN
    }
    pares_lo_extra: dict[int, list[tuple[str, str]]] = {
        n: gen_aleatorio(n) for n in TAMAÑOS_LO_EXTRA
    }
    pares_pref   = {n: gen_prefijo_comun(n) for n in [100, min(50_000, LIMITE_LO * 10)]}
    pares_sinpref= {n: gen_sin_prefijo(n)   for n in [100, 5_000]}
    pares_ord    = gen_ordenados(LIMITE_ABB_ORDENADO)
    print("OK")

    todos: list[Resultado] = []

    # Caché: evita repetir el mismo (estructura, n, tipo_pares)
    cache: dict[tuple[str, int], Resultado] = {}

    def _run(clave: str, pares: list, tipo: str = "std") -> Resultado:
        key = (clave, len(pares))
        if key in cache:
            return cache[key]
        etiqueta, factory, limite = ESTRUCTURAS[clave]
        n_grande = (len(pares) == TAMAÑOS_MAIN[-1])
        r = experimento(etiqueta, factory, pares, limite,
                        corridas=corridas, incluir_extra=n_grande)
        cache[key] = r
        todos.append(r)
        return r

    # 1. Siete comparaciones requeridas
    print(f"\n{sep}")
    print("  COMPARACIONES REQUERIDAS (llaves aleatorias)")
    print(sep)
    for idx, (clave_a, clave_b, titulo) in enumerate(PAREJAS, 1):
        print(f"\n  Pareja {idx}: {titulo}")
        for n in TAMAÑOS_MAIN:
            _run(clave_a, pares_std[n])
            _run(clave_b, pares_std[n])

    # 2. Tendencia de Lista Ordenada en tamaños intermedios
    print(f"\n{sep}")
    print("  TENDENCIA DE LISTA ORDENADA (tamaños intermedios)")
    print(sep)
    for clave in ("lo_din", "lo_est"):
        print(f"\n  {ESTRUCTURAS[clave][0]}")
        for n, pares in pares_lo_extra.items():
            etiqueta, factory, limite = ESTRUCTURAS[clave]
            r = experimento(etiqueta, factory, pares, limite, corridas=corridas)
            todos.append(r)

    # 3. Casos especiales
    print(f"\n{sep}")
    print("  CASO ESPECIAL: llaves con prefijo común (favorece Trie)")
    print(sep)
    for n, pares in sorted(pares_pref.items()):
        print(f"\n  n={n:,}")
        for clave in ("trie_ptr", "trie_arr", "hash_sr", "abb_ptr"):
            etiqueta, factory, limite = ESTRUCTURAS[clave]
            r = experimento(f"{etiqueta} [pref_comun]", factory, pares, limite,
                            corridas=corridas)
            todos.append(r)

    print(f"\n{sep}")
    print("  CASO ESPECIAL: llaves cortas sin prefijo común (perjudica Trie)")
    print(sep)
    for n, pares in sorted(pares_sinpref.items()):
        print(f"\n  n={n:,}")
        for clave in ("trie_ptr", "trie_arr", "hash_sr"):
            etiqueta, factory, limite = ESTRUCTURAS[clave]
            r = experimento(f"{etiqueta} [sin_pref]", factory, pares, limite,
                            corridas=corridas)
            todos.append(r)

    print(f"\n{sep}")
    print(f"  CASO ESPECIAL: inserciones ordenadas → ABB desbalanceado (n={LIMITE_ABB_ORDENADO:,})")
    print("  Nota: ABB vector heap omitido (índice exponencial con árbol degenerado)")
    print(sep)
    for clave in ("abb_ptr",):
        etiqueta, factory, limite = ESTRUCTURAS[clave]
        r = experimento(f"{etiqueta} [ordenado]", factory, pares_ord, limite,
                        corridas=corridas)
        todos.append(r)
    # Comparar con ABB aleatorio al mismo n para evidenciar degradación
    pares_ale_ord = gen_aleatorio(LIMITE_ABB_ORDENADO)
    for clave in ("abb_ptr",):
        etiqueta, factory, limite = ESTRUCTURAS[clave]
        r = experimento(f"{etiqueta} [aleatorio]", factory, pares_ale_ord, limite,
                        corridas=corridas)
        todos.append(r)

    # Guardar CSV
    _guardar_csv(todos)
    print(f"\n{'='*74}")
    print(f"  ✓ Benchmark completo. Resultados en: {CSV_SALIDA}")
    print(f"{'='*74}\n")
    return todos


# Exportar CSV

_CAMPOS_CSV = [
    "estructura", "n",
    "assign_media_us", "assign_desvio_us",
    "lookup_media_us", "lookup_desvio_us",
    "unassign_media_us", "unassign_desvio_us",
    "print_seg", "done_seg", "memoria_kb",
]


def _guardar_csv(resultados: list[Resultado]) -> None:
    with open(CSV_SALIDA, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_CAMPOS_CSV)
        writer.writeheader()
        for r in resultados:
            writer.writerow({c: r.get(c) for c in _CAMPOS_CSV})


# Menú de benchmark (llamado desde __init__.py)

def menu_benchmark() -> None:
    """Entry point desde el menú principal (opción 2)."""
    print("\n" + "=" * 60)
    print("  Análisis de rendimiento — Tarea Programada 1")
    print("=" * 60)
    print(f"\n  Corridas por experimento: {CORRIDAS} (predeterminado)")
    print("  Tamaños: 100 / 50,000 / 1,000,000 pares")
    print("  Lista Ordenada se omite para n > 5,000 (O(n²) impracticable)")
    print("\n  Advertencia: el benchmark completo puede tardar 20–40 min.")
    print("  Los resultados se guardan automáticamente en resultados_benchmark.csv\n")

    try:
        entrada = input("  ¿Cuántas corridas por experimento? [Enter = 10]: ").strip()
        corridas = int(entrada) if entrada else CORRIDAS
    except ValueError:
        corridas = CORRIDAS

    print()
    ejecutar_benchmark(corridas=corridas)
    input("  Presione Enter para volver al menú...")


# Ejecución directa

if __name__ == "__main__":
    ejecutar_benchmark()
