from tarea1.funcion import Funcion, validar_llave, validar_par


class NodoTrie:
    def __init__(self):
        self.hijos: dict[str, "NodoTrie"] = {}
        self.valor: str | None = None
        self.es_final: bool = False


class TriePunteros(Funcion):

    def __init__(self):
        self.__raiz   = NodoTrie()
        self.__tamano = 0

    def __len__(self):
        return self.__tamano

    def __getitem__(self, llave):
        return self.obtenga(llave)

    # Asigne
    def asigne(self, llave, valor):
        validar_par(llave, valor)
        nodo = self.__raiz
        for caracter in llave:
            if caracter not in nodo.hijos:
                nodo.hijos[caracter] = NodoTrie()
            nodo = nodo.hijos[caracter]
        if not nodo.es_final:
            self.__tamano += 1
        nodo.es_final = True
        nodo.valor = valor

    # Elimine
    def __eliminar(self, nodo: NodoTrie, llave, posicion):
        if posicion == len(llave):
            if not nodo.es_final:
                return False, False  # la llave no existe, no hacer nada
            nodo.es_final = False
            nodo.valor = None
            self.__tamano -= 1
            # El nodo puede borrarse si no tiene hijos
            return True, len(nodo.hijos) == 0

        caracter = llave[posicion]
        hijo = nodo.hijos.get(caracter)
        if hijo is None:
            return False, False

        eliminado, borrar_hijo = self.__eliminar(hijo, llave, posicion + 1)
        if borrar_hijo:
            # Desenlazar el hijo si quedó vacío
            del nodo.hijos[caracter]

        borrar_nodo = not nodo.es_final and len(nodo.hijos) == 0
        return eliminado, borrar_nodo

    def elimine(self, llave):
        validar_llave(llave)
        self.__eliminar(self.__raiz, llave, 0)

    # Limpie
    def limpie(self):
        self.__raiz   = NodoTrie()
        self.__tamano = 0

    # Obtenga
    def obtenga(self, llave):
        validar_llave(llave)
        nodo = self.__raiz
        for caracter in llave:
            nodo = nodo.hijos.get(caracter)
            if nodo is None:
                return None  # indicador de ausencia
        if nodo.es_final:
            return nodo.valor
        return None

    # Llaves
    def __recorrer(self, nodo: NodoTrie, prefijo, llaves):
        if nodo.es_final:
            llaves.append(prefijo)
        for caracter in sorted(nodo.hijos):  # sorted garantiza orden lexicográfico
            self.__recorrer(nodo.hijos[caracter], prefijo + caracter, llaves)

    def llaves(self):
        resultado = []
        self.__recorrer(self.__raiz, "", resultado)
        return resultado

    # Imprima
    def imprima(self):
        for llave in self.llaves():
            print(f"{llave}: {self.obtenga(llave)}")

    #  __str__
    def __str__(self) -> str:
        pares = [f"{llave}: {self.obtenga(llave)}" for llave in self.llaves()]
        return "{" + ", ".join(pares) + "}"

    # Done
    def __del__(self):
        self.limpie()
