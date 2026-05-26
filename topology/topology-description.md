# Descripción de la topología

La topología representa una red táctica IP simplificada. El puesto de mando `BASE` mantiene conectividad con tres nodos aéreos/intermedios. La red se diseña con redundancia física para que la pérdida de un enlace no implique pérdida total de conectividad.

## Nodos

### BASE

Representa el puesto de mando terrestre. Desde este nodo se ejecuta la prueba principal hacia `HELI-BRAVO`.

### HELI-ALFA

Representa el nodo de vanguardia. En condiciones normales, forma parte del camino preferente hacia `HELI-BRAVO`.

### HELI-BRAVO

Representa el nodo destino de la prueba de conectividad.

### HELI-CHARLIE

Representa el nodo de retaguardia/enlace alternativo. Permite mantener conectividad cuando falla el enlace `BASE - HELI-ALFA`.

## Hipótesis de validación

Si la red está correctamente configurada, OSPF detectará la caída del enlace principal y recalculará una ruta alternativa usando el enlace `BASE - HELI-CHARLIE`.

## Limitaciones

Este laboratorio no implementa una MANET real completa. Simula una topología táctica con redundancia y enrutamiento dinámico para estudiar continuidad, reconvergencia y validación técnica.
