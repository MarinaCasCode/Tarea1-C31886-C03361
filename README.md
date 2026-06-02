# Tarea Programada 1: Modelo Función (Arreglo Asociativo Llave-Valor)

**Curso:** CI-0116 Análisis de Algoritmos y Estructuras de Datos  
**Universidad de Costa Rica**  
**Autores:** Marina Castro Peralta (C31886), Emanuel González Chaves (C03361)

## Descripción

Implementación del Modelo Función como arreglo asociativo llave-valor. El modelo
representa una función parcial sobreyectiva del conjunto de llaves al conjunto de
valores: cada llave es única y se asocia a exactamente un valor.

El proyecto se entrega en tres etapas. Este repositorio contiene las tres entregas completas.

## Primera etapa

Incluye la especificación del Modelo Función, la Lista Ordenada genérica con sus
dos implementaciones (por punteros y por arreglos), la Tabla Hash genérica con su
implementación abierta, la función hash con evaluación de aleatoriedad, el proceso
de redistribución, y el programa de prueba con menú interactivo.

| Estructura | Archivo |
|---|---|
| Lista Ordenada por punteros | `src/tarea1/listaordenadadinamica.py` |
| Lista Ordenada por arreglos | `src/tarea1/listaordenadaestatica.py` |
| Tabla Hash abierta | `src/tarea1/tablahashabierta.py` |

## Segunda etapa

Incluye el Árbol de Búsqueda Binaria genérico con sus dos implementaciones (por
punteros y por vector heap), el Trie genérico con sus dos implementaciones (por
punteros y por arreglos), y la integración de todas las estructuras en el menú
interactivo.

| Estructura | Archivo |
|---|---|
| ABB por punteros | `src/tarea1/abbpunteros.py` |
| ABB por vector heap | `src/tarea1/abbvectorheap.py` |
| Trie por punteros | `src/tarea1/triepunteros.py` |
| Trie por arreglos | `src/tarea1/triearreglos.py` |

La especificación y descripción formal de cada estructura está en [`doc/index.md`](doc/index.md).

## Tercera etapa

Análisis empírico de rendimiento de las siete estructuras. Incluye un programa de
benchmark que mide los tiempos de las operaciones Assign, Lookup, Unassign, Print
y Done, así como el uso de memoria, sobre tres tamaños de entrada (n = 100,
50 000 y 1 000 000) con 10 corridas por experimento. El informe final con tablas,
gráficas, comparación teoría vs. resultados empíricos y rangos para N se entrega
como `Informe_Tarea1_TerceraEntrega.pdf`.

| Componente | Archivo |
|---|---|
| Programa de benchmark | `src/tarea1/benchmark.py` |
| Resultados crudos (10 corridas) | `resultados_benchmark.csv` |
| Informe final | `Informe_Tarea1_TerceraEntrega.pdf` |

Para lanzar el benchmark desde el menú principal: ejecutar `uv run tarea1` y
seleccionar la opción 2 (Pruebas de rendimiento). Las estructuras con
comportamiento cuadrático (Lista Ordenada, Tabla Hash sin redistribución) se
omiten automáticamente por encima de su límite práctico y se documenta la
limitación en el reporte.

## Requisitos

- Python 3.13 o superior
- [uv](https://github.com/astral-sh/uv)

## Instalación

```bash
git clone https://github.com/MarinaCasCode/Tarea1-C31886-C03361.git
cd Tarea1-C31886-C03361
uv sync
```

## Uso

Lanzar el menú interactivo:

```bash
uv run tarea1
```

Correr las pruebas de una estructura:

```bash
uv run python test/test_abbpunteros.py
uv run python test/test_abbvectorheap.py
uv run python test/test_triepunteros.py
uv run python test/test_triearreglos.py
```

Ejecutar el benchmark completo (≈ 20–30 minutos a 10 corridas):

```bash
uv run tarea1        # menú principal, opción 2
```

Los resultados se guardan en `resultados_benchmark.csv`.

## Estructura del repositorio

```
src/tarea1/                          código fuente de cada implementación
src/tarea1/benchmark.py              programa de análisis empírico
test/                                pruebas por estructura de datos
doc/                                 especificación y descripción de las estructuras
resultados_benchmark.csv             datos crudos del benchmark (10 corridas)
Informe_Tarea1_TerceraEntrega.pdf   informe final de la tercera entrega
```