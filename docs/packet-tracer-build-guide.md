# Guía de montaje en Cisco Packet Tracer

Esta guía describe cómo construir manualmente la topología del laboratorio en Cisco Packet Tracer.

## 1. Crear los routers

Añadir cuatro routers, por ejemplo modelos Cisco 2911 o 4331, y renombrarlos como:

- `BASE`
- `HELI-ALFA`
- `HELI-BRAVO`
- `HELI-CHARLIE`

## 2. Crear la topología lógica

Interconectar los routers formando un anillo redundante:

```text
BASE -------- HELI-ALFA
 |                |
 |                |
HELI-CHARLIE -- HELI-BRAVO
```

Enlaces:

| Enlace | Subred |
|---|---:|
| BASE - HELI-ALFA | `10.0.1.0/30` |
| HELI-ALFA - HELI-BRAVO | `10.0.2.0/30` |
| HELI-BRAVO - HELI-CHARLIE | `10.0.3.0/30` |
| HELI-CHARLIE - BASE | `10.0.4.0/30` |

## 3. Configurar interfaces

Usar los ficheros de la carpeta `configs/` como configuración base de cada router.

> Nota: si Packet Tracer asigna nombres de interfaz diferentes, adaptar únicamente el nombre de interfaz. Por ejemplo, cambiar `gigabitEthernet0/0` por `gigabitEthernet0/0/0` si el modelo lo requiere.

## 4. Configurar loopbacks

Cada router tiene una `Loopback0` que representa su identificador lógico estable:

| Nodo | Loopback |
|---|---:|
| BASE | `192.168.1.1/32` |
| HELI-ALFA | `192.168.2.1/32` |
| HELI-BRAVO | `192.168.3.1/32` |
| HELI-CHARLIE | `192.168.4.1/32` |

La prueba principal se realiza contra la loopback de `HELI-BRAVO`, no contra una interfaz física. Esto permite simular la alcanzabilidad del nodo aunque cambie el camino de red.

## 5. Activar OSPF

Todos los routers participan en OSPF área 0.

Se han configurado costes para que el camino preferente desde `BASE` hacia `HELI-BRAVO` sea:

```text
BASE -> HELI-ALFA -> HELI-BRAVO
```

Y el camino alternativo sea:

```text
BASE -> HELI-CHARLIE -> HELI-BRAVO
```

## 6. Verificación inicial

Desde `BASE`, ejecutar:

```ios
show ip interface brief
show ip ospf neighbor
show ip route 192.168.3.1
traceroute 192.168.3.1
ping 192.168.3.1 source 192.168.1.1
```

Criterio de éxito:

- Existe vecindad OSPF.
- Existe ruta OSPF hacia `192.168.3.1/32`.
- El traceroute pasa por `HELI-ALFA`.
- El ping responde correctamente.

## 7. Simular fallo de enlace

En `BASE`, apagar la interfaz hacia `HELI-ALFA`:

```ios
configure terminal
interface gigabitEthernet0/0
shutdown
end
```

Esperar unos segundos a la reconvergencia y repetir:

```ios
show ip ospf neighbor
show ip route 192.168.3.1
traceroute 192.168.3.1
ping 192.168.3.1 source 192.168.1.1
```

Criterio de éxito:

- La vecindad directa `BASE - HELI-ALFA` desaparece.
- La ruta hacia `192.168.3.1/32` cambia vía `HELI-CHARLIE`.
- El tráfico vuelve a responder tras la reconvergencia.

## 8. Recuperar el enlace

```ios
configure terminal
interface gigabitEthernet0/0
no shutdown
end
```

Tras la recuperación, OSPF debería volver a instalar el camino preferente de menor coste.
