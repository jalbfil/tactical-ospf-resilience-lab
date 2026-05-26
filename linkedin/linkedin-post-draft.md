# Borrador de publicación para LinkedIn

He montado un pequeño laboratorio de routing dinámico aplicado a un escenario táctico simulado.

El objetivo era representar una red formada por un puesto de mando terrestre y varios nodos aéreos/intermedios, comprobando cómo una topología redundante puede mantener la conectividad cuando se pierde un enlace.

La práctica se ha construido en Cisco Packet Tracer con:

- 4 routers: BASE, HELI-ALFA, HELI-BRAVO y HELI-CHARLIE.
- Enlaces punto a punto con subredes /30.
- Loopbacks para representar identificadores estables de cada nodo.
- OSPF en área 0 como protocolo de enrutamiento dinámico.
- Costes OSPF ajustados para observar claramente el cambio de ruta.

La prueba principal consistió en enviar tráfico desde BASE hacia HELI-BRAVO, provocar la caída del enlace BASE - HELI-ALFA y verificar cómo la red recalculaba una ruta alternativa a través de HELI-CHARLIE.

Más allá del laboratorio, la idea que me interesa es la misma que aparece en muchos entornos CIS y de comunicaciones críticas: no basta con que una red funcione en condiciones normales; debe poder degradarse, adaptarse y seguir proporcionando conectividad cuando una parte del sistema falla.

Este tipo de ejercicios me ayuda a reforzar conceptos de routing, resiliencia, validación técnica y continuidad de comunicaciones en escenarios próximos a Defensa, C2/CIS y redes tácticas.
