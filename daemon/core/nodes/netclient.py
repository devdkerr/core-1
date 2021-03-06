"""
Clients for dealing with bridge/interface commands.
"""
import json

from core.constants import ETHTOOL_BIN, IP_BIN, OVS_BIN, TC_BIN


def get_net_client(use_ovs, run):
    """
    Retrieve desired net client for running network commands.

    :param bool use_ovs: True for OVS bridges, False for Linux bridges
    :param func run: function used to run net client commands
    :return: net client class
    """
    if use_ovs:
        return OvsNetClient(run)
    else:
        return LinuxNetClient(run)


class LinuxNetClient:
    """
    Client for creating Linux bridges and ip interfaces for nodes.
    """

    def __init__(self, run):
        """
        Create LinuxNetClient instance.

        :param run: function to run commands with
        """
        self.run = run

    def set_hostname(self, name):
        """
        Set network hostname.

        :param str name: name for hostname
        :return: nothing
        """
        self.run(f"hostname {name}")

    def create_route(self, route, device):
        """
        Create a new route for a device.

        :param str route: route to create
        :param str device: device to add route to
        :return: nothing
        """
        self.run(f"{IP_BIN} route add {route} dev {device}")

    def device_up(self, device):
        """
        Bring a device up.

        :param str device: device to bring up
        :return: nothing
        """
        self.run(f"{IP_BIN} link set {device} up")

    def device_down(self, device):
        """
        Bring a device down.

        :param str device: device to bring down
        :return: nothing
        """
        self.run(f"{IP_BIN} link set {device} down")

    def device_name(self, device, name):
        """
        Set a device name.

        :param str device: device to set name for
        :param str name: name to set
        :return: nothing
        """
        self.run(f"{IP_BIN} link set {device} name {name}")

    def device_show(self, device):
        """
        Show information for a device.

        :param str device: device to get information for
        :return: device information
        :rtype: str
        """
        return self.run(f"{IP_BIN} link show {device}")

    def get_mac(self, device):
        """
        Retrieve MAC address for a given device.

        :param str device: device to get mac for
        :return: MAC address
        :rtype: str
        """
        return self.run(f"cat /sys/class/net/{device}/address")

    def get_ifindex(self, device):
        """
        Retrieve ifindex for a given device.

        :param str device: device to get ifindex for
        :return: ifindex
        :rtype: str
        """
        return self.run(f"cat /sys/class/net/{device}/ifindex")

    def device_ns(self, device, namespace):
        """
        Set netns for a device.

        :param str device: device to setns for
        :param str namespace: namespace to set device to
        :return: nothing
        """
        self.run(f"{IP_BIN} link set {device} netns {namespace}")

    def device_flush(self, device):
        """
        Flush device addresses.

        :param str device: device to flush
        :return: nothing
        """
        self.run(
            f"[ -e /sys/class/net/{device} ] && {IP_BIN} -6 address flush dev {device} || true",
            shell=True,
        )

    def device_mac(self, device, mac):
        """
        Set MAC address for a device.

        :param str device: device to set mac for
        :param str mac: mac to set
        :return: nothing
        """
        self.run(f"{IP_BIN} link set dev {device} address {mac}")

    def delete_device(self, device):
        """
        Delete device.

        :param str device: device to delete
        :return: nothing
        """
        self.run(f"{IP_BIN} link delete {device}")

    def delete_tc(self, device):
        """
        Remove traffic control settings for a device.

        :param str device: device to remove tc
        :return: nothing
        """
        self.run(f"{TC_BIN} qdisc delete dev {device} root")

    def checksums_off(self, interface_name):
        """
        Turns interface checksums off.

        :param str interface_name: interface to update
        :return: nothing
        """
        self.run(f"{ETHTOOL_BIN} -K {interface_name} rx off tx off")

    def create_address(self, device, address, broadcast=None):
        """
        Create address for a device.

        :param str device: device to add address to
        :param str address: address to add
        :param str broadcast: broadcast address to use, default is None
        :return: nothing
        """
        if broadcast is not None:
            self.run(
                f"{IP_BIN} address add {address} broadcast {broadcast} dev {device}"
            )
        else:
            self.run(f"{IP_BIN} address add {address} dev {device}")

    def delete_address(self, device, address):
        """
        Delete an address from a device.

        :param str device: targeted device
        :param str address: address to remove
        :return: nothing
        """
        self.run(f"{IP_BIN} address delete {address} dev {device}")

    def create_veth(self, name, peer):
        """
        Create a veth pair.

        :param str name: veth name
        :param str peer: peer name
        :return: nothing
        """
        self.run(f"{IP_BIN} link add name {name} type veth peer name {peer}")

    def create_gretap(self, device, address, local, ttl, key):
        """
        Create a GRE tap on a device.

        :param str device: device to add tap to
        :param str address: address to add tap for
        :param str local: local address to tie to
        :param int ttl: time to live value
        :param int key: key for tap
        :return: nothing
        """
        cmd = f"{IP_BIN} link add {device} type gretap remote {address}"
        if local is not None:
            cmd += f" local {local}"
        if ttl is not None:
            cmd += f" ttl {ttl}"
        if key is not None:
            cmd += f" key {key}"
        self.run(cmd)

    def create_bridge(self, name):
        """
        Create a Linux bridge and bring it up.

        :param str name: bridge name
        :return: nothing
        """
        self.run(f"{IP_BIN} link add name {name} type bridge")
        self.run(f"{IP_BIN} link set {name} type bridge stp_state 0")
        self.run(f"{IP_BIN} link set {name} type bridge forward_delay 0")
        self.run(f"{IP_BIN} link set {name} type bridge mcast_snooping 0")
        self.device_up(name)

    def delete_bridge(self, name):
        """
        Bring down and delete a Linux bridge.

        :param str name: bridge name
        :return: nothing
        """
        self.device_down(name)
        self.run(f"{IP_BIN} link delete {name} type bridge")

    def create_interface(self, bridge_name, interface_name):
        """
        Create an interface associated with a Linux bridge.

        :param str bridge_name: bridge name
        :param str interface_name: interface name
        :return: nothing
        """
        self.run(f"{IP_BIN} link set dev {interface_name} master {bridge_name}")
        self.device_up(interface_name)

    def delete_interface(self, bridge_name, interface_name):
        """
        Delete an interface associated with a Linux bridge.

        :param str bridge_name: bridge name
        :param str interface_name: interface name
        :return: nothing
        """
        self.run(f"{IP_BIN} link set dev {interface_name} nomaster")

    def existing_bridges(self, _id):
        """
        Checks if there are any existing Linux bridges for a node.

        :param _id: node id to check bridges for
        """
        output = self.run(f"{IP_BIN} -j link show type bridge")
        bridges = json.loads(output)
        for bridge in bridges:
            name = bridge["ifname"]
            fields = name.split(".")
            if len(fields) != 3:
                continue
            if fields[0] == "b" and fields[1] == _id:
                return True
        return False

    def disable_mac_learning(self, name):
        """
        Disable mac learning for a Linux bridge.

        :param str name: bridge name
        :return: nothing
        """
        self.run(f"{IP_BIN} link set {name} type bridge ageing_time 0")


class OvsNetClient(LinuxNetClient):
    """
    Client for creating OVS bridges and ip interfaces for nodes.
    """

    def create_bridge(self, name):
        """
        Create a OVS bridge and bring it up.

        :param str name: bridge name
        :return: nothing
        """
        self.run(f"{OVS_BIN} add-br {name}")
        self.run(f"{OVS_BIN} set bridge {name} stp_enable=false")
        self.run(f"{OVS_BIN} set bridge {name} other_config:stp-max-age=6")
        self.run(f"{OVS_BIN} set bridge {name} other_config:stp-forward-delay=4")
        self.device_up(name)

    def delete_bridge(self, name):
        """
        Bring down and delete a OVS bridge.

        :param str name: bridge name
        :return: nothing
        """
        self.device_down(name)
        self.run(f"{OVS_BIN} del-br {name}")

    def create_interface(self, bridge_name, interface_name):
        """
        Create an interface associated with a network bridge.

        :param str bridge_name: bridge name
        :param str interface_name: interface name
        :return: nothing
        """
        self.run(f"{OVS_BIN} add-port {bridge_name} {interface_name}")
        self.device_up(interface_name)

    def delete_interface(self, bridge_name, interface_name):
        """
        Delete an interface associated with a OVS bridge.

        :param str bridge_name: bridge name
        :param str interface_name: interface name
        :return: nothing
        """
        self.run(f"{OVS_BIN} del-port {bridge_name} {interface_name}")

    def existing_bridges(self, _id):
        """
        Checks if there are any existing OVS bridges for a node.

        :param _id: node id to check bridges for
        """
        output = self.run(f"{OVS_BIN} list-br")
        if output:
            for line in output.split("\n"):
                fields = line.split(".")
                if fields[0] == "b" and fields[1] == _id:
                    return True
        return False

    def disable_mac_learning(self, name):
        """
        Disable mac learning for a OVS bridge.

        :param str name: bridge name
        :return: nothing
        """
        self.run(f"{OVS_BIN} set bridge {name} other_config:mac-aging-time=0")
