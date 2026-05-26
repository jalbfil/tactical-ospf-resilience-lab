# Automatización futura

Esta carpeta queda preparada para la Fase 2 del proyecto: automatización de la validación mediante Python y SSH.

## Objetivo

Automatizar la recogida de evidencias antes y después de una caída de enlace.

## Herramienta propuesta

- Python 3.10+
- Netmiko

## Funciones previstas

1. Conectarse por SSH a cada router.
2. Ejecutar comandos de verificación.
3. Guardar salidas en ficheros `.txt`.
4. Apagar o levantar interfaces de prueba.
5. Generar evidencias comparables antes/después.

## Comandos a automatizar

```ios
show ip interface brief
show ip ospf neighbor
show ip route
show ip route 192.168.3.1
traceroute 192.168.3.1
```

## Nota

Cisco Packet Tracer tiene limitaciones para automatización externa real. Esta fase puede realizarse posteriormente en GNS3, EVE-NG o equipos Cisco IOS/IOSv reales o virtualizados.
