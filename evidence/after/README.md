# Evidencias después del fallo

Guardar aquí las capturas y salidas de comandos posteriores al apagado del enlace `BASE - HELI-ALFA`.

Comando para provocar el fallo en BASE:

```ios
configure terminal
interface gigabitEthernet0/0
shutdown
end
```

Comandos recomendados desde BASE:

```ios
show ip ospf neighbor
show ip route 192.168.3.1
traceroute 192.168.3.1
ping 192.168.3.1 source 192.168.1.1
```
