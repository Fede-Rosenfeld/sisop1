
"""Un cine tiene 5 salas de 50 asientos cada una. Diez usuarios intentan reservar concurrentemente: el usuario i (de 1 a 10) pide i asientos en la sala (i−1) mod 5. Una reserva solo se concreta si en ese momento hay suficientes asientos libres en la sala; si no, se rechaza entera (no se reservan asientos sueltos).

Requisitos
Clase Sala con la lista de asientos (libre/ocupado) y reservar_asientos(cantidad) que devuelva True/False.
Clase Cine que contenga las 5 salas y delegue la reserva a la sala pedida.
Clase Usuario(threading.Thread) que informe «reservó N asientos en la sala X» o «no pudo reservar».
Pensá dónde va el mecanismo: ¿uno para todo el cine o uno por sala? Justificalo.
pista: mecanismo
Lock por sala (el chequeo de libres y la marca de ocupados son una sola sección crítica)

Uno por sala permite que reservas en salas distintas no se bloqueen entre sí. Solución: P05 · 04.02-Locks.py."""



import random
import threading
import time


class Sala:
    def __init__(self, numero, capacidad):
        self.numero = numero
        self.asientos = [False] * capacidad   # False = libre, True = ocupado
        self.lock = threading.Lock()          # un lock por sala

    def reservar_asientos(self, cantidad):
        # Chequear y ocupar tiene que ser una sola sección crítica
        with self.lock:
            libres = [i for i, ocupado in enumerate(self.asientos) if not ocupado]
            if len(libres) < cantidad:
                return False                  # no alcanza: se rechaza entera
            for i in libres[:cantidad]:
                self.asientos[i] = True
            return True


class Cine:
    def __init__(self, cant_salas, capacidad):
        self.salas = [Sala(i, capacidad) for i in range(cant_salas)]

    def reservar(self, numero_sala, cant_asientos):
        return self.salas[numero_sala].reservar_asientos(cant_asientos)


class Usuario(threading.Thread):
    def __init__(self, numero, cine):
        super().__init__()
        self.numero = numero
        self.cine = cine

    def run(self):
        cantidad = self.numero
        sala = (self.numero - 1) % 5
        time.sleep(random.uniform(0, 0.1))     # para que se mezclen
        if self.cine.reservar(sala, cantidad):
            print(f"Usuario {self.numero} reservó {cantidad} asientos en la sala {sala}\n", end="")
        else:
            print(f"Usuario {self.numero} no pudo reservar {cantidad} asientos en la sala {sala}\n", end="")


def main():
    cine = Cine(cant_salas=5, capacidad=50)
    usuarios = [Usuario(i, cine) for i in range(1, 11)]

    for u in usuarios:
        u.start()
    for u in usuarios:
        u.join()


if __name__ == "__main__":
    main()
    