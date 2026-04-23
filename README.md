# Tarea Programada 1: Modelo Función (Arreglo Asociativo Llave-Valor)

**Curso:** CI-0116 Análisis de Algoritmos y Estructuras de Datos  
**Universidad de Costa Rica**  
**Autores:** Marina Castro Peralta (C31886), Emanuel González Chaves (C03361)

## Descripción

Implementación del Modelo Función como arreglo asociativo llave-valor. El modelo
representa una función parcial sobreyectiva del conjunto de llaves al conjunto de
valores: cada llave es única y se asocia a exactamente un valor.

El proyecto se entrega en tres etapas. Este repositorio corresponde a la primera,
con fecha de entrega el 28 de abril.

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

La especificación y descripción formal de cada estructura está en [`doc/index.md`](doc/index.md).

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

Correr las pruebas:

```bash
uv run python test/test_listaordenadadinamica.py
```

## Estructura del repositorio

```
src/tarea1/     código fuente de cada implementación
test/           pruebas por estructura de datos
doc/            especificación y descripción de las estructuras
```