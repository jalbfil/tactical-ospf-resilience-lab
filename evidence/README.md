# Evidencias

Esta carpeta recoge las capturas y salidas de comandos que demuestran el funcionamiento del laboratorio.

## Evidencias antes del fallo

Guardar en `before/`:

- Topología completa con todos los enlaces activos.
- `show ip ospf neighbor`.
- `show ip route 192.168.3.1` ejecutado desde BASE.
- `traceroute 192.168.3.1` ejecutado desde BASE.
- `ping 192.168.3.1 source 192.168.1.1`.

## Evidencias después del fallo

Guardar en `after/`:

- Topología con el enlace BASE - HELI-ALFA caído.
- `show ip ospf neighbor` tras la convergencia.
- `show ip route 192.168.3.1` ejecutado desde BASE.
- `traceroute 192.168.3.1` ejecutado desde BASE.
- `ping 192.168.3.1 source 192.168.1.1`.

## Formato recomendado

Nombrar los ficheros con prefijo numérico:

```text
01-topology-before.png
02-ospf-neighbors-before.png
03-route-before.png
04-traceroute-before.png
05-failover-event.png
06-route-after.png
07-traceroute-after.png
08-ping-after.png
```
