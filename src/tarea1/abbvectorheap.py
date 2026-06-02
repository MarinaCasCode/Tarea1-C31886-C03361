from tarea1.funcion import Funcion, Par, validar_llave, validar_par


class ABBVectorHeap(Funcion):

    def __init__(self):
        # Diccionario {índice: Par} - la raíz está en índice 0
        self.__arbol: dict[int, Par] = {}
        self.__tamano: int = 0

    def __len__(self):
        return self.__tamano

    def __getitem__(self, llave):
        return self.obtenga(llave)

    # Helpers de índices
    def __izquierdo(self, indice):
        return 2 * indice + 1

    def __derecho(self, indice):
        return 2 * indice + 2

    # Asigne
    def asigne(self, llave, valor):
        validar_par(llave, valor)
        indice = 0
        while indice in self.__arbol:
            par = self.__arbol[indice]
            if llave == par.llave:
                # La llave ya existe, actualizar valor
                par.valor = valor
                return
            if llave < par.llave:
                indice = self.__izquierdo(indice)
            else:
                indice = self.__derecho(indice)

        self.__arbol[indice] = Par(llave, valor)
        self.__tamano += 1

    # Elimine
    def __indice_llave(self, llave):
        # Retorna el índice del nodo con esa llave, o None si no existe
        indice = 0
        while indice in self.__arbol:
            par = self.__arbol[indice]
            if llave == par.llave:
                return indice
            if llave < par.llave:
                indice = self.__izquierdo(indice)
            else:
                indice = self.__derecho(indice)
        return None

    def __indice_minimo(self, indice):
        # Retorna el índice del nodo con la llave mínima del subárbol
        while self.__izquierdo(indice) in self.__arbol:
            indice = self.__izquierdo(indice)
        return indice

    def __mover_subarbol(self, origen, destino):
        # Mueve recursivamente el subárbol de origen a destino
        self.__arbol[destino] = self.__arbol.pop(origen)
        iz_o, der_o = self.__izquierdo(origen), self.__derecho(origen)
        iz_d, der_d = self.__izquierdo(destino), self.__derecho(destino)
        if iz_o in self.__arbol:
            self.__mover_subarbol(iz_o, iz_d)
        if der_o in self.__arbol:
            self.__mover_subarbol(der_o, der_d)

    def __eliminar_indice(self, indice):
        izquierdo = self.__izquierdo(indice)
        derecho   = self.__derecho(indice)
        tiene_iz  = izquierdo in self.__arbol
        tiene_der = derecho   in self.__arbol

        if not tiene_iz and not tiene_der:
            # Caso 1: hoja
            del self.__arbol[indice]
        elif tiene_iz and not tiene_der:
            # Caso 2: solo hijo izquierdo
            del self.__arbol[indice]
            self.__mover_subarbol(izquierdo, indice)
        elif tiene_der and not tiene_iz:
            # Caso 2: solo hijo derecho
            del self.__arbol[indice]
            self.__mover_subarbol(derecho, indice)
        else:
            # Caso 3: dos hijos, reemplazar con sucesor inorden
            sucesor = self.__indice_minimo(derecho)
            self.__arbol[indice] = self.__arbol[sucesor]
            self.__eliminar_indice(sucesor)

    def elimine(self, llave):
        validar_llave(llave)
        indice = self.__indice_llave(llave)
        if indice is None:
            return  # la llave no existe, no hacer nada
        self.__eliminar_indice(indice)
        self.__tamano -= 1

    # Limpie
    def limpie(self):
        self.__arbol  = {}
        self.__tamano = 0

    # Obtenga
    def obtenga(self, llave):
        validar_llave(llave)
        indice = self.__indice_llave(llave)
        if indice is None:
            return None  # indicador de ausencia
        return self.__arbol[indice].valor

    # Llaves (inorden)
    def __recorrer_en_orden(self, indice, pares):
        if indice not in self.__arbol:
            return
        self.__recorrer_en_orden(self.__izquierdo(indice), pares)
        pares.append(self.__arbol[indice])
        self.__recorrer_en_orden(self.__derecho(indice), pares)

    def __pares_en_orden(self):
        pares = []
        self.__recorrer_en_orden(0, pares)
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
