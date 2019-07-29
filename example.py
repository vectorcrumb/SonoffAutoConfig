from sonoff_control.control import SonoffController

sonoff = SonoffController("192.168.0.27")
sonoff.initialize()
sonoff.set_state([False, False])