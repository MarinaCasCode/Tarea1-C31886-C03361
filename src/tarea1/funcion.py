ffrom abc import ABC, abstractmethod
from dataclasses import dataclass
import string


MAX_LONGITUD_LLAVE = 20
LONGITUD_VALOR = 20
ALFABETO_LLAVE = set(string.ascii_letters + string.digits)
ALFABETO_VALOR = set(string.ascii_lowercase)


def validar_llave(llave: str) -> None:
    """Valida las restricciones del enunciado para las llaves."""
    if not isinstance(llave, str):
        raise ValueError("La llave debe ser una hilera.")
    if not 0 < len(llave) <= MAX_LONGITUD_LLAVE:
        raise ValueError("La llave debe tener entre 1 y 20 caracteres.")
    if any(caracter not in ALFABETO_LLAVE for caracter in llave):
        raise ValueError("La llave debe ser alfanumerica ASCII.")


def validar_valor(valor: str) -> None:
    """Valida las restricciones del enunciado para los valores."""
    if not isinstance(valor, str):
        raise ValueError("El valor debe ser una hilera.")
    if len(valor) != LONGITUD_VALOR:
        raise ValueError("El valor debe tener exactamente 20 caracteres.")
    if any(caracter not in ALFABETO_VALOR for caracter in valor):
        raise ValueError("El valor debe usar letras en el rango 'a'..'z'.")


def validar_par(llave: str, valor: str) -> None:
    validar_llave(llave)
    validar_valor(valor)

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
