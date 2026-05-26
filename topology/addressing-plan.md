# Plan de direccionamiento

## Enlaces punto a punto

| Enlace | Subred | IP lado A | IP lado B |
|---|---:|---:|---:|
| BASE - HELI-ALFA | `10.0.1.0/30` | BASE `10.0.1.1` | HELI-ALFA `10.0.1.2` |
| HELI-ALFA - HELI-BRAVO | `10.0.2.0/30` | HELI-ALFA `10.0.2.1` | HELI-BRAVO `10.0.2.2` |
| HELI-BRAVO - HELI-CHARLIE | `10.0.3.0/30` | HELI-BRAVO `10.0.3.1` | HELI-CHARLIE `10.0.3.2` |
| HELI-CHARLIE - BASE | `10.0.4.0/30` | HELI-CHARLIE `10.0.4.2` | BASE `10.0.4.1` |

## Loopbacks

| Nodo | Loopback | Uso |
|---|---:|---|
| BASE | `192.168.1.1/32` | Identificador lógico del puesto de mando |
| HELI-ALFA | `192.168.2.1/32` | Identificador lógico del nodo Alfa |
| HELI-BRAVO | `192.168.3.1/32` | Identificador lógico del nodo Bravo |
| HELI-CHARLIE | `192.168.4.1/32` | Identificador lógico del nodo Charlie |

## Criterio de costes OSPF

Se aplican costes OSPF diferentes para que el camino principal desde BASE hacia HELI-BRAVO sea:

```text
BASE -> HELI-ALFA -> HELI-BRAVO
```

Y el camino alternativo tras fallo sea:

```text
BASE -> HELI-CHARLIE -> HELI-BRAVO
```
