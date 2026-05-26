# Chuleta de verificación

Comandos útiles para validar el laboratorio desde la CLI de Cisco IOS.

## Estado de interfaces

```ios
show ip interface brief
```

Uso:

- Verificar que las interfaces están `up/up`.
- Confirmar que las IP se han aplicado correctamente.
- Detectar interfaces en `administratively down` tras un `shutdown`.

## Vecinos OSPF

```ios
show ip ospf neighbor
```

Uso:

- Confirmar que las adyacencias OSPF están levantadas.
- Comprobar qué vecinos desaparecen tras una caída de enlace.

Estados esperados:

- `FULL`: vecindad establecida correctamente.
- Sin vecino: enlace caído, interfaz mal configurada o problema de OSPF.

## Rutas aprendidas por OSPF

```ios
show ip route ospf
```

Uso:

- Ver únicamente las rutas instaladas por OSPF.
- Confirmar que las loopbacks remotas aparecen como rutas OSPF.

## Ruta concreta hacia HELI-BRAVO

```ios
show ip route 192.168.3.1
```

Antes del fallo, ruta esperada:

```text
O 192.168.3.1/32 [110/20] via 10.0.1.2
```

Después del fallo, ruta alternativa esperada:

```text
O 192.168.3.1/32 [110/100] via 10.0.4.2
```

## Trazado del camino

```ios
traceroute 192.168.3.1
```

Uso:

- Antes del fallo debe observarse el camino por `HELI-ALFA`.
- Después del fallo debe observarse el camino por `HELI-CHARLIE`.

## Ping con origen estable

```ios
ping 192.168.3.1 source 192.168.1.1
```

Uso:

- Validar conectividad desde la loopback de `BASE` hacia la loopback de `HELI-BRAVO`.
- Evitar que la prueba dependa de una IP física concreta del enlace.

## Simular caída del enlace principal

En `BASE`:

```ios
configure terminal
interface gigabitEthernet0/0
shutdown
end
```

## Recuperar el enlace principal

En `BASE`:

```ios
configure terminal
interface gigabitEthernet0/0
no shutdown
end
```

## Evidencias mínimas para documentar

1. Topología completa.
2. Vecinos OSPF antes del fallo.
3. Ruta hacia `192.168.3.1` antes del fallo.
4. Traceroute antes del fallo.
5. Enlace principal apagado.
6. Ruta hacia `192.168.3.1` después del fallo.
7. Traceroute después del fallo.
8. Ping final correcto.
