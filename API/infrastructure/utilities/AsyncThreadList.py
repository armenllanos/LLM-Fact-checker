
import asyncio
import threading
from typing import List, Any, Optional, Iterator
from collections import deque
import time



class AsyncThreadList:
    """Lista thread-safe usando threading.Lock para hilos tradicionales"""
    
    def __init__(self):
        self._lista: List[Any] = []
        self._lock = threading.RLock()  # RLock permite múltiples adquisiciones por el mismo hilo
    
    def add(self, item: Any) -> None:
        """Agrega un elemento de forma thread-safe"""
        with self._lock:
            self._lista.append(item)
            print(f"[{threading.current_thread().name}] Agregado: {item}")
    
    def get(self, indice: int) -> Any:
        """Obtiene un elemento por índice"""
        with self._lock:
            if 0 <= indice < len(self._lista):
                return self._lista[indice]
            raise IndexError("Índice fuera de rango")
    
    def delete(self, item: Any) -> bool:
        """Elimina la primera ocurrencia del elemento"""
        with self._lock:
            try:
                self._lista.remove(item)
                print(f"[{threading.current_thread().name}] Eliminado: {item}")
                return True
            except ValueError:
                return False
    def print(self):
        """Devuelve un string con todos los elementos de la lista"""
        return " ".join(str(self._lista))
    
    def pop_first(self):
        """Remueve el primer elemento"""
        with self._lock:
            if not self._lista:
                raise IndexError("Lista vacía")
            item = self._lista.pop(0)
            print(f"[{threading.current_thread().name}] Pop primero: {item} (Quedan: {len(self._lista)})")

        
    def first(self) -> Any:
        """Retorna el primer elemento"""
        with self._lock:
            if not self._lista:
                raise IndexError("Lista vacía")
            item = self._lista[0]
            return item