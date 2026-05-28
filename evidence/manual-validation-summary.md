# Manual validation summary

This file documents the first successful manual validation of the Packet Tracer OSPF resilience lab.

## 1. Initial state

The topology was built using Cisco 4331 routers in Cisco Packet Tracer.

Interfaces and loopbacks were configured and verified as active.

## 2. Issue detected

The initial OSPF path from `BASE` to `HELI-BRAVO` worked correctly through `HELI-ALFA`, but `BASE` did not initially form an OSPF adjacency with `HELI-CHARLIE`.

The cause was that `BASE` interface `GigabitEthernet0/0/1` was administratively down.

Observed state:

```text
BASE
GigabitEthernet0/0/1   10.0.4.1   administratively down down

HELI-CHARLIE
GigabitEthernet0/0/1   10.0.4.2   up down
```

Corrective action on `BASE`:

```ios
configure terminal
interface gigabitEthernet0/0/1
no shutdown
end
write memory
```

After this correction, `GigabitEthernet0/0/1` changed to `up/up` and OSPF formed adjacency with `HELI-CHARLIE`.

## 3. Nominal path validation

Before simulating the failure, `BASE` reached `HELI-BRAVO` through `HELI-ALFA`.

Observed route:

```text
Routing entry for 192.168.3.1/32
Known via "ospf 1", distance 110, metric 3, type intra area
Last update from 10.0.1.2 on GigabitEthernet0/0/0
```

Observed traceroute:

```text
Tracing the route to 192.168.3.1

1   10.0.1.2
2   10.0.2.2
```

Functional interpretation:

```text
BASE -> HELI-ALFA -> HELI-BRAVO
```

## 4. Failure simulation

The primary link `BASE - HELI-ALFA` was disabled from `BASE`:

```ios
configure terminal
interface GigabitEthernet0/0/0
shutdown
end
```

Observed OSPF event:

```text
%OSPF-5-ADJCHG: Process 1, Nbr 2.2.2.2 on GigabitEthernet0/0/0 from FULL to DOWN, Neighbor Down: Interface down or detached
```

After the failure, `BASE` maintained OSPF adjacency with `HELI-CHARLIE`:

```text
Neighbor ID     Pri   State           Dead Time   Address         Interface
4.4.4.4           1   FULL/DR         00:00:32    10.0.4.2        GigabitEthernet0/0/1
```

## 5. Degraded path validation

After the primary link failure, OSPF recalculated the route towards `HELI-BRAVO` through `HELI-CHARLIE`.

Observed route:

```text
Routing entry for 192.168.3.1/32
Known via "ospf 1", distance 110, metric 3, type intra area
Last update from 10.0.4.2 on GigabitEthernet0/0/1
```

Observed traceroute:

```text
Tracing the route to 192.168.3.1

1   10.0.4.2
2   10.0.3.1
```

Functional interpretation:

```text
BASE -> HELI-CHARLIE -> HELI-BRAVO
```

## 6. Result

The manual validation was successful.

The lab demonstrates that, after the loss of the primary link between `BASE` and `HELI-ALFA`, OSPF reconverges and preserves reachability towards `HELI-BRAVO` through the alternative path via `HELI-CHARLIE`.

This validates the main objective of the lab: dynamic routing resilience in a redundant tactical IP topology.
