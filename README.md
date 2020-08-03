# botnet

**This repo is created only for educational purpose, use on your own risk.**

Simple SSH scanner in very case specific local network, where each computer have the same login and password.
Script loads payload from specified URL on each open server.

## Requirements

+ `python3-nmap` from PyPI
+ `sshpass`

On Debian machine you can use `init_main.sh` script to install requirements.

## Usage

To use it you should edit `ctx` object in `botnet.py` file and run it on computer in the same network.
