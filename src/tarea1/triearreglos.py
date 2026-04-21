from tarea1.funcion import Funcion
from tarea1.arreglo import Array

class Nodo:
    """
    Representa un nodo del Trie.
    Cada nodo contiene un arreglo de tamaño fijo (27 posiciones: 'a'-'z' + '{')
    que empareja caracteres a otros nodos.
    """
    
    # Constantes para el rango de caracteres
    RANGO_INICIO = ord('0')  # 48
    RANGO_FIN = ord('{')     # 123
    TAMAÑO_ARREGLO = RANGO_FIN - RANGO_INICIO + 1  # 5 posiciones
    
    def __init__(self):
        """
        Crea un nuevo nodo con un arreglo de 75 posiciones (0-z + {).
        Todas las posiciones se inicializan en None.        
        """
        # Arreglo de tamaño fijo: índice 0='0', 1='1', ..., 73='z', 74='{'
        self.hijos = Array(valor_inicial=None, tamaño=Nodo.TAMAÑO_ARREGLO)
    
    @staticmethod
    def char_a_indice(caracter):
        """
        Convierte un carácter ('0'-'z' o '{') a un índice del arreglo (0-74).
        
        Args:
            caracter (str): Carácter a convertir
            
        Returns:
            int: Índice correspondiente en el arreglo
        """
        return ord(caracter) - Nodo.RANGO_INICIO
    
    @staticmethod
    def indice_a_char(indice):
        """
        Convierte un índice del arreglo (0-74) a un carácter ('a'-'z' o '{').
        
        Args:
            indice (int): Índice del arreglo
            
        Returns:
            str: Carácter correspondiente
        """
        return chr(indice + Nodo.RANGO_INICIO)
    
    def tiene_hijos(self):
        """
        Verifica si el nodo tiene algún hijo (excluyendo el marcador de fin '{').
        
        Returns:
            bool: True si tiene al menos un hijo no-None
        """
        for i in range(73):  # Solo verificar '0' a 'z', no el marcador '{'
            if self.hijos[i] is not None:
                return True
        return False


class TrieArreglos(Funcion):
    """
    Implementación de un Trie (árbol de prefijos) usando arreglos de tamaño fijo.
    """
    pass