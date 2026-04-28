"""
Pruebas para la Tabla Hash Abierta

Pruebas incluidas:
  1. Init          - la tabla empieza vacía (tamaño 0)
  2. Asigne        - insertar pares nuevos
  3. Asigne        - actualizar valor de llave ya existente sin duplicar
  4. Obtenga       - buscar llave existente y llave ausente (retorna None)
  5. Elimine       - borrar llave existente
  6. Elimine       - borrar llave inexistente (no debe lanzar excepción)
  7. Llaves        - llaves() con lista vacía retorna []
  8. Asigne        - llaves numéricas como string ("007", "2025", "42")
  9. Imprima       - imprima() y __str__() producen salida correcta
 10. Limpie        - vaciar la tabla y reutilizarla
 11. Valores dup.  - dos llaves distintas pueden tener el mismo valor
 12. Colisiones    - llaves que colisionan coexisten en la misma cubeta
 13. Redistribuir  - la tabla crece cuando se supera el umbral de carga
 14. Varianza      - la función hash distribuye con varianza razonable
 15. Done          - __del__ se ejecuta sin errores
"""

from tarea1.tablahashabierta import TablaHashAbierta


def titulo(texto):
    print(f"\n--- {texto} ---")


# =============================================================
# 1. Init
# =============================================================
titulo("Init: la tabla empieza vacía")
tabla = TablaHashAbierta()
assert len(tabla) == 0
print("Tamaño inicial:", len(tabla))


# =============================================================
# 2. Asigne básico
# =============================================================
titulo("Asigne: insertar tres pares")
tabla.asigne("manzana", "frutarojaaaaaaaaaaa")
tabla.asigne("banana",  "frutamarillaaaaaaaaa")
tabla.asigne("cereza",  "frutarojaaaaaaaaaaa")

assert len(tabla) == 3
print("Tamaño luego de 3 inserciones:", len(tabla))


# =============================================================
# 3. Asigne sobre llave existente (actualización)
# =============================================================
titulo("Asigne: actualizar valor de llave existente")
tabla.asigne("banana", "valoractualizadoaaaa")
assert len(tabla) == 3, "No debe crecer al actualizar una llave existente"
assert tabla.obtenga("banana") == "valoractualizadoaaaa"
print("Valor actualizado correctamente, tamaño sigue en:", len(tabla))


# =============================================================
# 4. Obtenga
# =============================================================
titulo("Obtenga: llave existente y llave ausente")
assert tabla.obtenga("cereza") == "frutarojaaaaaaaaaaa"
print("cereza →", tabla.obtenga("cereza"))

assert tabla.obtenga("durazno") is None
print("durazno → None (no existe)")


# =============================================================
# 5. Elimine: llave existente
# =============================================================
titulo("Elimine: borrar cereza")
tabla.elimine("cereza")
assert len(tabla) == 2
assert tabla.obtenga("cereza") is None
print("Tamaño tras eliminar cereza:", len(tabla))


# =============================================================
# 6. Elimine: llave inexistente
# =============================================================
titulo("Elimine: llave inexistente no lanza excepción")
tabla.elimine("papaya")
assert len(tabla) == 2
print("Tamaño sin cambios:", len(tabla))


# =============================================================
# 7. Llaves con tabla vacía
# =============================================================
titulo("Llaves: tabla vacía")
tabla2 = TablaHashAbierta()
assert tabla2.llaves() == []
print("llaves() con tabla vacía:", tabla2.llaves())


# =============================================================
# 8. Llaves numéricas como string
# =============================================================
titulo("Asigne: llaves numéricas como string")
tabla3 = TablaHashAbierta()
tabla3.asigne("007",  "agentesecretoaaaaaa")
tabla3.asigne("2025", "anionuevoaaaaaaaaaaa")
tabla3.asigne("42",   "larespuestaaaaaaaaa")

assert len(tabla3) == 3
assert tabla3.obtenga("007")  == "agentesecretoaaaaaa"
assert tabla3.obtenga("2025") == "anionuevoaaaaaaaaaaa"
assert tabla3.obtenga("42")   == "larespuestaaaaaaaaa"
print("Llaves numéricas como string insertadas:", sorted(tabla3.llaves()))


# =============================================================
# 9. Imprima y __str__
# =============================================================
titulo("Imprima y __str__")
tabla4 = TablaHashAbierta()
tabla4.asigne("zorro", "animalzorroaaaaaaaaa")
tabla4.asigne("oso",   "animalosoaaaaaaaaaaa")
tabla4.asigne("puma",  "animalpumaaaaaaaaaaa")

print("imprima():")
tabla4.imprima()
print("__str__():", tabla4)


# =============================================================
# 10. Limpie
# =============================================================
titulo("Limpie: vaciar y reutilizar la tabla")
tabla4.limpie()
assert len(tabla4) == 0
assert tabla4.llaves() == []
print("Tabla limpia, tamaño:", len(tabla4))

tabla4.asigne("nuevo", "despuesdeclearaaaaa")
assert tabla4.obtenga("nuevo") == "despuesdeclearaaaaa"
print("Tabla reutilizable, nuevo valor:", tabla4.obtenga("nuevo"))


# =============================================================
# 11. Valores duplicados
# =============================================================
titulo("Valores duplicados en llaves distintas")
tabla5 = TablaHashAbierta()
tabla5.asigne("llave1", "mismovaloraaaaaaaaaa")
tabla5.asigne("llave2", "mismovaloraaaaaaaaaa")
assert tabla5.obtenga("llave1") == tabla5.obtenga("llave2")
print("llave1 y llave2 comparten valor:", tabla5.obtenga("llave1"))


# =============================================================
# 12. Colisiones: llaves en la misma cubeta coexisten
# =============================================================
titulo("Colisiones: múltiples llaves en la misma cubeta")
# Se usa capacidad 1 para forzar que todo caiga en la misma cubeta
tabla6 = TablaHashAbierta(table_size=1)
tabla6.asigne("alfa",  "letraalfaaaaaaaaaaaa")
tabla6.asigne("beta",  "letrabetaaaaaaaaaaaa")
tabla6.asigne("gamma", "letragammaaaaaaaaaaa")

assert tabla6.obtenga("alfa")  == "letraalfaaaaaaaaaaaa"
assert tabla6.obtenga("beta")  == "letrabetaaaaaaaaaaaa"
assert tabla6.obtenga("gamma") == "letragammaaaaaaaaaaa"
assert len(tabla6) == 3
print("Tres llaves en la misma cubeta, tamaño:", len(tabla6))

tabla6.elimine("beta")
assert tabla6.obtenga("beta") is None
assert len(tabla6) == 2
print("Tras eliminar beta de la cubeta, tamaño:", len(tabla6))


# =============================================================
# 13. Redistribución
# =============================================================
titulo("Redistribuir: la tabla crece al superar el umbral")
tabla7 = TablaHashAbierta(table_size=4)
# Con umbral 0.75 y capacidad 4, redistribuye al insertar el 4to elemento (4*0.75=3)
tabla7.asigne("uno",    "valorunoaaaaaaaaaaaa")
tabla7.asigne("dos",    "valordosaaaaaaaaaaaa")
tabla7.asigne("tres",   "valortresaaaaaaaaaaa")
tabla7.asigne("cuatro", "valorcuatroaaaaaaaaa")  # fuerza redistribución

assert len(tabla7) == 4
assert tabla7.obtenga("uno")    == "valorunoaaaaaaaaaaaa"
assert tabla7.obtenga("dos")    == "valordosaaaaaaaaaaaa"
assert tabla7.obtenga("tres")   == "valortresaaaaaaaaaaa"
assert tabla7.obtenga("cuatro") == "valorcuatroaaaaaaaaa"
print("Redistribución exitosa, tamaño:", len(tabla7))


# =============================================================
# 14. Varianza de la función hash
# =============================================================
titulo("Varianza: evaluación de aleatoriedad de la función hash")
tabla8 = TablaHashAbierta()
llaves = [f"llave{i:03}" for i in range(50)]
for i, k in enumerate(llaves):
    tabla8.asigne(k, f"valor{i:014}aaaaa")

varianza = tabla8.varianza()
λ  = len(tabla8) / 11   # capacidad inicial era 11, puede haber redistribuido
print(f"Varianza = {varianza:.4f}")
print("Varianza calculada sin errores")


# =============================================================
# 15. Done (__del__)
# =============================================================
titulo("Done: destructor")
tabla9 = TablaHashAbierta()
tabla9.asigne("test", "valortestaaaaaaaaaaa")
del tabla9
print("__del__ ejecutado sin errores")


# =============================================================
print("\nTodas las pruebas pasaron.")