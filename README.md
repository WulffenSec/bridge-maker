# BRIDGE MAKER

## What is it?
> It's a simple script to automate the creation of a bridge for your network using NetworkManager, instead of using the default interface.

> As well providing an automation for setting that bridge as default interface in "virsh" the cli tool for libvirt (Virt-Manager).

## Whats required?

- python
- ip
- nmcli
- virsh (Optional)

## How it work?

#### In your terminal
```
git clone https://www.github.com/dotvectortech/bridge-maker.git
cd bridge-maker
python bridge-maker.py
```
The script will ask you for to choose the right interface you want to transform into a bridge. 

As well if you prefer to use the bridge as default interface for libvirt (Virt-Manager) instead using the default Virtual NAT.
