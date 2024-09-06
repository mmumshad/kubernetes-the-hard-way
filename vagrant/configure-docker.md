# Configuring docker on Linux Playgrounds

## Overview

Note that there is also a specific [Docker playground](https://kodekloud.com/playgrounds/playground-docker) running Ubuntu 20.04 where docker is preinstalled and all the steps below are already applied.

You have successfully installed Docker on a Linux playground, however you are receiving an error like the following when you try to pull or run any image

> You have reached your pull rate limit You may increase the rate limit by authenticating and upgrading...

This is due to policies introduced by Docker to encourage more people to upgrade their accounts (at a cost).

## Fix

To get round this, KodeKloud have an internal docker repository containing many common images that students will want to work with. Now we must edit some things to make the docker client work with the internal registry.

In Linux playgrounds you should already be logged in as `root`. If not, become root with `sudo -i`

1. Edit hosts file to add an entry for the internal registry.

    ```bash
    echo "10.0.0.6        docker-registry-mirror.kodekloud.com" >> /etc/hosts
    ```

1. Create a configuration file for the docker daemon to point to the internal registry

    ```bash
    mkdir -p /etc/docker
    cat <<EOF > /etc/docker/daemon.json
    {
        "exec-opts": [
            "native.cgroupdriver=cgroupfs"
        ],
        "bip":"172.12.0.1/24",
        "registry-mirrors": [
            "http://docker-registry-mirror.kodekloud.com"
       ]
    }
    EOF
    ```

1. Restart docker

    ```bash
    systemctl restart docker
    ```

1. Test

    ```bash
    docker pull nginx
    ```

## Installing Docker

### Ubuntu Playground

You should already be logged in as `root`.

Execute the following commands as root

```bash
apt update
apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" >> /etc/apt/sources.list.d/docker.list
apt update
apt-cache policy docker-ce
apt install -y docker-ce
```

### CentOS playground

CentOS is pre-installed with Red Hat PodMan. To replace this with the real Docker, execute the following commands. You should be logged in as `bob`

```bash
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo yum install -y --allowerasing  docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo chmod a+rw /var/run/docker.sock
```

