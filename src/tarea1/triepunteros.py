from tarea1.funcion import Funcion


def _nodo():
    return {"hijos": {}, "valor": None}


class TriePunteros(Funcion):

    def __init__(self):
        self.__raíz   = _nodo()
        self.__tamaño = 0

    def __len__(self):
        return self.__tamaño

    def __getitem__(self, llave):
        return self.obtenga(llave)

    # Asigne
    def asigne(self, llave, valor):
        nodo = self.__raíz
        for c in llave:
            if c not in nodo["hijos"]:
                nodo["hijos"][c] = _nodo()
            nodo = nodo["hijos"][c]
        # Si la llave ya existe, actualizar valor
        if nodo["valor"] is None:
            self.__tamaño += 1
        nodo["valor"] = valor

    # Elimine
    def elimine(self, llave):
        def _borrar(nodo, llave, i):
            if i == len(llave):
                # La llave no existe, no hacer nada
                if nodo["valor"] is None:
                    return False
                nodo["valor"] = None
                self.__tamaño -= 1
                # El nodo puede borrarse si no tiene hijos
                return len(nodo["hijos"]) == 0
            c = llave[i]
            if c not in nodo["hijos"]:
                return False
            if _borrar(nodo["hijos"][c], llave, i + 1):
                # Desenlazar el hijo si quedó vacío
                del nodo["hijos"][c]
                return nodo["valor"] is None and len(nodo["hijos"]) == 0
            return False
        _borrar(self.__raíz, llave, 0)

    # Limpie 
    def limpie(self):
        self.__raíz   = _nodo()
        self.__tamaño = 0

    # Obtenga
    def obtenga(self, llave):
        nodo = self.__raíz
        for c in llave:
            if c not in nodo["hijos"]:
                return None  # indicador de ausencia
            nodo = nodo["hijos"][c]
        return nodo["valor"]

    # Llaves
    def llaves(self):
        resultado = []
        def _rec(nodo, prefijo):
            if nodo["valor"] is not None:
                resultado.append(prefijo)
            for c, hijo in nodo["hijos"].items():
                _rec(hijo, prefijo + c)
        _rec(self.__raíz, "")
        return resultado

    # Imprima
    def imprima(self):
        def _rec(nodo, prefijo):
            if nodo["valor"] is not None:
                print(f"{prefijo}: {nodo['valor']}")
            for c, hijo in nodo["hijos"].items():
                _rec(hijo, prefijo + c)
        _rec(self.__raíz, "")

    # __str__ 
    def __str__(self):
        pares = []
        def _rec(nodo, prefijo):
            if nodo["valor"] is not None:
                pares.append(f"{prefijo}: {nodo['valor']}")
            for c, hijo in nodo["hijos"].items():
                _rec(hijo, prefijo + c)
        _rec(self.__raíz, "")
        return "{" + ", ".join(pares) + "}"

    # Done
    def __del__(self):
        self.limpie()