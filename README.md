# Tactical OSPF Resilience Lab

Laboratorio de red táctica resiliente con OSPF, simulación de caída de enlace y validación de reconvergencia.

Este proyecto simula una red IP táctica formada por un puesto de mando terrestre y tres nodos aéreos/intermedios. El objetivo es comprobar cómo una topología redundante con enrutamiento dinámico puede mantener la conectividad cuando se pierde un enlace principal.

> Nota técnica: la práctica no implementa una MANET real completa. Representa, de forma controlada en Cisco Packet Tracer, principios de redundancia, routing dinámico, reconvergencia y validación técnica aplicables a escenarios CIS/Defensa.

---

## 1. Escenario

- `BASE`: Puesto de mando terrestre.
- `HELI-ALFA`: Nodo aéreo de vanguardia y camino principal.
- `HELI-BRAVO`: Nodo destino de la prueba.
- `HELI-CHARLIE`: Nodo aéreo de retaguardia y camino alternativo.

Topología lógica:

```text
BASE -------- HELI-ALFA
 |                |
 |                |
HELI-CHARLIE -- HELI-BRAVO
```

---

## 2. Objetivo de validación

Validar tres estados de operación:

### Estado nominal

```text
BASE -> HELI-ALFA -> HELI-BRAVO
```

### Estado degradado tras fallo del enlace principal

```text
BASE -> HELI-CHARLIE -> HELI-BRAVO
```

### Estado recuperado

```text
BASE -> HELI-ALFA -> HELI-BRAVO
```

---

## 3. Tecnologías y conceptos trabajados

- Cisco Packet Tracer.
- Routers Cisco 4331.
- Direccionamiento IPv4 con subredes `/30` en enlaces punto a punto.
- Interfaces loopback como identificadores estables de nodo.
- OSPF en área 0.
- Ajuste de costes OSPF para definir camino principal y camino de respaldo.
- Verificación con `show ip route`, `show ip ospf neighbor`, `ping` y `traceroute`.
- Simulación de caída de enlace mediante `shutdown`.
- Documentación de evidencias antes, durante y después del fallo.

---

## 4. Resultado validado

El laboratorio fue montado y probado correctamente en Cisco Packet Tracer.

### 4.1. Ruta nominal

Antes del fallo, `BASE` alcanza la loopback de `HELI-BRAVO` (`192.168.3.1/32`) por el camino principal:

```text
BASE -> HELI-ALFA -> HELI-BRAVO
```

Resultado esperado en `BASE`:

```text
via 10.0.1.2, GigabitEthernet0/0/0
```

Traceroute esperado:

```text
1   10.0.1.2
2   10.0.2.2
```

### 4.2. Fallo controlado

Se simula la caída del enlace principal apagando la interfaz de `BASE` hacia `HELI-ALFA`:

```ios
configure terminal
interface GigabitEthernet0/0/0
shutdown
end
```

OSPF detecta la caída del vecino `HELI-ALFA` y elimina esa adyacencia.

### 4.3. Ruta degradada

Tras la reconvergencia, `BASE` mantiene conectividad hacia `HELI-BRAVO` mediante `HELI-CHARLIE`:

```text
BASE -> HELI-CHARLIE -> HELI-BRAVO
```

Resultado esperado en `BASE`:

```text
via 10.0.4.2, GigabitEthernet0/0/1
```

Traceroute esperado:

```text
1   10.0.4.2
2   10.0.3.1
```

### 4.4. Recuperación y ajuste de costes

Durante la recuperación apareció un comportamiento ECMP, ya que OSPF detectaba dos caminos de igual coste hacia `HELI-BRAVO`.

Se ajustaron los costes OSPF para que el camino por `HELI-ALFA` quedase como ruta principal y el camino por `HELI-CHARLIE` como respaldo.

Modelo de costes aplicado:

| Enlace | Coste OSPF |
|---|---:|
| BASE - HELI-ALFA | 10 |
| HELI-ALFA - HELI-BRAVO | 10 |
| BASE - HELI-CHARLIE | 50 |
| HELI-CHARLIE - HELI-BRAVO | 50 |

Después del ajuste, la ruta volvió correctamente a:

```text
BASE -> HELI-ALFA -> HELI-BRAVO
```

---

## 5. Evidencias

Las evidencias visuales se encuentran en la carpeta `evidence/`.

Estructura recomendada:

```text
evidence/
├── before/
│   ├── 01-ospf-neighbors-nominal.png
│   ├── 02-route-to-bravo-via-alfa.png
│   └── 03-traceroute-via-alfa.png
├── after/
│   ├── 01-primary-link-shutdown.png
│   ├── 02-ospf-neighbor-alfa-down.png
│   ├── 03-route-to-bravo-via-charlie.png
│   └── 04-traceroute-via-charlie.png
└── recovery/
    ├── 01-ospf-neighbors-recovered.png
    ├── 02-route-to-bravo-via-alfa-recovered.png
    └── 03-traceroute-via-alfa-recovered.png
```

También se incluye documentación textual de validación:

- [`evidence/manual-validation-summary.md`](evidence/manual-validation-summary.md)
- [`evidence/final-validation-results.md`](evidence/final-validation-results.md)

---

## 6. Documentación principal

- [`docs/packet-tracer-runbook.md`](docs/packet-tracer-runbook.md): guía completa paso a paso para montar y validar el laboratorio.
- [`docs/packet-tracer-4331-notes.md`](docs/packet-tracer-4331-notes.md): notas específicas para routers Cisco 4331 en Packet Tracer.
- [`docs/verification-cheatsheet.md`](docs/verification-cheatsheet.md): comandos de verificación rápida.
- [`docs/ospf-recovery-validation.md`](docs/ospf-recovery-validation.md): validación del retorno al estado nominal.
- [`docs/ospf-ecmp-cost-tuning.md`](docs/ospf-ecmp-cost-tuning.md): explicación del caso ECMP y ajuste de costes OSPF.

---

## 7. Estructura del repositorio

```text
tactical-ospf-resilience-lab/
├── README.md
├── topology/
│   ├── addressing-plan.md
│   ├── topology-description.md
│   ├── ospf-logical-topology.mmd
│   └── packet-tracer-topology.png
├── configs/
│   ├── BASE.txt
│   ├── HELI-ALFA.txt
│   ├── HELI-BRAVO.txt
│   └── HELI-CHARLIE.txt
├── docs/
│   ├── packet-tracer-runbook.md
│   ├── packet-tracer-4331-notes.md
│   ├── verification-cheatsheet.md
│   ├── ospf-recovery-validation.md
│   └── ospf-ecmp-cost-tuning.md
├── evidence/
│   ├── before/
│   ├── after/
│   ├── recovery/
│   ├── manual-validation-summary.md
│   └── final-validation-results.md
├── test-plan/
│   ├── validation-plan.md
│   ├── expected-results.md
│   └── lessons-learned.md
├── automation/
│   ├── README.md
│   ├── requirements.txt
│   ├── .env.example
│   └── collect_evidence.py
├── packet-tracer/
│   └── tactical-ospf-resilience-lab.pkt
└── linkedin/
    └── linkedin-post-draft.md
```

---

## 8. Fases del proyecto

### Fase 1 — Laboratorio manual

Completada.

1. Crear la topología en Cisco Packet Tracer.
2. Configurar interfaces y loopbacks.
3. Activar OSPF en área 0.
4. Verificar vecindades y rutas.
5. Simular caída del enlace principal.
6. Validar reconvergencia por ruta alternativa.
7. Restaurar el enlace principal.
8. Ajustar costes OSPF para eliminar ECMP y recuperar el camino preferente.
9. Documentar resultados.

### Fase 2 — Automatización

Preparada como evolución futura.

Se plantea automatizar la validación mediante Python y SSH usando Netmiko. La automatización recogerá evidencias de estado antes y después del fallo.

Archivo base:

- [`automation/collect_evidence.py`](automation/collect_evidence.py)

---

## 9. Enfoque profesional

Este proyecto demuestra capacidades prácticas en:

- Integración y validación de redes IP.
- Continuidad de comunicaciones.
- Diseño de pruebas técnicas.
- Documentación de evidencias.
- Análisis de comportamiento de routing dinámico.
- Ajuste de métricas OSPF.
- Validación de escenarios nominales, degradados y recuperados.
- Aplicación de conceptos de networking a escenarios CIS/Defensa.

El resultado es una simulación sencilla, pero técnicamente defendible, de resiliencia de red en una topología táctica IP con enrutamiento dinámico.
