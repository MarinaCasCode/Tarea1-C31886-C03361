from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Par:
    llave: str
    valor: str

    def __gt__(self, other: "Par") -> bool:
        return self.llave > other.llave

    def __lt__(self, other: "Par") -> bool:
        return self.llave < other.llave

class Funcion(ABC):
    """
    Clase abstracta Funcion. Dicta los métodos que deben tener las funciones.
    
    """
    @abstractmethod
    def asigne(self, llave, valor):
        """
        Inserta una relación. Valor puede ya estar asociado a otra llave.
        """
        pass

    @abstractmethod
    def elimine(self, llave):
        pass

    @abstractmethod
    def limpie(self):
        pass

    @abstractmethod
    def obtenga(self, llave):
        pass

    @abstractmethod
    def llaves(self):
        pass

    @abstractmethod
    def imprima(self):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass
