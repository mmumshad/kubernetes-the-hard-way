# Provisioning Compute Resources

[//]: # (ignore:)

Note: You must have VirtualBox or VMWare Fusion (depending on your system) and Vagrant configured at this point. This will not work if you have less than 8GB of RAM.

Download this github repository and cd into the vagrant folder:

```bash
git clone https://github.com/mmumshad/kubernetes-the-hard-way.git
```

CD into vagrant directory:

```bash
cd kubernetes-the-hard-way/vagrant
```


Run Vagrant up. Note that on some systems vagrant takes a few seconds to start up and begin producing output.

```bash
vagrant up
```

This does the following:

- Deploys 5 VMs - 2 controlplanes, 1 loadbalancer and 2 workers with the following names
    * `controlplane01`
    * `controlplane02`
    * `loadbalancer`
    * `node01`
    * `node02`

These have a varying amount of virtual CPU and memory assigned to them according to what is detected on your laptop. The bigger your laptop, the bigger the VMs will be. This is because it's a squeeze to get 5 VMs into 8GB of memory and they may not perform very well. Therefore if you have more, we take advantage of this.

Soon after the process starts, it will display a box like this. If you need to raise questions on our forums about the VM installation, you *must* copy this output from your system and include it with your message so we can help you better.

```text
┌─────────────────────────── EXAMPLE ─────────────────────────────────┐
│ If raising a question on our forums, please include the contents    │
│ of this box with your question. It will help us to identify issues  │
│ with your system.                                                   │
│                                                                     │
│ Detecting your hardware...                                          │
│ - System: Microsoft Windows 10 Enterprise                           │
│ - CPU:    Intel(R) Core(TM) i7-7800X CPU @ 3.50GHz (12 cores)       │
│ - RAM:    32 GB                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

When the process completes successfully, it will display the names of the VMs and their IP addresses on the network (IP addresses will be different for you)

```text
192.168.0.67 controlplane01
192.168.0.68 controlplane02
192.168.0.69 loadbalancer
192.168.0.70 node01
192.168.0.71 node02
```

Note that the login credentials for all these machines is

```
Username: vagrant
Password: vagrant
```



## SSH to the nodes

There are two ways to SSH into the nodes:

### 1. SSH using Vagrant

From the directory you ran the `vagrant up` command, run `vagrant ssh <name-of-vm>` for example `vagrant ssh controlplane01`. This is the recommended way.

### 2. SSH Using SSH Client Tools

Use your favourite SSH terminal tool (e.g. putty, MobaXterm etc).

* BRIDGE Mode (default): Use the IP addresses printed at the end of the deployment and the default port `22`. Username and password-based SSH is disabled by default.
* NAT Mode: Use IP `127.0.0.1` and the port number output for the VM you want to connect to. You'll find that in the provisioner output for the VM., e.g.:

    ```text
    ==> controlplane01: Forwarding ports...
    controlplane01: 22 (guest) => 2222 (host) (adapter 1)
    ```

    Here you would use port `2222` for `controlplane01`

Vagrant generates a private key for each of these VMs. It is placed under the `.vagrant` folder (in the directory you ran the `vagrant up` command from) at the below path for each VM:

- **Private key path**: `.vagrant/machines/<machine name>/<platform>/private_key`
- **Username/password**: `vagrant/vagrant`

Replace `<machine name>` with the VM name, e.g. `controlplane01` and `<platform>` with `virtualbox` if using Virtual Box, or `wmware_desktop` if using VMware on Apple before running the command.

## Verify Environment

- Ensure all VMs are up.
- Ensure you can SSH into these VMs either using `vagrant ssh` or the IP and private keys.
- Ensure the VMs can ping each other.

## Troubleshooting Tips

### Failed Provisioning

If any of the VMs failed to provision, or is not configured correct, delete the VM using the command:

```bash
vagrant destroy <vm-name>
```

Then re-provision. Only the missing VMs will be re-provisioned

```bash
vagrant up
```

### Provisioner gets stuck

This will most likely happen at "Waiting for machine to reboot"

1. Hit `CTRL+C`
1. Kill any running `ruby` process, or Vagrant will complain.
1. Destroy the VM that got stuck: `vagrant destroy <name-of-vm>`
1. Re-provision. It will pick up where it left off: `vagrant up`

# Pausing the Environment

You do not need to complete the entire lab in one session. You may shut down and resume the environment as follows, if you need to power off your computer.

To shut down. This will gracefully shut down all the VMs in the reverse order to which they were started:

```bash
vagrant halt
```

To power on again:

```bash
vagrant up
```

Next: [Client tools](../../docs/03-client-tools.md)<br>
Prev: [Prerequisites](01-prerequisites.md)
