import libvirt
from wrapper.host import HostApi
from wrapper.vm import VMApi


class LibVirtApi:
    def __init__(self):
        self.connection = self._connect()
        self.host_api = HostApi(self.connection)
        self.vm_api = VMApi(self.connection)


    def _connect(self, uri: str = 'qemu:///system'):
        conn = libvirt.open(uri)
        if conn is None:
            raise Exception('Failed to open connection to local qemu.')
        return conn

    def close(self, conn):
        if conn:
            conn.close()