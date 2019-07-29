import requests, json
from typing import Tuple, List

URL_TEMPLATE_GET = "http://{}/cm?cmnd=Template"
URL_TEMPLATE_SET = "http://{}/cm?cmnd=Template%20{}"
URL_POWER = "http://{}/cm?cmnd=Power{}%20{}"
MODULE_TEMPLATE_CODE = 39
CHANNEL_CODES = [1, 2]

class SonoffInitException(Exception):
    pass


class SonoffController():

    def __init__(self, ip: str):
        self.addr = ip
        self.template_init = False
        self.connected = False
    
    def _check_connection(self) -> bool:
        """Checks to see if a connection can be established to the Sonoff relay. 
        This is done by sending a request to the Sonoff relay and then checking for a 
        200 HTTP status code on the response.
        
        Returns:
            bool -- True if a 200 code is received, false otherwise.
        """
        status = requests.get(URL_TEMPLATE_GET.format(self.addr)).status_code
        return status == 200
    
    def _check_init_state(self) -> bool:
        """Checks to see if the Sonoff Dual R2 template has already been configured.
        This is a workaround due to not being able to set a template during the firmware
        building process.
        
        Returns:
            bool -- True is module template corresponds to the Dual R2.
        """
        respj = requests.get(URL_TEMPLATE_GET.format(self.addr)).json()
        return respj['NAME'] == "Sonoff Dual R2"
    
    def _ready(self) -> bool:
        """Helper function to indicate if both initialization checks are completed
        
        Returns:
            bool -- True if both checks are valid
        """
        return self.template_init and self.connected
    
    def initialize(self) -> bool:
        """Function to initialize Sonoff relay.
        URL_POWER
        Raises:
            ConnectionError: Raised if a connection cannot be succesfully established with the relay.
            SonoffInitException: Raised if Dual R2 template cannot be succesfully set.
        
        Returns:
            bool -- True if all checks are passed. Cannot return False.
        """
        self.connected = self._check_connection()
        if not self.connected:
            raise ConnectionError("Cannot establish a connection to Sonoff relay.")
        requests.get(URL_TEMPLATE_SET.format(self.addr, MODULE_TEMPLATE_CODE))
        self.template_init = self._check_init_state()
        if not self.template_init:
            raise SonoffInitException("Cannot set template on Sonoff relay.")
        return True

    def set_state(self, states=[False, False]) -> Tuple[int, int]:
        """Set states of both relays at a time.
        
        Keyword Arguments:
            states {List[bool, bool]} -- Set desired state of both relays as a list of 
            two booleans (default: {[False, False]})
        
        Returns:
            Tuple[int, int] -- Returned status codes for both channels in order.
        """
        if len(states) != 2:
            raise ValueError("states list is not of length 2 (length {}).".format(len(states)))
        status_codes = []
        for state, chan in zip(states, CHANNEL_CODES):
            req = requests.get(URL_POWER.format(self.addr, chan, int(state)))
            status_codes.append(req.status_code)
        return tuple(status_codes)
