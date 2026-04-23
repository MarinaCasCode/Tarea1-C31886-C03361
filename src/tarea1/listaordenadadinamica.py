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
        return self.obtenga(llave)

    def asigne(self, llave, valor):
        elemento = Par(llave, valor)
        referencia: Nodo = self.__cabeza
        nodo = Nodo(elemento)
        if referencia.siguiente is None:
            referencia.siguiente = nodo
            self.__tamaño += 1
        else:
            while referencia.siguiente is not None and elemento > referencia.siguiente.elemento:
                referencia = referencia.siguiente
            if referencia.siguiente is not None and referencia.siguiente.elemento.llave == llave:
                referencia.siguiente.elemento.valor = valor
                return
            nodo.siguiente = referencia.siguiente
            referencia.siguiente = nodo
            self.__tamaño += 1  

    def elimine(self, llave):
        ref: Nodo = self.__cabeza

        while ref.siguiente is not None and ref.siguiente.elemento.llave < llave:
            ref = ref.siguiente

        # La llave no existe → no hacer nada
        if ref.siguiente is None or ref.siguiente.elemento.llave != llave:
            return

        # Desenlazar el nodo
        ref.siguiente = ref.siguiente.siguiente
        self.__tamaño -= 1

    def limpie(self):
        self.__cabeza = Nodo()
        self.__tamaño = 0

    def obtenga(self, llave):
        ref: Nodo = self.__cabeza.siguiente

        while ref is not None and ref.elemento.llave < llave:
            ref = ref.siguiente

        if ref is not None and ref.elemento.llave == llave:
            return ref.elemento.valor
        
        return None

    def llaves(self):
        resultado = []
        ref: Nodo = self.__cabeza.siguiente
        while ref is not None:
            resultado.append(ref.elemento.llave)
            ref = ref.siguiente
        return resultado

    def imprima(self):
        ref: Nodo = self.__cabeza.siguiente
        while ref is not None:
            print(f"{ref.elemento.llave}: {ref.elemento.valor}")
            ref = ref.siguiente

    def __str__(self) -> str:
        pares = []
        ref: Nodo = self.__cabeza.siguiente
        while ref is not None:
            pares.append(f"{ref.elemento.llave}: {ref.elemento.valor}")
            ref = ref.siguiente
        return "{" + ", ".join(pares) + "}"
    
    def __del__(self):
        self.limpie()