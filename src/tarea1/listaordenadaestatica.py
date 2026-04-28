from tarea1.funcion import Funcion
from tarea1.arreglo import Array

TAMAÑO_INICIAL = 100

class ListaOrdenadaEstática(Funcion):
    def __init__(self, tamaño=TAMAÑO_INICIAL):
        self.__arreglo: Array = Array(valor_inicial=None, tamaño=tamaño)
        self.__último: int | None = None

    def __len__(self):
        if self.__último is None:
            return 0
        else:
            return self.__último + 1

    def __getitem__(self, llave):
        return self.obtenga(llave)

    def __buscar(self, llave: str) -> int:
        # Búsqueda binaria retorna el índice donde está o debería estar la llave
        inicio = 0
        fin = len(self) - 1
        while inicio <= fin:
            medio = (inicio + fin) // 2
            llave_medio = self.__arreglo[medio][0]
            if llave_medio == llave:
                return medio
            elif llave_medio < llave:
                inicio = medio + 1
            else:
                fin = medio - 1
        return inicio

    def __redimensionar(self):
        tamaño_nuevo = len(self.__arreglo) * 2
        arreglo_nuevo = Array(valor_inicial=None, tamaño=tamaño_nuevo)
        for i in range(len(self)):
            arreglo_nuevo[i] = self.__arreglo[i]
        self.__arreglo = arreglo_nuevo

    def asigne(self, llave, valor):
        índice = self.__buscar(llave)

        # Si la llave ya existe actualizar valor
        if índice < len(self) and self.__arreglo[índice] is not None and self.__arreglo[índice][0] == llave:
            self.__arreglo[índice] = (llave, valor)
            return

        # Redimensionar si no hay espacio
        if len(self) == len(self.__arreglo):
            self.__redimensionar()

        # Desplazar elementos a la derecha para hacer espacio
        if self.__último is None:
            self.__último = 0
        else:
            self.__último += 1
            for i in range(self.__último, índice, -1):
                self.__arreglo[i] = self.__arreglo[i - 1]

        self.__arreglo[índice] = (llave, valor)

    def elimine(self, llave):
        índice = self.__buscar(llave)

        # La llave no existe no hacer nada
        if índice >= len(self) or self.__arreglo[índice] is None or self.__arreglo[índice][0] != llave:
            return

        # Desplazar elementos a la izquierda
        for i in range(índice, self.__último):
            self.__arreglo[i] = self.__arreglo[i + 1]
        self.__arreglo[self.__último] = None

        if self.__último == 0:
            self.__último = None
        else:
            self.__último -= 1

    def limpie(self):
        for i in range(len(self)):
            self.__arreglo[i] = None
        self.__último = None

    def obtenga(self, llave):
        índice = self.__buscar(llave)
        if índice < len(self) and self.__arreglo[índice] is not None and self.__arreglo[índice][0] == llave:
            return self.__arreglo[índice][1]
        return None

    def llaves(self):
        resultado = []
        for i in range(len(self)):
            resultado.append(self.__arreglo[i][0])
        return resultado

    def imprima(self):
        for i in range(len(self)):
            print(f"{self.__arreglo[i][0]}: {self.__arreglo[i][1]}")

    def __str__(self) -> str:
        pares = []
        for i in range(len(self)):
            pares.append(f"{self.__arreglo[i][0]}: {self.__arreglo[i][1]}")
        return "{" + ", ".join(pares) + "}"

    def __del__(self):
        self.limpie()