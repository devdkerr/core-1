import datetime
import logging
import parser

from core.emulator.coreemu import CoreEmu
from core.emulator.emudata import IpPrefixes, NodeOptions
from core.emulator.enumerations import EventTypes, NodeTypes
from core.location.mobility import BasicRangeModel


def example(args):
    # ip generator for example
    prefixes = IpPrefixes("10.83.0.0/16")

    # create emulator instance for creating sessions and utility methods
    coreemu = CoreEmu()
    session = coreemu.create_session()

    # must be in configuration state for nodes to start, when using "node_add" below
    session.set_state(EventTypes.CONFIGURATION_STATE)

    # create wlan network node
    wlan = session.add_node(_type=NodeTypes.WIRELESS_LAN)
    session.mobility.set_model(wlan, BasicRangeModel)

    # create nodes, must set a position for wlan basic range model
    options = NodeOptions(model="mdr")
    options.set_position(0, 0)
    for _ in range(args.nodes):
        node = session.add_node(options=options)
        interface = prefixes.create_interface(node)
        session.add_link(node.id, wlan.id, interface_one=interface)

    # instantiate session
    session.instantiate()

    # get nodes for example run
    first_node = session.get_node(2)
    last_node = session.get_node(args.nodes + 1)

    logging.info("starting iperf server on node: %s", first_node.name)
    first_node.cmd("iperf -s -D")
    address = prefixes.ip4_address(first_node)
    logging.info("node %s connecting to %s", last_node.name, address)
    output = last_node.cmd(f"iperf -t {args.time} -c {address}")
    logging.info(output)
    first_node.cmd("killall -9 iperf")

    # shutdown session
    coreemu.shutdown()


def main():
    logging.basicConfig(level=logging.INFO)
    args = parser.parse("wlan")

    start = datetime.datetime.now()
    logging.info("running wlan example: nodes(%s) time(%s)", args.nodes, args.time)
    example(args)
    logging.info("elapsed time: %s", datetime.datetime.now() - start)


if __name__ == "__main__":
    main()
