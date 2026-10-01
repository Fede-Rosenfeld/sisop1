

"""
LOCK

Caja de ahorro compartida

Cinco usuarios comparten una misma caja de ahorro que arranca con saldo 0.
Cada usuario deposita $100. El depósito tarda un tiempo aleatorio (0.5 a 1.5 s) 
entre que lee el saldo y lo actualiza. Implementar el sistema de forma que ningún depósito se pierda.

Requisitos
Clase CajaDeAhorro con el saldo como atributo privado y un método depositar(monto).
Clase Usuario que herede de threading.Thread y reciba nombre, caja y monto.
Mostrar cada depósito y el saldo actualizado. El saldo final tiene que ser $500 siempre.
Garantizar que el mecanismo se libere aunque ocurra una excepción dentro del depósito."""



import threading
import time
import random


class CajaDeAhorro:
    def __init__(self,saldo=0):
        self.saldo = saldo
        self.lock = threading.Lock()

    def depositar(self,name, monto):
    
        self.lock.acquire()
        print(f"EL SALDO ANTES DE DEPOSITAR ES DE: {self.saldo}")
        print(f"El usuario {name} deposita: {monto}")
        self.saldo += monto
        time.sleep(random.uniform(0.05,0.5))
        print(f"EL SALDO LUEGO DE DEPOSITAR ES DE: {self.saldo}, saliendo del sistema")
        self.lock.release()

    
    def getSaldo(self):
        return self.saldo


class Usuario(threading.Thread):
    def __init__(self, name, caja, monto):
        super().__init__()
        self.name = name
        self.caja = caja
        self.monto = monto

    def run(self):
        print(f"Usuario {self.name} conectado")
        self.caja.depositar(self.name, self.monto)
        



def main():
    caja = CajaDeAhorro(0)
    usuarios = []
    for i in range(0,5):
        k = Usuario(f"{i}",caja,100)
        usuarios.append(k)
    for u in usuarios:
        u.start()
    for u in usuarios:
        u.join()
    print(f"SALDO FINAL: {caja.getSaldo()}")


if __name__ == "__main__":
    main()