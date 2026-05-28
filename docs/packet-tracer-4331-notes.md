# Nota específica para Cisco 4331 en Packet Tracer

Esta nota complementa el runbook principal cuando se utilizan routers Cisco 4331.

## 1. Diferencia principal

En muchos routers 4331 de Packet Tracer, las interfaces no aparecen como:

```text
GigabitEthernet0/0
GigabitEthernet0/1
```

sino como:

```text
GigabitEthernet0/0/0
GigabitEthernet0/0/1
GigabitEthernet0/0/2
```

Por tanto, si al pegar una configuración aparece un error tipo:

```text
% Invalid input detected at '^' marker.
```

en una línea de interfaz, lo más probable es que el nombre de interfaz no coincida con el modelo.

## 2. Equivalencia recomendada

Usar esta equivalencia:

| Documento original | Cisco 4331 |
|---|---|
| `GigabitEthernet0/0` | `GigabitEthernet0/0/0` |
| `GigabitEthernet0/1` | `GigabitEthernet0/0/1` |

## 3. Comprobación básica

En cada router, ejecutar:

```ios
show ip interface brief
```

El objetivo es ver las interfaces usadas en estado:

```text
up                    up
```

Si una interfaz aparece como:

```text
administratively down down
```

faltaría ejecutar `no shutdown` en esa interfaz.

Si aparece como:

```text
up                    down
```

la interfaz está encendida, pero no hay enlace físico correcto o el otro extremo no está activo.

## 4. Configuración mínima esperada por router

Cada router debe tener:

- 1 loopback activa.
- 2 interfaces físicas con IP.
- OSPF proceso 1 activo.
- Las redes directamente conectadas anunciadas en área 0.

## 5. Verificación inicial recomendada

Después de pegar la configuración en los cuatro routers, ejecutar en `BASE`:

```ios
show ip interface brief
show ip ospf neighbor
show ip route ospf
show ip route 192.168.3.1
traceroute 192.168.3.1
ping 192.168.3.1 source 192.168.1.1
```

## 6. Qué debe verse si todo está bien

En `BASE`, deben aparecer dos vecinos OSPF cuando la red está completa:

- `HELI-ALFA`, por el enlace `10.0.1.0/30`.
- `HELI-CHARLIE`, por el enlace `10.0.4.0/30`.

Antes del fallo, la ruta hacia `192.168.3.1/32` debe ir por `10.0.1.2`.

Después de apagar la interfaz de `BASE` hacia `HELI-ALFA`, debe cambiar a `10.0.4.2`.

## 7. Sobre las líneas discontinuas en Packet Tracer

Las líneas discontinuas o el aspecto visual del cable no son suficientes para validar el laboratorio. La validación real debe hacerse por CLI:

```ios
show ip interface brief
show ip ospf neighbor
show ip route 192.168.3.1
```

Si las interfaces están `up/up`, hay vecinos OSPF y existe ruta hacia `192.168.3.1`, la topología está funcionando aunque el aspecto visual del enlace no sea exactamente como se esperaba.
