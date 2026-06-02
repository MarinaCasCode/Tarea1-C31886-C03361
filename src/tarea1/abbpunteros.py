ffrom tarea1.funcion import Funcion, Par, validar_llave, validar_par


class NodoABB:
    def __init__(self, elemento: Par):
        self.elemento = elemento
        self.izquierdo: "NodoABB | None" = None
        self.derecho:   "NodoABB | None" = None


class AbbPunteros(Funcion):

    def __init__(self):
        self.__raiz:   NodoABB | None = None
        self.__tamano: int = 0

    def __len__(self):
        return self.__tamano

    def __getitem__(self, llave):
        return self.obtenga(llave)

    # Asigne
    def asigne(self, llave, valor):
        validar_par(llave, valor)
        elemento = Par(llave, valor)
        if self.__raiz is None:
            self.__raiz = NodoABB(elemento)
            self.__tamano = 1
            return

        # Recorrido iterativo hasta encontrar posición o llave existente
        nodo = self.__raiz
        while True:
            if llave == nodo.elemento.llave:
                # La llave ya existe, actualizar valor
                nodo.elemento.valor = valor
                return
            if llave < nodo.elemento.llave:
                if nodo.izquierdo is None:
                    nodo.izquierdo = NodoABB(elemento)
                    self.__tamano += 1
                    return
                nodo = nodo.izquierdo
            else:
                if nodo.derecho is None:
                    nodo.derecho = NodoABB(elemento)
                    self.__tamano += 1
                    return
                nodo = nodo.derecho

    # Elimine
    def __extraer_minimo(self, nodo: NodoABB):
        # Retorna (elemento_minimo, nuevo_subarbol_sin_ese_nodo)
        if nodo.izquierdo is None:
            return nodo.elemento, nodo.derecho
        elemento, nodo.izquierdo = self.__extraer_minimo(nodo.izquierdo)
        return elemento, nodo

    def __eliminar(self, nodo: "NodoABB | None", llave):
        if nodo is None:
            return None, False

        if llave < nodo.elemento.llave:
            nodo.izquierdo, eliminado = self.__eliminar(nodo.izquierdo, llave)
            return nodo, eliminado
        if llave > nodo.elemento.llave:
            nodo.derecho, eliminado = self.__eliminar(nodo.derecho, llave)
            return nodo, eliminado

        # Caso 1: sin hijo izquierdo
        if nodo.izquierdo is None:
            return nodo.derecho, True
        # Caso 2: sin hijo derecho
        if nodo.derecho is None:
            return nodo.izquierdo, True

        # Caso 3: dos hijos, reemplazar con sucesor inorden
        sucesor, nodo.derecho = self.__extraer_minimo(nodo.derecho)
        nodo.elemento = sucesor
        return nodo, True

    def elimine(self, llave):
        validar_llave(llave)
        self.__raiz, eliminado = self.__eliminar(self.__raiz, llave)
        if eliminado:
            self.__tamano -= 1

    # Limpie
    def limpie(self):
        self.__raiz   = None
        self.__tamano = 0

    # Obtenga
    def obtenga(self, llave):
        validar_llave(llave)
        nodo = self.__raiz
        while nodo is not None:
            if llave == nodo.elemento.llave:
                return nodo.elemento.valor
            if llave < nodo.elemento.llave:
                nodo = nodo.izquierdo
            else:
                nodo = nodo.derecho
        return None  # indicador de ausencia

    # Llaves (inorden)
    def __recorrer_en_orden(self, nodo: "NodoABB | None", pares):
        if nodo is None:
            return
        self.__recorrer_en_orden(nodo.izquierdo, pares)
        pares.append(nodo.elemento)
        self.__recorrer_en_orden(nodo.derecho, pares)

    def __pares_en_orden(self):
        pares = []
        self.__recorrer_en_orden(self.__raiz, pares)
        return pares

    def llaves(self):
        return [par.llave for par in self.__pares_en_orden()]

    # Imprima
    def imprima(self):
        for par in self.__pares_en_orden():
            print(f"{par.llave}: {par.valor}")

    # __str__
    def __str__(self) -> str:
        pares = [f"{par.llave}: {par.valor}" for par in self.__pares_en_orden()]
        return "{" + ", ".join(pares) + "}"

    # Done
    def __del__(self):
        self.limpie()
