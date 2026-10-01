import threading, time, random

class Buffer:
    def __init__(self, capacidad):
        self.__items = []
        self.__espacios = threading.Semaphore(capacidad)  # lugares libres
        self.__elementos = threading.Semaphore(0)         # items listos para consumir
        self.__lock = threading.Lock()                    # protege la lista

    def agregar(self, item):
        self.__espacios.acquire()          # si esta lleno, el productor espera
        with self.__lock:                  # seccion critica corta
            self.__items.append(item)
            estado = list(self.__items)
        self.__elementos.release()         # avisa: hay un item mas
        return estado

    def retirar(self):
        self.__elementos.acquire()         # si esta vacio, el consumidor espera
        with self.__lock:
            item = self.__items.pop(0)
            estado = list(self.__items)
        self.__espacios.release()          # avisa: hay un lugar mas
        return item, estado

class Productor(threading.Thread):
    def __init__(self, nombre, buffer, cantidad):
        super().__init__()
        self.__nombre = nombre
        self.__buffer = buffer
        self.__cantidad = cantidad

    def run(self):
        for _ in range(self.__cantidad):
            item = random.randint(1, 100)
            estado = self.__buffer.agregar(item)
            print(f"{self.__nombre} produjo {item:3} | buffer {estado}", end="\n")
            time.sleep(random.uniform(0.01, 0.05))

class Consumidor(threading.Thread):
    def __init__(self, nombre, buffer, cantidad):
        super().__init__()
        self.__nombre = nombre
        self.__buffer = buffer
        self.__cantidad = cantidad

    def run(self):
        for _ in range(self.__cantidad):
            item, estado = self.__buffer.retirar()
            print(f"{self.__nombre} consumio {item:3} | buffer {estado}", end="")
            time.sleep(random.uniform(0.02, 0.08))

def main():
    buffer = Buffer(5)
    # 1 productor -> 3 consumidores, como el dibujo de la diapo 4 (12 items = 3 x 4)
    hilos = [Productor("Productor", buffer, 12)]
    hilos += [Consumidor(f"Consumidor {i+1}", buffer, 4) for i in range(3)]
    for h in hilos: h.start()
    for h in hilos: h.join()
    print("Produccion y consumo finalizados.")

if __name__ == "__main__":
    main()