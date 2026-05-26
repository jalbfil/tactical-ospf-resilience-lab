# Tactical OSPF Resilience Lab

Laboratorio de red táctica resiliente con OSPF, simulación de caída de enlace y validación de reconvergencia.

## 1. Objetivo

Este laboratorio simula una topología de comunicaciones formada por un puesto de mando terrestre y tres nodos aéreos/intermedios. El objetivo es comprobar cómo una red con encaminamiento dinámico puede mantener la conectividad cuando se pierde un enlace principal.

La práctica no pretende implementar una MANET real completa, sino representar de forma controlada los principios de redundancia, encaminamiento dinámico, reconvergencia y validación técnica en una red táctica IP.

## 2. Escenario

- `BASE`: Puesto de mando terrestre.
- `HELI-ALFA`: Nodo aéreo de vanguardia.
- `HELI-BRAVO`: Nodo aéreo de flanco/destino de la prueba.
- `HELI-CHARLIE`: Nodo aéreo de retaguardia/enlace alternativo.

Topología lógica:

```text
BASE -------- HELI-ALFA
 |                |
 |                |
HELI-CHARLIE -- HELI-BRAVO
```

## 3. Tecnologías y conceptos trabajados

- Cisco Packet Tracer.
- Direccionamiento IPv4 con subredes /30 en enlaces punto a punto.
- Interfaces loopback como identificadores estables de nodo.
- OSPF en área 0.
- Costes OSPF para priorizar rutas.
- Verificación con `show ip route`, `show ip ospf neighbor`, `ping` y `traceroute`.
- Simulación de caída de enlace mediante `shutdown`.

## 4. Resultado esperado

Antes del fallo, el tráfico desde `BASE` hacia `HELI-BRAVO` debe circular por:

```text
BASE -> HELI-ALFA -> HELI-BRAVO
```

Tras apagar el enlace entre `BASE` y `HELI-ALFA`, OSPF debe recalcular una ruta alternativa:

```text
BASE -> HELI-CHARLIE -> HELI-BRAVO
```

## 5. Estructura del repositorio

```text
tactical-ospf-resilience-lab/
├── README.md
├── topology/
│   ├── addressing-plan.md
│   ├── topology-description.md
│   └── ospf-logical-topology.mmd
├── configs/
│   ├── BASE.txt
│   ├── HELI-ALFA.txt
│   ├── HELI-BRAVO.txt
│   └── HELI-CHARLIE.txt
├── evidence/
│   ├── README.md
│   ├── before/
│   │   └── README.md
│   └── after/
│       └── README.md
├── test-plan/
│   ├── validation-plan.md
│   ├── expected-results.md
│   └── lessons-learned.md
├── automation/
│   ├── README.md
│   └── requirements.txt
└── linkedin/
    └── linkedin-post-draft.md
```

## 6. Fases del proyecto

### Fase 1 — Laboratorio manual

1. Crear la topología en Cisco Packet Tracer.
2. Configurar interfaces y loopbacks.
3. Activar OSPF en área 0.
4. Verificar vecindades y rutas.
5. Simular caída del enlace principal.
6. Documentar el cambio de ruta.

### Fase 2 — Automatización

Como evolución del laboratorio, se plantea automatizar la validación mediante Python y SSH usando Netmiko. La automatización recogerá evidencias de estado antes y después del fallo.

## 7. Enfoque profesional

Este proyecto está orientado a demostrar capacidades prácticas en:

- Integración y validación de redes IP.
- Continuidad de comunicaciones.
- Diseño de pruebas técnicas.
- Documentación de evidencias.
- Aplicación de conceptos de networking a escenarios CIS/Defensa.
