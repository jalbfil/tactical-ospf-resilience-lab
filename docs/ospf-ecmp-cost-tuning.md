# OSPF ECMP and cost tuning

This note documents an important observation during the recovery phase of the lab: after the primary link was restored, OSPF installed two equal-cost paths towards `HELI-BRAVO`.

## 1. Observed state

After restoring `BASE - HELI-ALFA`, both OSPF adjacencies were fully established:

```text
Neighbor ID     State      Address     Interface
2.2.2.2         FULL/DR    10.0.1.2    GigabitEthernet0/0/0
4.4.4.4         FULL/DR    10.0.4.2    GigabitEthernet0/0/1
```

The route towards `192.168.3.1/32` showed two valid next hops with the same metric:

```text
Routing Descriptor Blocks:
* 10.0.4.2, from 3.3.3.3, via GigabitEthernet0/0/1
  Route metric is 3, traffic share count is 1
  10.0.1.2, from 3.3.3.3, via GigabitEthernet0/0/0
  Route metric is 3, traffic share count is 1
```

## 2. Interpretation

This is not a failure.

It means OSPF sees both paths as having the same total cost and installs both in the routing table. This behavior is known as ECMP: Equal-Cost Multi-Path.

Functional interpretation:

```text
Path A: BASE -> HELI-ALFA -> HELI-BRAVO
Path B: BASE -> HELI-CHARLIE -> HELI-BRAVO
```

Both are valid because both have equal OSPF metric.

## 3. Why it matters for this lab

For a professional networking lab, ECMP is an interesting result because it demonstrates that the network has more than one valid path.

However, for a clear before/failure/after demonstration, it is preferable to force a deterministic primary path and a deterministic backup path:

```text
Primary path: BASE -> HELI-ALFA -> HELI-BRAVO
Backup path:  BASE -> HELI-CHARLIE -> HELI-BRAVO
```

This is achieved by changing OSPF interface costs.

## 4. Recommended cost model

Use lower costs on the primary path and higher costs on the backup path.

| Link | Recommended OSPF cost |
|---|---:|
| BASE - HELI-ALFA | 10 |
| HELI-ALFA - HELI-BRAVO | 10 |
| BASE - HELI-CHARLIE | 50 |
| HELI-CHARLIE - HELI-BRAVO | 50 |

Expected total cost:

```text
Primary path: 10 + 10 = 20
Backup path:  50 + 50 = 100
```

## 5. Configuration commands

### BASE

```ios
configure terminal
interface GigabitEthernet0/0/0
 ip ospf cost 10
interface GigabitEthernet0/0/1
 ip ospf cost 50
end
write memory
```

### HELI-ALFA

```ios
configure terminal
interface GigabitEthernet0/0/0
 ip ospf cost 10
interface GigabitEthernet0/0/1
 ip ospf cost 10
end
write memory
```

### HELI-BRAVO

```ios
configure terminal
interface GigabitEthernet0/0/0
 ip ospf cost 10
interface GigabitEthernet0/0/1
 ip ospf cost 50
end
write memory
```

### HELI-CHARLIE

```ios
configure terminal
interface GigabitEthernet0/0/0
 ip ospf cost 50
interface GigabitEthernet0/0/1
 ip ospf cost 50
end
write memory
```

## 6. Recalculate OSPF

After applying the costs, wait a few seconds and run on `BASE`:

```ios
show ip route 192.168.3.1
traceroute 192.168.3.1
```

Expected result:

```text
via 10.0.1.2, GigabitEthernet0/0/0
```

Expected traceroute:

```text
1   10.0.1.2
2   10.0.2.2
```

If the routing table does not refresh immediately, use this on the routers:

```ios
clear ip ospf process
```

Confirm with `yes` when prompted.

> Note: in a production environment this command would disrupt OSPF adjacencies temporarily. In this Packet Tracer lab, it is acceptable for validation purposes.

## 7. Final expected behavior

After cost tuning, the full validation should show:

1. Nominal state: traffic uses `BASE -> HELI-ALFA -> HELI-BRAVO`.
2. Failure state: after shutting down `BASE - HELI-ALFA`, traffic uses `BASE -> HELI-CHARLIE -> HELI-BRAVO`.
3. Recovery state: after restoring `BASE - HELI-ALFA`, traffic returns to `BASE -> HELI-ALFA -> HELI-BRAVO`.
