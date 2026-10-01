



import threading
import time
import random



class Peaje:
    def __init__(self,cantCabinas):
        self.semaforo = threading.Semaphore(cantCabinas)
        self.recaudado = 0

    def atender_vehiculo(self, nombre, importe):
        try:
            print(f" {nombre} Esperando una cabina de peaje. Hay: {self.semaforo._value} libres")
            self.semaforo.acquire()
            
            print(f" {nombre} ingresa al peaje y paga {importe}")
            self.recaudado += importe
            time.sleep(random.uniform(0.05,0.5))
            print(f" {nombre} Sale del peaje")
        finally:
            self.semaforo.release()


    def mostrar_recaudacion(self):
        return self.recaudado

class Vehiculo(threading.Thread):
    def __init__(self, nombre, monto,peaje):
        super().__init__()
        self.nombre = nombre
        self.monto = monto
        self.peaje = peaje

    def run(self):
        self.peaje.atender_vehiculo(self.nombre,self.monto)

def main():
    peaje = Peaje(3)
    vehiculo1 = Vehiculo("fede",1000, peaje)
    vehiculo2 = Vehiculo("raul",1500, peaje)
    vehiculo3 = Vehiculo("carlos",1200, peaje)
    vehiculo4 = Vehiculo("mecha",1800, peaje)
    vehiculo5 = Vehiculo("marti",1000, peaje)
    vehiculo6 = Vehiculo("nacho",2000, peaje)
    vehiculo7 = Vehiculo("pedro",1500, peaje)
    vehiculo8 = Vehiculo("luis",1200, peaje)

    vehiculo1.start()
    vehiculo2.start()
    vehiculo3.start()
    vehiculo4.start()
    vehiculo5.start()
    vehiculo6.start()
    vehiculo7.start()
    vehiculo8.start()

    vehiculo1.join()
    vehiculo2.join()
    vehiculo3.join()
    vehiculo4.join()
    vehiculo5.join()
    vehiculo6.join()
    vehiculo7.join()
    vehiculo8.join()

    print(f"RECAUDACION FINAL:{peaje.mostrar_recaudacion()}")

if __name__ == "__main__":
    main()

        



