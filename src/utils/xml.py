"""
This module provides a function to create an XML configuration for a new virtual machine.
"""
from utils.errors import VmctlError

def create_xml_config(vm_name: str, vm_memory: int, vm_vcpus: int, iso_path: str = None, disk_path: str = None):
    """
    Creates an XML configuration for a new virtual machine.

    Args:
        vm_name (str): The name of the virtual machine.
        vm_memory (int): The amount of memory for the virtual machine in MiB.
        vm_vcpus (int): The number of virtual CPUs for the virtual machine.
        iso_path (str, optional): The path to the ISO file for the virtual machine. Defaults to None.
        disk_path (str, optional): The path to the disk file for the virtual machine. Defaults to None.

    Raises:
        VmctlError: If both or neither iso_path and disk_path are provided.

    Returns:
        str: The XML configuration for the virtual machine.
    """
    # i need to create a basic xml config for
    # provisioning a new virtual machine
    # reference: https://libvirt.org/formatdomain.html

    if not disk_path and not iso_path:
        raise VmctlError("Either disk_path or iso_path must be provided")
    

    if iso_path and disk_path:
        raise VmctlError("Only one of disk_path or iso_path should be provided")
    

    if iso_path:
        boot_device = "cdrom"
        xml_device_config = f"""
        <disk type='file' device='cdrom'>
            <driver name='qemu' type='raw'/>
            <source file='{iso_path}'/>
            <target dev='hdc' bus='ide'/>
            <readonly/>
        </disk>
        """

    elif disk_path:
        boot_device = "hd"
        xml_device_config = f"""
        <disk type='file' device='disk'>
            <driver name='qemu' type='qcow2'/>
            <source file='{disk_path}'/>
            <target dev='vda' bus='virtio'/>

        </disk>
        """

    xml_string = f"""

<domain type='kvm'>
  <name>{vm_name}</name>
    <memory unit='MiB'>{vm_memory}</memory>
    <vcpu placement='static'>{vm_vcpus}</vcpu>
    
    <os>
        <type arch="x86_64" machine="pc">hvm</type>
        <boot dev="{boot_device}"/>
    </os>
    <devices>
        <emulator>/usr/bin/qemu-system-x86_64</emulator>
        {xml_device_config}
        <interface type='network'>
            <source network='default'/>
        </interface>
        <graphics type='vnc' port='-1' autoport='yes'/>
    </devices>

</domain>
    """

    return xml_string