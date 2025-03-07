import random

class Desafio:
    def __init__(self, numero, comprendido=False):
        self.numero = numero
        self.comprendido = comprendido

class Nodo:
    def __init__(self, desafio):
        self.desafio = desafio
        self.izq = None
        self.der = None

class Arbol:
    def __init__(self):
        self.raiz = None

    def insertar(self, nodo, desafio):
        if nodo is None:
            return Nodo(desafio)
        if desafio.numero < nodo.desafio.numero:
            nodo.izq = self.insertar(nodo.izq, desafio)
        else:
            nodo.der = self.insertar(nodo.der, desafio)
        return nodo

    def insertar_desafios(self, desafios):
        for desafio in desafios:
            self.raiz = self.insertar(self.raiz, desafio)

    def buscar(self, nodo, numero):
        if nodo is None or nodo.desafio.numero == numero:
            return nodo
        if numero < nodo.desafio.numero:
            return self.buscar(nodo.izq, numero)
        return self.buscar(nodo.der, numero)

    def recomendar_desafio(self, desafios_comprendidos):
        while True:
            numero_aleatorio = random.randint(1, 101)
            if numero_aleatorio not in desafios_comprendidos:
                return numero_aleatorio

def main():
    arbol = Arbol()
    desafios = [Desafio(i) for i in range(1, 102)]
    arbol.insertar_desafios(desafios)

    # Lista de desafíos comprendidos por el usuario
    desafios_comprendidos = [3, 5, 8, 15, 26, 62, 72, 90, 100]
    
    # Mostrar los desafíos comprendidos
    print(f"Desafíos comprendidos por el usuario:{desafios_comprendidos}")

    desafio_recomendado_num = arbol.recomendar_desafio(desafios_comprendidos)
    desafio_recomendado = arbol.buscar(arbol.raiz, desafio_recomendado_num)
    if desafio_recomendado:
        print(f"Se te ha recomendado el desafío #{desafio_recomendado.desafio.numero} para que lo intentes resolver.")
    else:
        print("No se pudo encontrar un desafío para recomendar.")

    print("\nInformación adicional:")
    print("Total de desafíos:", len(desafios))
    print("Desafíos aún no comprendidos:")
    no_comprendidos = [i for i in range(1, 102) if i not in desafios_comprendidos]
    print(no_comprendidos)
    print("Número total de desafíos comprendidos:", len(desafios_comprendidos))
    print("Número de nodo de la raíz:", arbol.raiz.desafio.numero if arbol.raiz else "No hay nodo raíz")
    print("Primero desafío comprendido:", desafios_comprendidos[0] if desafios_comprendidos else "Ninguno")
    print("Último desafío comprendido:", desafios_comprendidos[-1] if desafios_comprendidos else "Ninguno")

if __name__ == "__main__":
    main()