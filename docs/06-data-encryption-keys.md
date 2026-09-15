# Generating the Data Encryption Config and Key

Kubernetes stores a variety of data including cluster state, application configurations, and secrets. Kubernetes supports the ability to [encrypt](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data) cluster data at rest, that is, the data stored within `etcd`.

In this lab you will generate an encryption key and an [encryption config](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/#understanding-the-encryption-at-rest-configuration) suitable for encrypting Kubernetes Secrets.

## The Encryption Key

[//]: # (host:controlplane01)

Generate an encryption key. This is simply 32 bytes of random data, which we base64 encode:

```bash
ENCRYPTION_KEY=$(head -c 32 /dev/urandom | base64)
```

## The Encryption Config File

Create the `encryption-config.yaml` encryption config file:

```bash
cat > encryption-config.yaml <<EOF
kind: EncryptionConfiguration
apiVersion: apiserver.config.k8s.io/v1
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: ${ENCRYPTION_KEY}
      - identity: {}
EOF
```

Copy the `encryption-config.yaml` encryption config file to each controller instance:

```bash
for instance in controlplane01 controlplane02; do
  scp encryption-config.yaml ${instance}:~/
done
```

At this point, the encryption configuration file has been created and copied to all control plane nodes. However, **creating this file alone does not enable encryption at rest**.

The `kube-apiserver` must be configured to use this file by specifying the `--encryption-provider-config` option. When configured, the API server uses the encryption provider to encrypt supported resources, such as Secrets, **before persisting them to etcd**.

We will configure the `kube-apiserver` to use this encryption configuration in the upcoming section, when we create its systemd unit file.

Move `encryption-config.yaml` encryption config file to appropriate directory.

```bash
for instance in controlplane01 controlplane02; do
  ssh ${instance} sudo mkdir -p /var/lib/kubernetes/
  ssh ${instance} sudo mv encryption-config.yaml /var/lib/kubernetes/
done
```

Reference: https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/#encrypting-your-data

Next: [Bootstrapping the etcd Cluster](07-bootstrapping-etcd.md)<br>
Prev: [Generating Kubernetes Configuration Files for Authentication](05-kubernetes-configuration-files.md)
