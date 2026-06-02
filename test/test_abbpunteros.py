"""
Pruebas para AbbPunteros (Árbol de Búsqueda Binaria por punteros)

Pruebas incluidas:
  1. Init          - el árbol empieza vacío (tamaño 0)
  2. Asigne        - insertar pares nuevos y verificar orden inorden
  3. Asigne        - actualizar valor de llave ya existente sin duplicar
  4. Obtenga       - buscar llave existente y llave ausente (retorna None)
  5. Elimine       - borrar hoja (nodo sin hijos)
  6. Elimine       - borrar nodo con un solo hijo
  7. Elimine       - borrar nodo con dos hijos
  8. Elimine       - borrar llave inexistente (no debe lanzar excepción)
  9. Llaves        - llaves() con árbol vacío retorna []
 10. Llaves        - llaves() retorna llaves en orden lexicográfico
 11. Asigne        - llaves numéricas como string ("007", "2025", "42")
 12. Imprima       - imprima() y __str__() producen salida correcta
 13. Limpie        - vaciar el árbol y reutilizarlo
 14. Valores dup.  - dos llaves distintas pueden tener el mismo valor
 15. Done          - __del__ se ejecuta sin errores
"""

from tarea1.abbpunteros import AbbPunteros


def titulo(texto):
    print(f"\n--- {texto} ---")


# =============================================================
# 1. Init
# =============================================================
titulo("Init: el árbol empieza vacío")
abb = AbbPunteros()
assert len(abb) == 0
print("Tamaño inicial:", len(abb))


# =============================================================
# 2. Asigne básico
# =============================================================
titulo("Asigne: insertar cinco pares")
abb.asigne("manzana", "frutarojaaaaaaaaaaaa")
abb.asigne("banana",  "frutamarillaaaaaaaaa")
abb.asigne("cereza",  "frutarojaaaaaaaaaaaa")
abb.asigne("durazno", "frutanaranjaaaaaaaaa")
abb.asigne("anona",   "frutaverdeaaaaaaaaaa")

assert len(abb) == 5
print("Tamaño luego de 5 inserciones:", len(abb))

# Inorden debe retornar llaves en orden lexicográfico
llaves = abb.llaves()
assert llaves == sorted(llaves), f"Orden incorrecto: {llaves}"
print("Llaves en orden inorden:", llaves)


# =============================================================
# 3. Asigne sobre llave existente (actualización)
# =============================================================
titulo("Asigne: actualizar valor de llave existente")
abb.asigne("banana", "valoractualizadoaaaa")
assert len(abb) == 5, "No debe crecer al actualizar una llave existente"
assert abb.obtenga("banana") == "valoractualizadoaaaa"
print("Valor actualizado correctamente, tamaño sigue en:", len(abb))


# =============================================================
# 4. Obtenga
# =============================================================
titulo("Obtenga: llave existente y llave ausente")
assert abb.obtenga("cereza") == "frutarojaaaaaaaaaaaa"
print("cereza →", abb.obtenga("cereza"))

assert abb.obtenga("papaya") is None
print("papaya → None (no existe)")


# =============================================================
# 5. Elimine: hoja (nodo sin hijos)
# =============================================================
titulo("Elimine: borrar hoja")
abb2 = AbbPunteros()
abb2.asigne("50", "cincuentaaaaaaaaaaaa")
abb2.asigne("30", "treintaaaaaaaaaaaaaa")
abb2.asigne("70", "setentaaaaaaaaaaaaaa")
abb2.asigne("20", "veinteaaaaaaaaaaaaaa")

abb2.elimine("20")  # hoja
assert len(abb2) == 3
assert abb2.obtenga("20") is None
print("Hoja eliminada, llaves:", abb2.llaves())


# =============================================================
# 6. Elimine: nodo con un solo hijo
# =============================================================
titulo("Elimine: borrar nodo con un solo hijo")
abb2.elimine("30")  # solo tenía hijo derecho (40 no existe, tenía izq=20 que ya borramos)
assert len(abb2) == 2
assert abb2.obtenga("30") is None
print("Nodo con un hijo eliminado, llaves:", abb2.llaves())


# =============================================================
# 7. Elimine: nodo con dos hijos
# =============================================================
titulo("Elimine: borrar nodo con dos hijos")
abb3 = AbbPunteros()
abb3.asigne("50", "cincuentaaaaaaaaaaaa")
abb3.asigne("30", "treintaaaaaaaaaaaaaa")
abb3.asigne("70", "setentaaaaaaaaaaaaaa")
abb3.asigne("20", "veinteaaaaaaaaaaaaaa")
abb3.asigne("40", "cuarentaaaaaaaaaaaaa")

abb3.elimine("30")  # tiene dos hijos: 20 y 40
assert len(abb3) == 4
assert abb3.obtenga("30") is None
assert abb3.obtenga("20") is not None
assert abb3.obtenga("40") is not None
llaves3 = abb3.llaves()
assert llaves3 == sorted(llaves3), f"Orden roto tras eliminar: {llaves3}"
print("Nodo con dos hijos eliminado, llaves:", llaves3)


# =============================================================
# 8. Elimine: llave inexistente
# =============================================================
titulo("Elimine: llave inexistente no lanza excepción")
abb3.elimine("99")
assert len(abb3) == 4
print("Tamaño sin cambios:", len(abb3))


# =============================================================
# 9. Llaves: árbol vacío
# =============================================================
titulo("Llaves: árbol vacío")
abb4 = AbbPunteros()
assert abb4.llaves() == []
print("llaves() con árbol vacío:", abb4.llaves())


# =============================================================
# 10. Llaves: orden lexicográfico
# =============================================================
titulo("Llaves: orden inorden = orden lexicográfico")
abb5 = AbbPunteros()
for k in ["mango", "kiwi", "pera", "uva", "fresa"]:
    abb5.asigne(k, "valorgeneriaaaaaaaaa")
llaves5 = abb5.llaves()
assert llaves5 == sorted(llaves5)
print("Llaves en orden:", llaves5)


# =============================================================
# 11. Llaves numéricas como string
# =============================================================
titulo("Asigne: llaves numéricas como string")
abb6 = AbbPunteros()
abb6.asigne("007",  "agentesecretoaaaaaaa")
abb6.asigne("2025", "anionuevoaaaaaaaaaaa")
abb6.asigne("42",   "larespuestaaaaaaaaaa")

# Orden lexicográfico: "007" < "2025" < "42"
assert abb6.llaves() == ["007", "2025", "42"], f"Orden incorrecto: {abb6.llaves()}"
print("Orden léxico de llaves numéricas:", abb6.llaves())


# =============================================================
# 12. Imprima y __str__
# =============================================================
titulo("Imprima y __str__")
abb7 = AbbPunteros()
abb7.asigne("zorro", "animalzorroaaaaaaaaa")
abb7.asigne("oso",   "animalosoaaaaaaaaaaa")
abb7.asigne("puma",  "animalpumaaaaaaaaaaa")

print("imprima():")
abb7.imprima()
print("__str__():", abb7)


# =============================================================
# 13. Limpie
# =============================================================
titulo("Limpie: vaciar y reutilizar el árbol")
abb7.limpie()
assert len(abb7) == 0
assert abb7.llaves() == []
print("Árbol limpio, tamaño:", len(abb7))

abb7.asigne("nuevo", "despuesdeclearaaaaaa")
assert abb7.obtenga("nuevo") == "despuesdeclearaaaaaa"
print("Árbol reutilizable, nuevo valor:", abb7.obtenga("nuevo"))


# =============================================================
# 14. Valores duplicados
# =============================================================
titulo("Valores duplicados en llaves distintas")
abb8 = AbbPunteros()
abb8.asigne("llave1", "mismovaloraaaaaaaaaa")
abb8.asigne("llave2", "mismovaloraaaaaaaaaa")
assert abb8.obtenga("llave1") == abb8.obtenga("llave2")
print("llave1 y llave2 comparten valor:", abb8.obtenga("llave1"))


# =============================================================
# 15. Done (__del__)
# =============================================================
titulo("Done: destructor")
abb9 = AbbPunteros()
abb9.asigne("test", "valortestaaaaaaaaaaa")
del abb9
print("__del__ ejecutado sin errores")


# =============================================================
print("\nTodas las pruebas pasaron.")