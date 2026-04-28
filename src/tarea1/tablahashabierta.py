from tarea1.funcion import Funcion

UMBRAL_CARGA = 0.75


class TablaHashAbierta(Funcion):
    def __init__(self, table_size=11):
        self.table_size = table_size
        self.table = [[] for _ in range(table_size)]
        self.__tamaño = 0

    def __len__(self):
        return self.__tamaño

    def __getitem__(self, llave):
        return self.obtenga(llave)

    # Función hash polinomial con multiplicador 31 descrita en index.md
    def hash_func(self, key: str) -> int:
        hash_value = 0
        p = 31
        for char in key:
            hash_value = (hash_value * p + ord(char)) % self.table_size
        return hash_value

    def __factor_carga(self) -> float:
        return self.__tamaño / self.table_size

    def __redistribuir(self) -> None:
        table_size_nueva = self.table_size * 2
        table_nueva = [[] for _ in range(table_size_nueva)]

        # Reinsertar todos los pares con la nueva capacidad
        for cubeta in self.table:
            for llave, valor in cubeta:
                h = 0
                for c in llave:
                    h = (h * 31 + ord(c)) % table_size_nueva
                table_nueva[h].append((llave, valor))

        self.table = table_nueva
        self.table_size = table_size_nueva

    def asigne(self, llave, valor):
        # Redistribuir si se supera el umbral de carga
        if self.__factor_carga() >= UMBRAL_CARGA:
            self.__redistribuir()

        índice = self.hash_func(llave)
        cubeta = self.table[índice]

        # Si la llave ya existe → actualizar valor
        for i, (k, _) in enumerate(cubeta):
            if k == llave:
                cubeta[i] = (llave, valor)
                return

        cubeta.append((llave, valor))
        self.__tamaño += 1

    def elimine(self, llave):
        índice = self.hash_func(llave)
        cubeta = self.table[índice]

        for i, (k, _) in enumerate(cubeta):
            if k == llave:
                cubeta.pop(i)
                self.__tamaño -= 1
                return
        # La llave no existe no hacer nada

    def limpie(self):
        self.table = [[] for _ in range(self.table_size)]
        self.__tamaño = 0

    def obtenga(self, llave):
        índice = self.hash_func(llave)
        for k, v in self.table[índice]:
            if k == llave:
                return v
        return None  # indicador de ausencia

    def llaves(self):
        resultado = []
        for cubeta in self.table:
            for k, _ in cubeta:
                resultado.append(k)
        return resultado

    def imprima(self):
        for cubeta in self.table:
            for k, v in cubeta:
                print(f"{k}: {v}")

    def __str__(self) -> str:
        pares = []
        for cubeta in self.table:
            for k, v in cubeta:
                pares.append(f"{k}: {v}")
        return "{" + ", ".join(pares) + "}"

    def varianza(self) -> float:
        # Evaluación de aleatoriedad descrita en index.md sección 3.2
        # σ² = (1/m) · Σ (cᵢ − λ)²
        factor = self.__factor_carga()
        return sum((len(c) - factor) ** 2 for c in self.table) / self.table_size

    def __del__(self):
        if hasattr(self, 'table'):
            self.limpie()