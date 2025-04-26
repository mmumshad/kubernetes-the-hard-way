# Provisioning Pod Network

Container Network Interface (CNI) is a standard interface for managing IP networks between containers across many nodes.

We chose to use CNI - [weave](https://github.com/weaveworks/weave) as our networking option.


### Deploy Weave Network

Some of you may have noticed the announcement that WeaveWorks is no longer trading. At this time, this does not mean that Weave is not a valid CNI. WeaveWorks software has always been and remains to be open source, and as such is still useable. It just means that the company is no longer providing updates. While it continues to be compatible with Kubernetes, we will continue to use it as the other options (e.g. Calico, Cilium) require far more configuration steps.

Weave sets its [default network CIDR](https://github.com/weaveworks/weave/blob/master/site/kubernetes/kube-addon.md#-changing-configuration-options) to '10.32.0.0/12', which means we need to modify it before the installation
to match the [CIDR we picked](01-prerequisites.md#pod-network) at the beginning for our POD network - ie. '10.244.0.0/16'.

[//]: # (host:controlplane01)

On `controlplane01`

Download the weave manifest:

```bash
curl -LO "https://github.com/weaveworks/weave/releases/download/v2.8.1/weave-daemonset-k8s-1.11.yaml"
```

Manually edit the manifest and set the correct POD network CIDR via IPALLOC_RANGE environment variable:

```
vim weave-daemonset-k8s-1.11.yaml

...
containers:
- name: weave
    env:
    ...
    - name: IPALLOC_RANGE
        value: 10.244.0.0/16
...
```

Deploy weave network. Run only once on the `controlplane01` node. You may see a warning, but this is OK:

```bash
kubectl apply -f weave-daemonset-k8s-1.11.yaml

```

It may take up to 60 seconds for the Weave pods to be ready.

## Verification

[//]: # (command:kubectl rollout status daemonset weave-net -n kube-system --timeout=90s)

List the registered Kubernetes nodes from the controlplane node:

```bash
kubectl get pods -n kube-system
```

Output will be similar to

```
NAME              READY   STATUS    RESTARTS   AGE
weave-net-58j2j   2/2     Running   0          89s
weave-net-rr5dk   2/2     Running   0          89s
```

Once the Weave pods are fully running, the nodes should be ready.

```bash
kubectl get nodes
```

Output will be similar to

```
NAME       STATUS   ROLES    AGE     VERSION
node01     Ready    <none>   4m11s   v1.28.4
node02     Ready    <none>   2m49s   v1.28.4
```

Reference: https://kubernetes.io/docs/tasks/administer-cluster/network-policy-provider/weave-network-policy/#install-the-weave-net-addon

Next: [Kube API Server to Kubelet Connectivity](./14-kube-apiserver-to-kubelet.md)</br>
Prev: [Configuring Kubectl](./12-configuring-kubectl.md)
