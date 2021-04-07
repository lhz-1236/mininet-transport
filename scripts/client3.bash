#!/usr/bin/env bash

ip rule add from 10.0.0.5 table 1
ip route add 10.0.0.0/8 dev client3-eth0 scope link table 1
ip route add default via 10.0.0.23 dev client3-eth0 table 1
