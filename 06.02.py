import threading
import random
import time


class RecursoCompartido:
    def __init__(self):
        self.dato = 0
        self.lectores = 0             # lectores leyendo ahora
        self.escribiendo = False      # hay un escritor adentro
        self.esperando = 0            # escritores en la fila
        self.cond = threading.Condition()

    def leer(self, nombre):
        # Entrar: no paso si alguien escribe o hay un escritor esperando
        with self.cond:
            while self.escribiendo or self.esperando > 0:
                self.cond.wait()
            self.lectores += 1

        # Leer (varios lectores a la vez)
        print(f"{nombre} lee {self.dato}\n", end="")
        time.sleep(random.uniform(0.1, 0.3))

        # Salir: si soy el último lector, aviso
        with self.cond:
            self.lectores -= 1
            if self.lectores == 0:
                self.cond.notify_all()

    def escribir(self, nombre, valor):
        # Entrar: me anoto y espero que no haya nadie adentro
        with self.cond:
            self.esperando += 1
            while self.escribiendo or self.lectores > 0:
                self.cond.wait()
            self.esperando -= 1
            self.escribiendo = True

        # Escribir (solo)
        print(f"{nombre} escribe {valor}\n", end="")
        time.sleep(random.uniform(0.1, 0.3))
        self.dato = valor

        # Salir: aviso a todos
        with self.cond:
            self.escribiendo = False
            self.cond.notify_all()


class Lector(threading.Thread):
    def __init__(self, nombre, recurso):
        super().__init__()
        self.nombre = nombre
        self.recurso = recurso

    def run(self):
        for _ in range(3):
            self.recurso.leer(self.nombre)
            time.sleep(random.uniform(0.1, 0.2))


class Escritor(threading.Thread):
    def __init__(self, nombre, recurso):
        super().__init__()
        self.nombre = nombre
        self.recurso = recurso

    def run(self):
        for _ in range(2):
            self.recurso.escribir(self.nombre, random.randint(1, 100))
            time.sleep(random.uniform(0.2, 0.4))


def main():
    recurso = RecursoCompartido()
    hilos = [Lector(f"Lector {i}", recurso) for i in range(4)]
    hilos += [Escritor(f"Escritor {i}", recurso) for i in range(2)]

    for h in hilos:
        h.start()
    for h in hilos:
        h.join()


if __name__ == "__main__":
    main()