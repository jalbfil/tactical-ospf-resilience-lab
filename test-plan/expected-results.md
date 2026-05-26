# Resultados esperados

## Estado nominal

Ruta esperada desde `BASE` hacia `HELI-BRAVO`:

```text
BASE -> HELI-ALFA -> HELI-BRAVO
```

Salida esperada aproximada en `BASE`:

```text
O 192.168.3.1/32 [110/20] via 10.0.1.2
```

Interpretación:

- `110` es la distancia administrativa de OSPF.
- `20` representa el coste acumulado aproximado del camino principal.
- `10.0.1.2` es la IP de `HELI-ALFA` en el enlace con `BASE`.

## Tras la caída del enlace BASE - HELI-ALFA

Ruta alternativa esperada:

```text
BASE -> HELI-CHARLIE -> HELI-BRAVO
```

Salida esperada aproximada en `BASE`:

```text
O 192.168.3.1/32 [110/100] via 10.0.4.2
```

Interpretación:

- La ruta sigue siendo OSPF.
- El coste aumenta porque se usa el camino alternativo.
- `10.0.4.2` es la IP de `HELI-CHARLIE` en el enlace con `BASE`.

## Conclusión esperada

La red mantiene conectividad hacia el nodo destino aunque se pierda el enlace principal. El laboratorio demuestra redundancia, encaminamiento dinámico y reconvergencia ante fallo.
