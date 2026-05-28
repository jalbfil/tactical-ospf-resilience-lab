# Final validation results

This document records the final successful validation of the OSPF resilience lab after applying OSPF cost tuning.

## 1. Cost tuning applied

The lab initially produced ECMP because both paths from `BASE` to `HELI-BRAVO` had the same OSPF metric.

To make the demonstration deterministic, OSPF costs were adjusted to create a preferred primary path and a higher-cost backup path.

| Link | OSPF cost |
|---|---:|
| BASE - HELI-ALFA | 10 |
| HELI-ALFA - HELI-BRAVO | 10 |
| BASE - HELI-CHARLIE | 50 |
| HELI-CHARLIE - HELI-BRAVO | 50 |

## 2. Nominal recovered path

After setting the OSPF costs on `BASE`, the route towards `HELI-BRAVO` returned to the intended primary path.

Observed route from `BASE`:

```text
Routing entry for 192.168.3.1/32
Known via "ospf 1", distance 110, metric 21, type intra area
Last update from 10.0.1.2 on GigabitEthernet0/0/0
Routing Descriptor Blocks:
* 10.0.1.2, from 3.3.3.3, via GigabitEthernet0/0/0
  Route metric is 21, traffic share count is 1
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

## 3. Meaning of metric 21

The metric is expected because the path cost includes:

```text
BASE -> HELI-ALFA   cost 10
HELI-ALFA -> BRAVO  cost 10
Destination loopback cost contribution
```

The important validation point is not the exact number itself, but the fact that the route uses the intended next hop:

```text
via 10.0.1.2, GigabitEthernet0/0/0
```

## 4. Final validation cycle

The lab now demonstrates the complete cycle:

1. Nominal state:

```text
BASE -> HELI-ALFA -> HELI-BRAVO
```

2. Failure state after shutting down the primary link:

```text
BASE - HELI-ALFA down
```

3. Degraded state:

```text
BASE -> HELI-CHARLIE -> HELI-BRAVO
```

4. Recovery state after restoring the primary link and tuning OSPF costs:

```text
BASE -> HELI-ALFA -> HELI-BRAVO
```

## 5. Result

The lab objective has been achieved.

The topology demonstrates dynamic routing resilience with OSPF in a redundant tactical IP topology. It shows nominal operation, link failure, route reconvergence, alternative path usage and recovery to the preferred path.
