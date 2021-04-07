#!/usr/bin/env bash

ip rule add from 10.0.0.2 table 1
ip rule add from 10.0.0.3 table 2
ip rule add from 10.0.0.4 table 3

ip route add 10.0.0.0/8 dev clientmp-eth0 scope link table 1
ip route add default via 10.0.0.22 dev clientmp-eth0 table 1
ip route add 10.0.0.0/8 dev clientmp-eth1 scope link table 2
ip route add default via 10.0.0.22 dev clientmp-eth1 table 2
ip route add 10.0.0.0/8 dev clientmp-eth2 scope link table 3
ip route add default via 10.0.0.22 dev clientmp-eth2 table 3

