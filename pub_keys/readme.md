## Description 

This folder contains the ssh keys for use in encrypting sensitive files. Each user should create a folder with their preferred
username containing a public ssh key in a single file.
For simplicity of use, we assume that the encryption scheme used for now is RSA.



## Example
A user creates a folder `/internal/pub_keys/roberts/` containing a file `id_rsa.pub` which contains the public rsa keystring. 
When the PR is approved, you can then ssh to dev.xal.no with your username. In the above example we would type `ssh roberts@dev.xal.no`.

As a neat aside since the age encrpytion we use is based on the public-key in this repo this allows for easy secure file transfer inside the company.

## Nebula 
This repository contains a default configuration file to connect to the XAL https://github.com/slackhq/nebula subnetwork. 
You should install nebula  at this point. Installing nebula can be done either by downloading their pre-built binaries or compiling from source. 

Upon arriving at `dev.xal.no` you can retrieve the certification needed to set up nebula. The certificates and keys needed to connect to nebula are located in the folder `dev.xal.no:/home/sally`, in a tarball named `USER_nebula_cert.tar.gz.age`.

Using https://github.com/FiloSottile/age this tarball can be decrypted with your private ssh key. For details see: https://github.com/FiloSottile/age#ssh-keys 

Three files are contained in a folder extracted from the tarball. These three should be moved together with the `config.yml` file from this repository to `/etc/nebula/`. In the config file edit these lines:

```
pki:
  # The CAs that are accepted by this node. Must contain one or more certificates created by 'nebula-cert ca'
  ca: /etc/nebula/ca.crt
  cert: /etc/nebula/YOURNAME.laptop.crt
  key: /etc/nebula/YOURNAME.laptop.key
```
to point to your newly aquired certification files. 

Launching nebula with `nebula -config /etc/nebula/config.yml` now allows you to ssh directly to our compute-node `sally` at `USER@192.168.100.200`.
