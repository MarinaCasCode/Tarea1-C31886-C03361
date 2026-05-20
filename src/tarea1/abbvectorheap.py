from tarea1.funcion import Funcion

CAPACIDAD_INICIAL = 100


class ABBVectorHeap(Funcion):

    def __init__(self, capacidad=CAPACIDAD_INICIAL):
        # Índice 0 no se usa; la raíz está en índice 1
        self.__llaves  = [None] * (capacidad + 1)
        self.__valores = [None] * (capacidad + 1)
        self.__tamaño  = 0
        self.__capacidad = capacidad

    def __len__(self):
        return self.__tamaño

    def __getitem__(self, llave):
        return self.obtenga(llave)

    # Redimensionar
    def __redimensionar(self):
        self.__capacidad *= 2
        self.__llaves  += [None] * (self.__capacidad // 2 + 1)
        self.__valores += [None] * (self.__capacidad // 2 + 1)

    # Asigne
    def __insertar(self, índice: int, llave: str, valor: str) -> bool:
        # Retorna True si insertó un nodo nuevo, False si actualizó
        if self.__llaves[índice] is None:
            self.__llaves[índice]  = llave
            self.__valores[índice] = valor
            return True
        if llave < self.__llaves[índice]:
            hijo = índice * 2
            if hijo > self.__capacidad:
                self.__redimensionar()
            return self.__insertar(hijo, llave, valor)
        elif llave > self.__llaves[índice]:
            hijo = índice * 2 + 1
            if hijo > self.__capacidad:
                self.__redimensionar()
            return self.__insertar(hijo, llave, valor)
        else:
            # La llave ya existe → actualizar valor
            self.__valores[índice] = valor
            return False

    def asigne(self, llave, valor):
        if self.__tamaño >= self.__capacidad:
            self.__redimensionar()
        if self.__insertar(1, llave, valor):
            self.__tamaño += 1

    # Elimine 
    def __minimo_índice(self, índice: int) -> int:
        # Retorna el índice del nodo con la llave mínima del subárbol
        while self.__llaves[índice * 2] is not None and índice * 2 <= self.__capacidad:
            índice = índice * 2
        return índice

    def __eliminar(self, índice: int, llave: str) -> bool:
        if índice > self.__capacidad or self.__llaves[índice] is None:
            return False  # la llave no existe
        if llave < self.__llaves[índice]:
            return self.__eliminar(índice * 2, llave)
        elif llave > self.__llaves[índice]:
            return self.__eliminar(índice * 2 + 1, llave)
        else:
            iz = índice * 2
            der = índice * 2 + 1
            tiene_iz  = iz  <= self.__capacidad and self.__llaves[iz]  is not None
            tiene_der = der <= self.__capacidad and self.__llaves[der] is not None

            if not tiene_iz and not tiene_der:
                # Caso 1: hoja
                self.__llaves[índice]  = None
                self.__valores[índice] = None
            elif not tiene_iz:
                # Caso 2: solo hijo derecho, subir subárbol derecho
                self.__subir_subárbol(der, índice)
            elif not tiene_der:
                # Caso 2: solo hijo izquierdo, subir subárbol izquierdo
                self.__subir_subárbol(iz, índice)
            else:
                # Caso 3: dos hijos, reemplazar con sucesor inorden
                sucesor = self.__minimo_índice(der)
                self.__llaves[índice]  = self.__llaves[sucesor]
                self.__valores[índice] = self.__valores[sucesor]
                self.__eliminar(der, self.__llaves[sucesor])
                return True  # ya restó tamaño en la llamada recursiva
            return True

    def __subir_subárbol(self, origen: int, destino: int):
        # Copia el subárbol de origen a destino recursivamente
        if origen > self.__capacidad or self.__llaves[origen] is None:
            self.__llaves[destino]  = None
            self.__valores[destino] = None
            return
        self.__llaves[destino]  = self.__llaves[origen]
        self.__valores[destino] = self.__valores[origen]
        self.__llaves[origen]   = None
        self.__valores[origen]  = None
        self.__subir_subárbol(origen * 2,     destino * 2)
        self.__subir_subárbol(origen * 2 + 1, destino * 2 + 1)

    def elimine(self, llave):
        if self.__eliminar(1, llave):
            self.__tamaño -= 1

    # Limpie
    def limpie(self):
        self.__llaves  = [None] * (self.__capacidad + 1)
        self.__valores = [None] * (self.__capacidad + 1)
        self.__tamaño  = 0

    # Obtenga
    def obtenga(self, llave):
        índice = 1
        while índice <= self.__capacidad and self.__llaves[índice] is not None:
            if llave < self.__llaves[índice]:
                índice = índice * 2
            elif llave > self.__llaves[índice]:
                índice = índice * 2 + 1
            else:
                return self.__valores[índice]
        return None  # indicador de ausencia

    # Llaves (inorden)
    def __inorden(self, índice: int, resultado: list):
        if índice > self.__capacidad or self.__llaves[índice] is None:
            return
        self.__inorden(índice * 2, resultado)
        resultado.append(self.__llaves[índice])
        self.__inorden(índice * 2 + 1, resultado)

    def llaves(self):
        resultado = []
        self.__inorden(1, resultado)
        return resultado

    # Imprima
    def __imprimir_inorden(self, índice: int):
        if índice > self.__capacidad or self.__llaves[índice] is None:
            return
        self.__imprimir_inorden(índice * 2)
        print(f"{self.__llaves[índice]}: {self.__valores[índice]}")
        self.__imprimir_inorden(índice * 2 + 1)

    def imprima(self):
        self.__imprimir_inorden(1)

    # __str__
    def __str__(self) -> str:
        pares = []
        self.__inorden_str(1, pares)
        return "{" + ", ".join(pares) + "}"

    def __inorden_str(self, índice: int, pares: list):
        if índice > self.__capacidad or self.__llaves[índice] is None:
            return
        self.__inorden_str(índice * 2, pares)
        pares.append(f"{self.__llaves[índice]}: {self.__valores[índice]}")
        self.__inorden_str(índice * 2 + 1, pares)

    # Done
    def __del__(self):
        self.limpie()