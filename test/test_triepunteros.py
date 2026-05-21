"""
Pruebas para TriePunteros (Trie por punteros)

Pruebas incluidas:
  1. Init          - el trie empieza vacío (tamaño 0)
  2. Asigne        - insertar pares nuevos
  3. Asigne        - actualizar valor de llave ya existente sin duplicar
  4. Asigne        - llaves con prefijos comunes
  5. Obtenga       - buscar llave existente y llave ausente (retorna None)
  6. Elimine       - borrar llave existente (hoja)
  7. Elimine       - borrar llave que es prefijo de otra
  8. Elimine       - borrar llave inexistente (no debe lanzar excepción)
  9. Llaves        - llaves() con trie vacío retorna []
 10. Llaves        - llaves() retorna todas las llaves almacenadas
 11. Asigne        - llaves numéricas como string ("007", "2025", "42")
 12. Imprima       - imprima() y __str__() producen salida correcta
 13. Limpie        - vaciar el trie y reutilizarlo
 14. Valores dup.  - dos llaves distintas pueden tener el mismo valor
 15. Done          - __del__ se ejecuta sin errores
"""

from tarea1.triepunteros import TriePunteros


def titulo(texto):
    print(f"\n--- {texto} ---")


# =============================================================
# 1. Init
# =============================================================
titulo("Init: el trie empieza vacío")
trie = TriePunteros()
assert len(trie) == 0
print("Tamaño inicial:", len(trie))


# =============================================================
# 2. Asigne básico
# =============================================================
titulo("Asigne: insertar tres pares")
trie.asigne("bat", "palabrabataaaaaaaaaaa"[:20])
trie.asigne("bad", "palabrabadaaaaaaaaaaa"[:20])
trie.asigne("be",  "palabrabeaaaaaaaaaaaa"[:20])

assert len(trie) == 3
print("Tamaño luego de 3 inserciones:", len(trie))


# =============================================================
# 3. Asigne sobre llave existente (actualización)
# =============================================================
titulo("Asigne: actualizar valor de llave existente")
trie.asigne("bat", "valoractualizadoaaaa")
assert len(trie) == 3
assert trie.obtenga("bat") == "valoractualizadoaaaa"
print("Valor actualizado correctamente, tamaño sigue en:", len(trie))


# =============================================================
# 4. Asigne llaves con prefijos comunes
# =============================================================
titulo("Asigne: llaves con prefijos comunes")
trie2 = TriePunteros()
trie2.asigne("banana",  "frutamarillaaaaaaaaa")
trie2.asigne("ban",     "prefijobanaaaaaaaaa")
trie2.asigne("band",    "palabrabandaaaaaaaaa")
trie2.asigne("bandana", "palabrabandanaaaaaaa")

assert len(trie2) == 4
assert trie2.obtenga("ban")     is not None
assert trie2.obtenga("band")    is not None
assert trie2.obtenga("bandana") is not None
print("Llaves con prefijos comunes:", sorted(trie2.llaves()))


# =============================================================
# 5. Obtenga
# =============================================================
titulo("Obtenga: llave existente y llave ausente")
assert trie.obtenga("bad") == "palabrabadaaaaaaaaaaa"[:20]
print("bad →", trie.obtenga("bad"))

assert trie.obtenga("ba") is None
print("ba → None (prefijo pero no llave completa)")

assert trie.obtenga("xyz") is None
print("xyz → None (no existe)")


# =============================================================
# 6. Elimine: hoja
# =============================================================
titulo("Elimine: borrar llave hoja")
trie.elimine("bat")
assert len(trie) == 2
assert trie.obtenga("bat") is None
assert trie.obtenga("bad") is not None  # bad sigue existiendo
print("Tras eliminar bat, llaves:", sorted(trie.llaves()))


# =============================================================
# 7. Elimine: llave que es prefijo de otra
# =============================================================
titulo("Elimine: borrar llave que es prefijo de otra")
trie2.elimine("ban")
assert len(trie2) == 3
assert trie2.obtenga("ban")     is None
assert trie2.obtenga("band")    is not None  # band sigue existiendo
assert trie2.obtenga("bandana") is not None  # bandana sigue existiendo
print("Tras eliminar ban, llaves:", sorted(trie2.llaves()))


# =============================================================
# 8. Elimine: llave inexistente
# =============================================================
titulo("Elimine: llave inexistente no lanza excepción")
trie.elimine("xyz")
assert len(trie) == 2
print("Tamaño sin cambios:", len(trie))


# =============================================================
# 9. Llaves: trie vacío
# =============================================================
titulo("Llaves: trie vacío")
trie3 = TriePunteros()
assert trie3.llaves() == []
print("llaves() con trie vacío:", trie3.llaves())


# =============================================================
# 10. Llaves: todas las llaves almacenadas
# =============================================================
titulo("Llaves: retorna todas las llaves")
trie4 = TriePunteros()
palabras = ["mango", "manzana", "man", "mar", "sol"]
for p in palabras:
    trie4.asigne(p, "valorgeneriaaaaaaaaa")
llaves4 = trie4.llaves()
assert sorted(llaves4) == sorted(palabras), f"Faltan llaves: {llaves4}"
print("Llaves almacenadas:", sorted(llaves4))


# =============================================================
# 11. Llaves numéricas como string
# =============================================================
titulo("Asigne: llaves numéricas como string")
trie5 = TriePunteros()
trie5.asigne("007",  "agentesecretoaaaaaa")
trie5.asigne("2025", "anionuevoaaaaaaaaaaa")
trie5.asigne("42",   "larespuestaaaaaaaaa")

assert len(trie5) == 3
assert trie5.obtenga("007")  == "agentesecretoaaaaaa"
assert trie5.obtenga("2025") == "anionuevoaaaaaaaaaaa"
assert trie5.obtenga("42")   == "larespuestaaaaaaaaa"
print("Llaves numéricas:", sorted(trie5.llaves()))


# =============================================================
# 12. Imprima y __str__
# =============================================================
titulo("Imprima y __str__")
trie6 = TriePunteros()
trie6.asigne("zorro", "animalzorroaaaaaaaaa")
trie6.asigne("oso",   "animalosoaaaaaaaaaaa")
trie6.asigne("puma",  "animalpumaaaaaaaaaaa")

print("imprima():")
trie6.imprima()
print("__str__():", trie6)


# =============================================================
# 13. Limpie
# =============================================================
titulo("Limpie: vaciar y reutilizar el trie")
trie6.limpie()
assert len(trie6) == 0
assert trie6.llaves() == []
print("Trie limpio, tamaño:", len(trie6))

trie6.asigne("nuevo", "despuesdeclearaaaaa")
assert trie6.obtenga("nuevo") == "despuesdeclearaaaaa"
print("Trie reutilizable, nuevo valor:", trie6.obtenga("nuevo"))


# =============================================================
# 14. Valores duplicados
# =============================================================
titulo("Valores duplicados en llaves distintas")
trie7 = TriePunteros()
trie7.asigne("llave1", "mismovaloraaaaaaaaaa")
trie7.asigne("llave2", "mismovaloraaaaaaaaaa")
assert trie7.obtenga("llave1") == trie7.obtenga("llave2")
print("llave1 y llave2 comparten valor:", trie7.obtenga("llave1"))


# =============================================================
# 15. Done (__del__)
# =============================================================
titulo("Done: destructor")
trie8 = TriePunteros()
trie8.asigne("test", "valortestaaaaaaaaaaa")
del trie8
print("__del__ ejecutado sin errores")


# =============================================================
print("\nTodas las pruebas pasaron.")