#!/usr/bin/env bash

[ -z "$(sudo swapon -s)"] && exit 0

echo "--> Disabling swap"
sudo swapoff -a
sudo sed -i '/swap.img/d' /etc/fstab
echo "--> Disabling swap"
echo "--> Done"
