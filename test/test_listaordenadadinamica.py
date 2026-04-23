"""
Pruebas para la Lista Ordenada Dinámica (punteros simplemente enlazada)

Pruebas incluidas:
  1. Init          - la lista empieza vacía (tamaño 0)
  2. Asigne        - insertar pares nuevos y verificar orden lexicográfico
  3. Asigne        - actualizar valor de llave ya existente sin duplicar
  4. Obtenga       - buscar llave existente y llave ausente (retorna None)
  5. Elimine       - borrar llave existente
  6. Elimine       - borrar llave inexistente (no debe lanzar excepción)
  7. Elimine       - casos borde: primer nodo, último nodo, vaciar lista
  8. Llaves        - llaves() con lista vacía retorna []
  9. Asigne        - llaves numéricas como string ("007", "2025", "42")
 10. Imprima       - imprima() y __str__() producen salida correcta
 11. Limpie        - vaciar la lista y reutilizarla
 12. Valores dup.  - dos llaves distintas pueden tener el mismo valor
 13. Done          - __del__ se ejecuta sin errores
"""

from tarea1.listaordenadadinamica import ListaOrdenadaDinámica


def titulo(texto):
    print(f"\n--- {texto} ---")


# =============================================================
# 1. Init
# =============================================================
titulo("Init: la lista empieza vacía")
lista = ListaOrdenadaDinámica()
assert len(lista) == 0
print("Tamaño inicial:", len(lista))


# =============================================================
# 2. Asigne básico
# =============================================================
titulo("Asigne: insertar tres pares")
lista.asigne("manzana", "frutarojaaaaaaaaaaa")
lista.asigne("banana",  "frutamarillaaaaaaaaa")
lista.asigne("cereza",  "frutarojaaaaaaaaaaa")

assert len(lista) == 3
print("Tamaño luego de 3 inserciones:", len(lista))

llaves = lista.llaves()
assert llaves == ["banana", "cereza", "manzana"], f"Orden incorrecto: {llaves}"
print("Llaves en orden:", llaves)


# =============================================================
# 3. Asigne sobre llave existente (actualización)
# =============================================================
titulo("Asigne: actualizar valor de llave existente")
lista.asigne("banana", "valoractualizadoaaaa")
assert len(lista) == 3, "No debe crecer al actualizar una llave existente"
assert lista.obtenga("banana") == "valoractualizadoaaaa"
print("Valor actualizado correctamente, tamaño sigue en:", len(lista))


# =============================================================
# 4. Obtenga
# =============================================================
titulo("Obtenga: llave existente y llave ausente")
assert lista.obtenga("cereza") == "frutarojaaaaaaaaaaa"
print("cereza →", lista.obtenga("cereza"))

assert lista.obtenga("durazno") is None
print("durazno → None (no existe)")


# =============================================================
# 5. Elimine: llave existente
# =============================================================
titulo("Elimine: borrar cereza")
lista.elimine("cereza")
assert len(lista) == 2
assert lista.obtenga("cereza") is None
print("Llaves tras eliminar cereza:", lista.llaves())


# =============================================================
# 6. Elimine: llave inexistente
# =============================================================
titulo("Elimine: llave inexistente no lanza excepción")
lista.elimine("papaya")
assert len(lista) == 2
print("Tamaño sin cambios:", len(lista))


# =============================================================
# 7. Elimine: casos borde de punteros
# =============================================================
titulo("Elimine: primer nodo, último nodo, vaciar lista")
lista2 = ListaOrdenadaDinámica()
lista2.asigne("alfa",  "letraalfaaaaaaaaaaaa")
lista2.asigne("beta",  "letrabetaaaaaaaaaaaa")
lista2.asigne("gamma", "letragammaaaaaaaaaaa")

lista2.elimine("alfa")
assert lista2.llaves() == ["beta", "gamma"]
print("Tras eliminar primer nodo:", lista2.llaves())

lista2.elimine("gamma")
assert lista2.llaves() == ["beta"]
print("Tras eliminar último nodo:", lista2.llaves())

lista2.elimine("beta")
assert len(lista2) == 0
print("Lista vacía, tamaño:", len(lista2))


# =============================================================
# 8. Llaves con lista vacía
# =============================================================
titulo("Llaves: lista vacía")
lista3 = ListaOrdenadaDinámica()
assert lista3.llaves() == []
print("llaves() con lista vacía:", lista3.llaves())


# =============================================================
# 9. Llaves numéricas como string
# =============================================================
titulo("Asigne: llaves numéricas como string")
lista4 = ListaOrdenadaDinámica()
lista4.asigne("007",  "agentesecretoaaaaaa")
lista4.asigne("2025", "anionuevoaaaaaaaaaaa")
lista4.asigne("42",   "larespuestaaaaaaaaa")

# Orden lexicográfico, no numérico: "007" < "2025" < "42"
assert lista4.llaves() == ["007", "2025", "42"], f"Orden incorrecto: {lista4.llaves()}"
print("Orden léxico de llaves numéricas:", lista4.llaves())


# =============================================================
# 10. Imprima y __str__
# =============================================================
titulo("Imprima y __str__")
lista5 = ListaOrdenadaDinámica()
lista5.asigne("zorro", "animalzorroaaaaaaaaa")
lista5.asigne("oso",   "animalosoaaaaaaaaaaa")
lista5.asigne("puma",  "animalpumaaaaaaaaaaa")

print("imprima():")
lista5.imprima()
print("__str__():", lista5)


# =============================================================
# 11. Limpie
# =============================================================
titulo("Limpie: vaciar y reutilizar la lista")
lista5.limpie()
assert len(lista5) == 0
assert lista5.llaves() == []
print("Lista limpia, tamaño:", len(lista5))

lista5.asigne("nuevo", "despuesdeclearaaaaa")
assert lista5.obtenga("nuevo") == "despuesdeclearaaaaa"
print("Lista reutilizable, nuevo valor:", lista5.obtenga("nuevo"))


# =============================================================
# 12. Valores duplicados
# =============================================================
titulo("Valores duplicados en llaves distintas")
lista6 = ListaOrdenadaDinámica()
lista6.asigne("llave1", "mismovaloraaaaaaaaaa")
lista6.asigne("llave2", "mismovaloraaaaaaaaaa")
assert lista6.obtenga("llave1") == lista6.obtenga("llave2")
print("llave1 y llave2 comparten valor:", lista6.obtenga("llave1"))


# =============================================================
# 13. Done (__del__)
# =============================================================
titulo("Done: destructor")
lista7 = ListaOrdenadaDinámica()
lista7.asigne("test", "valortestaaaaaaaaaaa")
del lista7
print("__del__ ejecutado sin errores")


# =============================================================
print("\nTodas las pruebas pasaron.")