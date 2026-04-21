from tarea1.funcion import Par
from tarea1.funcion import Funcion

class Nodo:
    def __init__(self, elemento: Par | None = None):
        self.elemento = elemento
        self.siguiente: Nodo | None = None

class ListaOrdenadaDinámica(Funcion):
    def __init__(self):
        self.__cabeza = Nodo()
        self.__tamaño = 0

    def __len__(self):
        return self.__tamaño
    
    def __getitem__(self, llave: str):
        pass

    def asigne(self, llave, valor):
        elemento = Par(llave, valor)
        referencia: Nodo = self.__cabeza
        nodo = Nodo(elemento)
        if referencia.siguiente is None:
            referencia.siguiente = nodo
        else:
            while referencia.siguiente.siguiente is not None and elemento > referencia.siguiente.elemento:
                referencia = referencia.siguiente
            nodo.siguiente = referencia.siguiente
            referencia.siguiente = nodo

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
        pass
    
    def __del__(self):
        pass