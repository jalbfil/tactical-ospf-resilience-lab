# Lecciones aprendidas

## 1. Redundancia física y lógica

La existencia de enlaces alternativos permite que la pérdida de un enlace no implique necesariamente pérdida de servicio.

## 2. Importancia del plano de control

OSPF actúa como plano de control distribuido, intercambiando información de red y recalculando rutas cuando cambia la topología.

## 3. Costes y diseño de rutas

Los costes OSPF permiten influir en la selección de caminos. En este laboratorio se han utilizado para diferenciar un camino principal y un camino alternativo.

## 4. Validación técnica

La prueba no se considera completa solo porque exista conectividad. Es necesario conservar evidencias de:

- Estado de interfaces.
- Vecindades OSPF.
- Ruta instalada.
- Camino observado con traceroute.
- Recuperación efectiva del tráfico.

## 5. Aplicación a entornos CIS/Defensa

En escenarios de comunicaciones críticas, la clave no es únicamente desplegar una red funcional, sino diseñarla, probarla y documentarla para operar en condiciones degradadas.
