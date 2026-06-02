from tarea1.arreglo import Array
from tarea1.funcion import Funcion, validar_llave, validar_par


class Nodo:
    RANGO_INICIO   = ord("0")
    RANGO_FIN      = ord("z")
    TAMANO_ARREGLO = RANGO_FIN - RANGO_INICIO + 1

    def __init__(self):
        self.hijos    = Array(None, Nodo.TAMANO_ARREGLO)
        self.valor:   str | None = None
        self.es_final: bool = False

    @staticmethod
    def char_a_indice(caracter):
        indice = ord(caracter) - Nodo.RANGO_INICIO
        if indice < 0 or indice >= Nodo.TAMANO_ARREGLO:
            raise ValueError("La llave debe usar caracteres alfanumericos ASCII.")
        return indice

    @staticmethod
    def indice_a_char(indice):
        return chr(indice + Nodo.RANGO_INICIO)

    def tiene_hijos(self):
        for indice in range(Nodo.TAMANO_ARREGLO):
            if self.hijos[indice] is not None:
                return True
        return False


class TrieArreglos(Funcion):

    def __init__(self):
        self.__raiz   = Nodo()
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
            indice = Nodo.char_a_indice(caracter)
            if nodo.hijos[indice] is None:
                nodo.hijos[indice] = Nodo()
            nodo = nodo.hijos[indice]
        if not nodo.es_final:
            self.__tamano += 1
        nodo.es_final = True
        nodo.valor = valor

    # Elimine
    def __eliminar(self, nodo: Nodo, llave, posicion):
        if posicion == len(llave):
            if not nodo.es_final:
                return False, False  # la llave no existe, no hacer nada
            nodo.es_final = False
            nodo.valor    = None
            self.__tamano -= 1
            # El nodo puede borrarse si no tiene hijos
            return True, not nodo.tiene_hijos()

        indice = Nodo.char_a_indice(llave[posicion])
        hijo   = nodo.hijos[indice]
        if hijo is None:
            return False, False

        eliminado, borrar_hijo = self.__eliminar(hijo, llave, posicion + 1)
        if borrar_hijo:
            # Desenlazar el hijo si quedó vacío
            nodo.hijos[indice] = None

        borrar_nodo = not nodo.es_final and not nodo.tiene_hijos()
        return eliminado, borrar_nodo

    def elimine(self, llave):
        validar_llave(llave)
        self.__eliminar(self.__raiz, llave, 0)

    # Limpie
    def limpie(self):
        self.__raiz   = Nodo()
        self.__tamano = 0

    # Obtenga
    def obtenga(self, llave):
        validar_llave(llave)
        nodo = self.__raiz
        for caracter in llave:
            indice = Nodo.char_a_indice(caracter)
            nodo   = nodo.hijos[indice]
            if nodo is None:
                return None  # indicador de ausencia
        if nodo.es_final:
            return nodo.valor
        return None

    # Llaves
    def __recorrer(self, nodo: Nodo, prefijo, llaves):
        if nodo.es_final:
            llaves.append(prefijo)
        for indice in range(Nodo.TAMANO_ARREGLO):
            hijo = nodo.hijos[indice]
            if hijo is not None:
                self.__recorrer(hijo, prefijo + Nodo.indice_a_char(indice), llaves)

    def llaves(self):
        resultado = []
        self.__recorrer(self.__raiz, "", resultado)
        return resultado

    # Imprima
    def imprima(self):
        for llave in self.llaves():
            print(f"{llave}: {self.obtenga(llave)}")

    # __str__
    def __str__(self) -> str:
        pares = [f"{llave}: {self.obtenga(llave)}" for llave in self.llaves()]
        return "{" + ", ".join(pares) + "}"

    # Done
    def __del__(self):
        self.limpie()
