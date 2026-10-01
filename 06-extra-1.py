


"""Por un puente solo puede pasar un vehículo a la vez, 
y puede haber vehículos esperando en ambos extremos. 
Diseñar un mecanismo para que crucen de forma segura, sin colisión, 
y que el tráfico de ambos lados fluya de manera eficiente y justa."""


import threading
import time
import random


class Coche(threading.Thread):
    def __init__(self,nombre,puente):
        super().__init__()
        self.nombre = nombre
        self.puente = puente

    def run(self):
        print(f"Coche {self.name} esperando cruzar el puente")
        time.sleep(random.uniform(0.5,1.0))
        self.puente.acquire()
        print(f"Coche {self.name} CRUZANDO")
        print(f"Coche {self.name} PASO")
        self.puente.release()


def main():
    puente = threading.Lock()
    vehiculos = []
    for i in range(0,5):
        vehiculos.append(Coche(i,puente))
    for i in vehiculos:
        i.start()
    for i in vehiculos:
        i.join()

    print(f"TODOS LOS VEHICULOS PASARON POR EL PUENTE")
    



if __name__ == "__main__":
    main()
