# Plan de validación

## 1. Objetivo de la prueba

Validar que la topología mantiene conectividad desde `BASE` hacia `HELI-BRAVO` cuando se pierde el enlace principal `BASE - HELI-ALFA`.

## 2. Condiciones iniciales

- Todos los enlaces están activos.
- Todos los routers tienen interfaces configuradas con `no shutdown`.
- OSPF está activo en área 0.
- Las vecindades OSPF están establecidas.
- Las loopbacks de todos los nodos son alcanzables.

## 3. Prueba 1: estado nominal

### Comandos

Desde `BASE`:

```ios
show ip ospf neighbor
show ip route 192.168.3.1
traceroute 192.168.3.1
ping 192.168.3.1 source 192.168.1.1
```

### Criterio de éxito

- `BASE` tiene vecinos OSPF activos.
- Existe ruta OSPF hacia `192.168.3.1/32`.
- El traceroute muestra el camino por `HELI-ALFA`.
- El ping responde correctamente.

## 4. Prueba 2: fallo de enlace

### Acción

Apagar el enlace `BASE - HELI-ALFA` desde `BASE`:

```ios
configure terminal
interface gigabitEthernet0/0
shutdown
end
```

### Comandos de verificación

```ios
show ip ospf neighbor
show ip route 192.168.3.1
traceroute 192.168.3.1
ping 192.168.3.1 source 192.168.1.1
```

### Criterio de éxito

- La vecindad OSPF con `HELI-ALFA` desaparece en `BASE`.
- OSPF instala una ruta alternativa hacia `192.168.3.1/32` vía `HELI-CHARLIE`.
- El traceroute muestra el camino alternativo.
- El ping vuelve a responder tras la reconvergencia.

## 5. Prueba 3: recuperación del enlace

### Acción

Reactivar el enlace `BASE - HELI-ALFA`:

```ios
configure terminal
interface gigabitEthernet0/0
no shutdown
end
```

### Criterio de éxito

- La vecindad OSPF con `HELI-ALFA` se recupera.
- La ruta preferente vuelve al camino de menor coste.
