# OSPF recovery validation

This note documents the expected checks after restoring the primary `BASE - HELI-ALFA` link.

## 1. Context

The resilience test was successful: after shutting down `BASE` interface `GigabitEthernet0/0/0`, OSPF removed the adjacency with `HELI-ALFA` and recalculated the path towards `HELI-BRAVO` through `HELI-CHARLIE`.

After the test, the primary link must be restored to confirm that the network returns to the nominal path.

## 2. Restore primary link

On `BASE`:

```ios
configure terminal
interface GigabitEthernet0/0/0
no shutdown
end
write memory
```

Expected interface state:

```text
GigabitEthernet0/0/0   10.0.1.1   up   up
```

## 3. Temporary OSPF states

Immediately after restoring the interface, OSPF may show a transitional state such as:

```text
2.2.2.2   INIT/DROTHER   10.0.1.2   GigabitEthernet0/0/0
```

This is not yet the final recovered state.

The final expected state is:

```text
2.2.2.2   FULL/...       10.0.1.2   GigabitEthernet0/0/0
4.4.4.4   FULL/...       10.0.4.2   GigabitEthernet0/0/1
```

## 4. Recovery validation commands

Run on `BASE`:

```ios
show ip ospf neighbor
show ip route 192.168.3.1
traceroute 192.168.3.1
```

## 5. Expected recovered route

After OSPF reconverges, the preferred route to `HELI-BRAVO` should return through `HELI-ALFA`:

```text
BASE -> HELI-ALFA -> HELI-BRAVO
```

Expected next hop:

```text
via 10.0.1.2, GigabitEthernet0/0/0
```

Expected traceroute:

```text
1   10.0.1.2
2   10.0.2.2
```

## 6. If the route does not return through HELI-ALFA

If the route remains through `HELI-CHARLIE`, wait a short interval and repeat:

```ios
show ip ospf neighbor
show ip route 192.168.3.1
traceroute 192.168.3.1
```

If `HELI-ALFA` remains stuck in `INIT`, check from both sides:

On `BASE`:

```ios
show ip interface brief
show ip ospf interface GigabitEthernet0/0/0
show running-config interface GigabitEthernet0/0/0
```

On `HELI-ALFA`:

```ios
show ip interface brief
show ip ospf interface GigabitEthernet0/0/0
show running-config interface GigabitEthernet0/0/0
show ip ospf neighbor
```

The interface must be `up/up`, OSPF must be active on both ends, and both routers must belong to area 0.

## 7. Professional interpretation

The full validation cycle is complete when the lab demonstrates three states:

1. Nominal state: `BASE -> HELI-ALFA -> HELI-BRAVO`.
2. Degraded state after failure: `BASE -> HELI-CHARLIE -> HELI-BRAVO`.
3. Recovered state: return to `BASE -> HELI-ALFA -> HELI-BRAVO`.
