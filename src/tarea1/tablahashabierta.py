from tarea1.funcion import Funcion

class TablaHashAbierta(Funcion):
    
    def __init__(self, table_size=101):
        self.table_size = table_size
        self.table = [[] for _ in range(table_size)] 
    # 🔹 Función hash (polinomial)
    def hash_func(self, key: str) -> int:
        hash_value = 0
        p = 31  

        for char in key:
            hash_value = (hash_value * p + ord(char)) % self.table_size

        return hash_value