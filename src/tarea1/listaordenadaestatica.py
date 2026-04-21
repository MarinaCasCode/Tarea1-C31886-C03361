from tarea1.funcion import Funcion
from tarea1.arreglo import Array

class ListaOrdenadaEstática(Funcion):
    def __init__(self, tamaño):
        self.__arreglo: Array = Array(valor_inicial=0, tamaño=tamaño)
        self.__último: int | None = None

    def __len__(self):
        if self.__último is None:
            return 0
        else:
            return self.__último + 1
    
    def __getitem__(self, llave):
        pass

    def asigne(self, llave, valor):
        pass

    def elimine(self, llave):
        pass

    def limpie(self):
        pass

    def obtenga(self, llave):
        pass

    def llaves(self):
        pass

    def imprima(self):
        pass

    def __str__(self) -> str:
        return str(self.__arreglo)
    
    def __del__(self):
        pass