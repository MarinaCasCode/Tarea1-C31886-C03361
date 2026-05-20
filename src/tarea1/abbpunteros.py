from tarea1.funcion import Funcion


class Nodo:
    def __init__(self, llave: str, valor: str):
        self.llave = llave
        self.valor = valor
        self.izquierdo: "Nodo | None" = None
        self.derecho:   "Nodo | None" = None


class AbbPunteros(Funcion):

    def __init__(self):
        self.__raíz: Nodo | None = None
        self.__tamaño: int = 0

    def __len__(self):
        return self.__tamaño

    def __getitem__(self, llave):
        return self.obtenga(llave)

    # Asigne
    def __insertar(self, nodo: Nodo | None, llave: str, valor: str) -> tuple[Nodo, bool]:
        # Retorna (nodo_raíz, fue_insertado_nuevo)
        if nodo is None:
            return Nodo(llave, valor), True
        if llave < nodo.llave:
            nodo.izquierdo, nuevo = self.__insertar(nodo.izquierdo, llave, valor)
        elif llave > nodo.llave:
            nodo.derecho, nuevo = self.__insertar(nodo.derecho, llave, valor)
        else:
            # La llave ya existe, actualizar valor
            nodo.valor = valor
            nuevo = False
        return nodo, nuevo

    def asigne(self, llave, valor):
        self.__raíz, nuevo = self.__insertar(self.__raíz, llave, valor)
        if nuevo:
            self.__tamaño += 1

    # Elimine
    def __minimo(self, nodo: Nodo) -> Nodo:
        # Retorna el nodo con la llave mínima del subárbol
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo

    def __eliminar(self, nodo: Nodo | None, llave: str) -> tuple[Nodo | None, bool]:
        # Retorna (nodo_raíz, fue_eliminado)
        if nodo is None:
            return None, False  # la llave no existe
        if llave < nodo.llave:
            nodo.izquierdo, eliminado = self.__eliminar(nodo.izquierdo, llave)
        elif llave > nodo.llave:
            nodo.derecho, eliminado = self.__eliminar(nodo.derecho, llave)
        else:
            eliminado = True
            if nodo.izquierdo is None:
                # Caso 1: sin hijo izquierdo
                return nodo.derecho, eliminado
            elif nodo.derecho is None:
                # Caso 2: sin hijo derecho
                return nodo.izquierdo, eliminado
            else:
                # Caso 3: dos hijos, reemplazar con sucesor inorden
                sucesor = self.__minimo(nodo.derecho)
                nodo.llave = sucesor.llave
                nodo.valor = sucesor.valor
                nodo.derecho, _ = self.__eliminar(nodo.derecho, sucesor.llave)
        return nodo, eliminado

    def elimine(self, llave):
        self.__raíz, eliminado = self.__eliminar(self.__raíz, llave)
        if eliminado:
            self.__tamaño -= 1

    # Limpie
    def limpie(self):
        self.__raíz = None
        self.__tamaño = 0

    # Obtenga
    def obtenga(self, llave):
        nodo = self.__raíz
        while nodo is not None:
            if llave < nodo.llave:
                nodo = nodo.izquierdo
            elif llave > nodo.llave:
                nodo = nodo.derecho
            else:
                return nodo.valor
        return None  # indicador de ausencia

    # Llaves (inorden)
    def __inorden(self, nodo: Nodo | None, resultado: list) -> None:
        if nodo is None:
            return
        self.__inorden(nodo.izquierdo, resultado)
        resultado.append(nodo.llave)
        self.__inorden(nodo.derecho, resultado)

    def llaves(self):
        resultado = []
        self.__inorden(self.__raíz, resultado)
        return resultado

    # Imprima
    def __imprimir_inorden(self, nodo: Nodo | None) -> None:
        if nodo is None:
            return
        self.__imprimir_inorden(nodo.izquierdo)
        print(f"{nodo.llave}: {nodo.valor}")
        self.__imprimir_inorden(nodo.derecho)

    def imprima(self):
        self.__imprimir_inorden(self.__raíz)

    # __str__
    def __str__(self) -> str:
        pares = []
        self.__inorden_str(self.__raíz, pares)
        return "{" + ", ".join(pares) + "}"

    def __inorden_str(self, nodo: Nodo | None, pares: list) -> None:
        if nodo is None:
            return
        self.__inorden_str(nodo.izquierdo, pares)
        pares.append(f"{nodo.llave}: {nodo.valor}")
        self.__inorden_str(nodo.derecho, pares)

    # Done
    def __del__(self):
        self.limpie()