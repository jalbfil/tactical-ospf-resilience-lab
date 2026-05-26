# Runbook completo: montaje y validación en Cisco Packet Tracer

Este documento es la guía operativa principal para construir, configurar, probar y documentar el laboratorio `Tactical OSPF Resilience Lab` en Cisco Packet Tracer.

El objetivo es que puedas seguirlo de principio a fin sin consultar otros documentos.

---

## 1. Objetivo del laboratorio

Simular una red táctica IP formada por un puesto de mando y tres nodos aéreos/intermedios. La red utiliza OSPF para mantener conectividad hacia un nodo destino aunque se pierda el enlace principal.

La prueba principal consiste en comprobar que, si cae el enlace `BASE - HELI-ALFA`, el tráfico desde `BASE` hacia `HELI-BRAVO` deja de usar el camino principal y se redirige por `HELI-CHARLIE`.

---

## 2. Resultado esperado

### Estado nominal

```text
BASE -> HELI-ALFA -> HELI-BRAVO
```

### Estado degradado tras fallo del enlace BASE - HELI-ALFA

```text
BASE -> HELI-CHARLIE -> HELI-BRAVO
```

---

## 3. Material necesario

- Cisco Packet Tracer.
- 4 routers Cisco, preferiblemente `2911`, `1941` o `4331`.
- 4 enlaces Ethernet o Serial, según disponibilidad del modelo.
- Consola CLI de cada router.

> Recomendación: usar interfaces GigabitEthernet para simplificar el laboratorio.

---

## 4. Crear la topología

### 4.1. Añadir routers

Arrastra cuatro routers al área de trabajo y renómbralos así:

| Router | Nombre lógico | Función |
|---|---|---|
| Router 1 | `BASE` | Puesto de mando terrestre |
| Router 2 | `HELI-ALFA` | Nodo de vanguardia / camino principal |
| Router 3 | `HELI-BRAVO` | Nodo destino de la prueba |
| Router 4 | `HELI-CHARLIE` | Nodo alternativo / camino de respaldo |

### 4.2. Conectar routers

Crear esta topología en anillo:

```text
BASE -------- HELI-ALFA
 |                |
 |                |
HELI-CHARLIE -- HELI-BRAVO
```

Enlaces a crear:

| Enlace | Subred |
|---|---:|
| `BASE` - `HELI-ALFA` | `10.0.1.0/30` |
| `HELI-ALFA` - `HELI-BRAVO` | `10.0.2.0/30` |
| `HELI-BRAVO` - `HELI-CHARLIE` | `10.0.3.0/30` |
| `HELI-CHARLIE` - `BASE` | `10.0.4.0/30` |

---

## 5. Plan de direccionamiento

### 5.1. Interfaces físicas

| Router | Interfaz | IP | Máscara | Enlace |
|---|---|---:|---:|---|
| `BASE` | `G0/0` | `10.0.1.1` | `255.255.255.252` | BASE - ALFA |
| `HELI-ALFA` | `G0/0` | `10.0.1.2` | `255.255.255.252` | ALFA - BASE |
| `HELI-ALFA` | `G0/1` | `10.0.2.1` | `255.255.255.252` | ALFA - BRAVO |
| `HELI-BRAVO` | `G0/0` | `10.0.2.2` | `255.255.255.252` | BRAVO - ALFA |
| `HELI-BRAVO` | `G0/1` | `10.0.3.1` | `255.255.255.252` | BRAVO - CHARLIE |
| `HELI-CHARLIE` | `G0/0` | `10.0.3.2` | `255.255.255.252` | CHARLIE - BRAVO |
| `HELI-CHARLIE` | `G0/1` | `10.0.4.2` | `255.255.255.252` | CHARLIE - BASE |
| `BASE` | `G0/1` | `10.0.4.1` | `255.255.255.252` | BASE - CHARLIE |

> Si Packet Tracer usa nombres como `GigabitEthernet0/0/0`, adapta el nombre de interfaz, pero conserva las IP.

### 5.2. Loopbacks

| Router | Loopback | IP | Función |
|---|---|---:|---|
| `BASE` | `Loopback0` | `192.168.1.1/32` | Identificador estable del puesto de mando |
| `HELI-ALFA` | `Loopback0` | `192.168.2.1/32` | Identificador estable de ALFA |
| `HELI-BRAVO` | `Loopback0` | `192.168.3.1/32` | Destino principal de la prueba |
| `HELI-CHARLIE` | `Loopback0` | `192.168.4.1/32` | Identificador estable de CHARLIE |

---

## 6. Configuración de `BASE`

Entra en la CLI de `BASE` y pega:

```ios
enable
configure terminal

hostname BASE

interface loopback0
 ip address 192.168.1.1 255.255.255.255

interface gigabitEthernet0/0
 description ENLACE_BASE_HELI-ALFA
 ip address 10.0.1.1 255.255.255.252
 ip ospf cost 10
 ip ospf network point-to-point
 no shutdown

interface gigabitEthernet0/1
 description ENLACE_BASE_HELI-CHARLIE
 ip address 10.0.4.1 255.255.255.252
 ip ospf cost 50
 ip ospf network point-to-point
 no shutdown

router ospf 1
 router-id 1.1.1.1
 passive-interface loopback0
 network 10.0.1.0 0.0.0.3 area 0
 network 10.0.4.0 0.0.0.3 area 0
 network 192.168.1.1 0.0.0.0 area 0

end
write memory
```

---

## 7. Configuración de `HELI-ALFA`

```ios
enable
configure terminal

hostname HELI-ALFA

interface loopback0
 ip address 192.168.2.1 255.255.255.255

interface gigabitEthernet0/0
 description ENLACE_HELI-ALFA_BASE
 ip address 10.0.1.2 255.255.255.252
 ip ospf cost 10
 ip ospf network point-to-point
 no shutdown

interface gigabitEthernet0/1
 description ENLACE_HELI-ALFA_HELI-BRAVO
 ip address 10.0.2.1 255.255.255.252
 ip ospf cost 10
 ip ospf network point-to-point
 no shutdown

router ospf 1
 router-id 2.2.2.2
 passive-interface loopback0
 network 10.0.1.0 0.0.0.3 area 0
 network 10.0.2.0 0.0.0.3 area 0
 network 192.168.2.1 0.0.0.0 area 0

end
write memory
```

---

## 8. Configuración de `HELI-BRAVO`

```ios
enable
configure terminal

hostname HELI-BRAVO

interface loopback0
 ip address 192.168.3.1 255.255.255.255

interface gigabitEthernet0/0
 description ENLACE_HELI-BRAVO_HELI-ALFA
 ip address 10.0.2.2 255.255.255.252
 ip ospf cost 10
 ip ospf network point-to-point
 no shutdown

interface gigabitEthernet0/1
 description ENLACE_HELI-BRAVO_HELI-CHARLIE
 ip address 10.0.3.1 255.255.255.252
 ip ospf cost 50
 ip ospf network point-to-point
 no shutdown

router ospf 1
 router-id 3.3.3.3
 passive-interface loopback0
 network 10.0.2.0 0.0.0.3 area 0
 network 10.0.3.0 0.0.0.3 area 0
 network 192.168.3.1 0.0.0.0 area 0

end
write memory
```

---

## 9. Configuración de `HELI-CHARLIE`

```ios
enable
configure terminal

hostname HELI-CHARLIE

interface loopback0
 ip address 192.168.4.1 255.255.255.255

interface gigabitEthernet0/0
 description ENLACE_HELI-CHARLIE_HELI-BRAVO
 ip address 10.0.3.2 255.255.255.252
 ip ospf cost 50
 ip ospf network point-to-point
 no shutdown

interface gigabitEthernet0/1
 description ENLACE_HELI-CHARLIE_BASE
 ip address 10.0.4.2 255.255.255.252
 ip ospf cost 50
 ip ospf network point-to-point
 no shutdown

router ospf 1
 router-id 4.4.4.4
 passive-interface loopback0
 network 10.0.3.0 0.0.0.3 area 0
 network 10.0.4.0 0.0.0.3 area 0
 network 192.168.4.1 0.0.0.0 area 0

end
write memory
```

---

## 10. Verificación inicial

Espera unos segundos a que OSPF forme vecindades.

En `BASE`, ejecuta:

```ios
show ip interface brief
show ip ospf neighbor
show ip route ospf
show ip route 192.168.3.1
traceroute 192.168.3.1
ping 192.168.3.1 source 192.168.1.1
```

### Resultado esperado

`BASE` debe alcanzar la loopback de `HELI-BRAVO` (`192.168.3.1`) a través de `HELI-ALFA`.

La ruta esperada debe ser similar a:

```text
O 192.168.3.1/32 [110/20] via 10.0.1.2
```

Y el traceroute debe mostrar el camino:

```text
BASE -> HELI-ALFA -> HELI-BRAVO
```

---

## 11. Evidencias antes del fallo

Guardar capturas o salida de consola de:

1. Topología completa en Packet Tracer.
2. `show ip ospf neighbor` en `BASE`.
3. `show ip route 192.168.3.1` en `BASE`.
4. `traceroute 192.168.3.1` en `BASE`.
5. `ping 192.168.3.1 source 192.168.1.1` en `BASE`.

Estas evidencias corresponden a la carpeta:

```text
evidence/before/
```

---

## 12. Simular caída del enlace principal

En `BASE`, apaga la interfaz que conecta con `HELI-ALFA`:

```ios
configure terminal
interface gigabitEthernet0/0
shutdown
end
```

Espera unos segundos para permitir la reconvergencia de OSPF.

---

## 13. Verificación después del fallo

En `BASE`, ejecuta:

```ios
show ip interface brief
show ip ospf neighbor
show ip route 192.168.3.1
traceroute 192.168.3.1
ping 192.168.3.1 source 192.168.1.1
```

### Resultado esperado

La ruta hacia `HELI-BRAVO` debe cambiar al camino alternativo:

```text
BASE -> HELI-CHARLIE -> HELI-BRAVO
```

La ruta esperada debe ser similar a:

```text
O 192.168.3.1/32 [110/100] via 10.0.4.2
```

---

## 14. Evidencias después del fallo

Guardar capturas o salida de consola de:

1. Enlace `BASE - HELI-ALFA` apagado.
2. `show ip ospf neighbor` en `BASE`.
3. `show ip route 192.168.3.1` en `BASE`.
4. `traceroute 192.168.3.1` en `BASE`.
5. `ping 192.168.3.1 source 192.168.1.1` en `BASE`.

Estas evidencias corresponden a la carpeta:

```text
evidence/after/
```

---

## 15. Recuperar el enlace principal

En `BASE`:

```ios
configure terminal
interface gigabitEthernet0/0
no shutdown
end
```

Esperar unos segundos y verificar de nuevo:

```ios
show ip ospf neighbor
show ip route 192.168.3.1
traceroute 192.168.3.1
```

La red debería volver al camino preferente:

```text
BASE -> HELI-ALFA -> HELI-BRAVO
```

---

## 16. Problemas comunes

### 16.1. No aparecen vecinos OSPF

Comprobar:

```ios
show ip interface brief
show ip ospf interface brief
```

Posibles causas:

- Interfaz apagada.
- IP incorrecta.
- Máscara incorrecta.
- El `network` de OSPF no cubre la interfaz.
- Nombre de interfaz diferente al usado en la configuración.

### 16.2. El ping falla pero hay vecinos OSPF

Comprobar:

```ios
show ip route
show ip route ospf
show ip route 192.168.3.1
```

Posibles causas:

- Loopback no anunciada en OSPF.
- Falta ruta de retorno.
- Configuración incompleta en uno de los routers intermedios.

### 16.3. El traceroute no cambia tras el fallo

Comprobar:

```ios
show ip ospf neighbor
show ip route 192.168.3.1
```

Posibles causas:

- No se ha apagado la interfaz correcta.
- La ruta alternativa no existe.
- Costes OSPF mal aplicados.
- Todavía no ha terminado la reconvergencia.

---

## 17. Checklist final

Antes de dar por terminado el laboratorio, confirmar:

- [ ] Los cuatro routers están creados y renombrados.
- [ ] Los cuatro enlaces están activos.
- [ ] Todas las interfaces tienen IP correcta.
- [ ] Todas las loopbacks están configuradas.
- [ ] OSPF está activo en área 0.
- [ ] `BASE` tiene ruta hacia `192.168.3.1/32`.
- [ ] Antes del fallo, el camino va por `HELI-ALFA`.
- [ ] Tras el fallo, el camino va por `HELI-CHARLIE`.
- [ ] El ping final responde.
- [ ] Se han guardado evidencias antes y después.

---

## 18. Lectura profesional del resultado

El laboratorio demuestra que una red IP con topología redundante y enrutamiento dinámico puede mantener conectividad ante la pérdida de un enlace.

En un contexto CIS/Defensa, la práctica es útil para explicar conceptos como:

- continuidad de comunicaciones;
- degradación controlada de red;
- resiliencia de enlaces;
- validación técnica con evidencias;
- separación entre estado nominal y estado degradado;
- documentación de pruebas de aceptación.
