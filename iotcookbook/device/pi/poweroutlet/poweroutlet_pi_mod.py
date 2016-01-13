# Copyright (C) Tavendo GmbH. Open-source licensed under the
# MIT License (http://opensource.org/licenses/MIT)

import re
import sys
import argparse
import os
import pi_switch

from twisted.python import log
from twisted.internet.utils import getProcessOutput
from twisted.internet.defer import inlineCallbacks

from autobahn import wamp
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner


class PowerOutletSwitcher(ApplicationSession):
    """
    Connects the pygame mixer to WAMP.
    """

    @inlineCallbacks
    def onJoin(self, details):
        # the component has now joined the realm on the WAMP router
        log.msg("PowerOutletSwitcher connected.")

        # get custom configuration
        extra = self.config.extra

        # Device ID and auxiliary info
        self._id = extra['id']


        system_code = "11111" # the system code set as the first 5 dip switches on the ten-switch adapters we're using

        # #Basic Version - only a single outlet
        # sender = pi_switch.RCSwitchA("11111", "00010") # system code, adapter code
        # sender.enableTransmit(0) # WiringPi pin 0 = pin 11 on the Pi 2

        # def switch_outlet(state):
        #     if state == "on":
        #         sender.switchOn()
        #     elif state == "off":
        #         sender.switchOff()
        #     else:
        #         print("received unknown state to switch to", state)


        #More adapters
        adapter_codes = ["10000", "01000", "00100", "00010", "00001"]

        def switch_outlet(adapter, state):
	    print("switchoutlet_called", adapter, state)
	
            
            sender = pi_switch.RCSwitchA(system_code, adapter_codes[adapter]) # system code, adapter code
            sender.enableTransmit(0) # WiringPi pin 0 = pin 11 on the Pi 2

            if state == "on":
                sender.switchOn()
            elif state == "off":
                sender.switchOff()
            else:
                print("received unknown state to switch to", state)


        yield self.register(switch_outlet, u'io.crossbar.examples.iot.devices.pi.poweroutlet.switch')


def get_serial():
    """
    Get the Pi's serial number.
    """
    try:
        with open('/proc/cpuinfo') as f:
            for line in f.read().splitlines():
               if line.startswith('Serial'):
                   return line.split(':')[1].strip()[8:]
    except:
        pass
    return "00000000"


if __name__ == '__main__':

    # parse command line arguments
    #
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enable debug output.")

    parser.add_argument("--router", type=unicode, default=u"ws://192.168.1.136:8080/ws",
                        help='URL of WAMP router to connect to.')

    parser.add_argument("--realm", type=unicode, default=u"iot_cookbook",
                        help='The WAMP realm to join on the router.')

    parser.add_argument("--id", type=unicode, default=None,
                        help='The Device ID to use. Default is to use the RaspberryPi Serial Number')

    args = parser.parse_args()

    # start logging to stdout
    #
    log.startLogging(sys.stdout)

    # get the Pi's serial number (allow override from command line)
    #
    if args.id is None:
        args.id = get_serial()
    log.msg("AudioOutputAdapter starting with Device ID {} ...".format(args.id))

    # install the "best" available Twisted reactor
    #
    from autobahn.twisted.choosereactor import install_reactor
    reactor = install_reactor()
    log.msg("Running on reactor {}".format(reactor))

    # custom configuration data
    #
    extra = {
        # device ID
        'id': args.id,
    }

    # create and start app runner for our app component ..
    #
    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra, debug=args.debug)
    runner.run(PowerOutletSwitcher)
