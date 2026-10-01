import threading
import time
import random

class Filosofo(threading.Thread):
    def __init__(self, nombre, izq, der):
        super().__init__()
        self.nombre = nombre
        self.primero = min(izq, der)   # siempre el tenedor de número más bajo primero
        self.segundo = max(izq, der)

    def run(self):
        for _ in range(3):
            with tenedores[self.primero]:
                print(f"{self.nombre} tiene el primero\n", end="")
                time.sleep(random.uniform(0.1, 0.5))
                with tenedores[self.segundo]:
                    print(f"{self.nombre} tiene el segundo\n", end="")
                    print(f"{self.nombre} COME\n", end="")
                    time.sleep(random.uniform(0.1, 0.5))

tenedores = [threading.Lock() for _ in range(5)]

def main():
    tenedores = [threading.Lock() for _ in range(5)]
    nombres = ["Fede", "Raul", "Nicky", "Ana", "Sofi"]
    filosofos = [Filosofo(nombres[i], i, (i + 1) % 5) for i in range(5)]
    for f in filosofos:
        f.start()
    for f in filosofos:
        f.join()
    print("Todos comieron, sin deadlock")

if __name__ == "__main__":
    main()