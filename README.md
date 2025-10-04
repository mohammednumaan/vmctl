# vmctl

`vmctl` is a command-line tool to manage virtual machines in the `qemu/kvm` virtualization stack. It utilizes the `Libvirt` API to provision and manage the entire lifecycle of VM's.

![alt text](/screenshots/vmctl_banner.png)

# features

This is a basic version of `vmctl`. It contains minimal features to manage VM's. Some of the features `vmctl` supports are:

- **view basic host information**
    - viewing the host's name.
    - viewing the maximum number of vCPU's the host supports.
    - viewing the host's info (model, memory, sockets, etc).

- **lifecycle management for virtual machines**
    - provision **persistent** virtual machines. 
        - user's can provide the `name`, `memory (in MiB)`, `vCpu's` and `iso` or `disk` image file path.

    - manage entire lifecycle of virtual machines, which include:
        1. start
        2. shutdown/destroy
        3. suspend/resume
        4. reboot
      
    - view a list of virtual machines configured on this host machine.
    - view a vritual machine's info (name, memory, vCpu's, etc).


# usage


1. clone this repo.
```bash
git clone git@github.com:mohammednumaan/vmctl.git
```
2. install all the dependencies for the program to run correctly.
```bash
pip install -r requirements.txt
```
3. activate the python environment (in linux).
```bash
source .venv/bin/activate
```
4. run the program. this command shows you the list of commands you can execute.
```bash
python src/main.py
```

**Note**: 
- your system needs to support `hardware virtualization`.
- kvm, qemu, libvirt and other dependencies need to be installed on your system. 



# notes
This was a very simple project primarily to get exposed to some `virtualization` concepts and practice `python`. I plan to revisit this project in the fututre and build an end-end CLI tool to manage VM's like `virsh` and also create a GUI application like `virt-manager` to manage VM's.

This is not a production-ready version for managing VM's. There might be a lot of issues with this version, I haven't tested it in a Windows Machine. Some commands like `shutdown` might not work as expected (requires `qemu-guest-agent` to be installed on the vm). 

```
built my mohammed numaan.
```