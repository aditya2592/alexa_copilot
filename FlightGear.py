from telnetlib import Telnet
import sys
import socket
import re
from string import split, join
import time

__all__ = ["FlightGear"]

CRLF = '\r\n'

class EngineAction:
    def __init__(self,fg,ctype,cvalue):
        self.fg = fg
        self.ctype = ctype
        self.cvalue = cvalue

    def prime_engine(self, count):
        self.fg.set_bool('/controls/engines/engine/use-primer', 0)
        self.fg.set_double('/controls/engines/engine/primer', 0)

        for num in range(0, count) :    
            engine_path = '/controls/engines/engine/primer-lever'
            self.fg.set_bool(engine_path,1)
            self.fg.set_bool(engine_path,0)

    def auto_start_sequence (self):
        self.fg.set_bool('/controls/electric/external-power', 0)
        self.fg.set_double('/controls/engines/current-engine/throttle', 0)
        self.fg.set_double('/controls/engines/current-engine/mixture', 0)

        self.fg.set_bool('/controls/switches/starter', 1)
        self.prime_engine(5)

        self.fg.set_double('/controls/engines/current-engine/mixture', 1)
        self.fg.set_double('/controls/engines/current-engine/throttle', 0.2)

        self.fg.set_int('/controls/switches/magnetos', 3)
        self.fg.set_bool('/controls/electric/external-power', 1)


    def execute_action(self):
        if self.ctype == "throttle":
            self.fg.set_double('/controls/engines/current-engine/throttle', float(self.cvalue)/100);
        elif self.ctype == "mixture":
            self.g.set_double('/controls/engines/current-engine/mixture', float(self.cvalue)/100);
        elif self.ctype == "prime":
            self.prime_engine(int(self.cvalue))
        elif self.ctype == "autostart" and self.cvalue == "true":
            self.auto_start_sequence()
        else :
            print("Uncoded instruction")

class FGTelnet(Telnet):
    def __init__(self,host,port):
        Telnet.__init__(self,host,port)
        self.prompt = []
        self.prompt.append( re.compile('/[^>]*> ') )
        self.timeout = 5
        Telnet.set_debuglevel(self,2)

    def help(self):
        return

    def ls(self,dir=None):
        """
        Returns a list of properties.
        """
        if dir == None:
            self._putcmd('ls')
        else:
            self._putcmd('ls %s' % dir )
        return self._getresp()

    def dump(self):
        """Dump current state as XML."""
        self._putcmd('dump')
        return self._getresp()

    def cd(self, dir):
        """Change directory."""
        self._putcmd('cd ' + dir)
        self._getresp()
        return

    def pwd(self):
        """Display current path."""
        self._putcmd('pwd')
        return self._getresp()

    def get(self,var):
        """Retrieve the value of a parameter."""
        self._putcmd('get %s' % var )
        return self._getresp()

    def set(self,var,value):
        """Set variable to a new value"""
        self._putcmd('set %s %s' % (var,value))
        self._getresp() # Discard response

    def setb(self,var,value):
        """Set variable to a new value"""
        self._putcmd('setb %s %s' % (var,value))
        self._getresp() # Discard response

    def setd(self,var,value):
        """Set variable to a new value"""
        self._putcmd('setd %s %s' % (var,value))
        self._getresp() # Discard response

    def seti(self,var,value):
        """Set variable to a new value"""
        self._putcmd('seti %s %s' % (var,value))
        self._getresp() # Discard response

    def quit(self):
        """Terminate connection"""
        self._putcmd('quit')
        self.close()
        return

    # Internal: send one command to FlightGear
    def _putcmd(self,cmd):
        cmd = cmd + CRLF;
        Telnet.write(self, cmd)
        return

    # Internal: get a response from FlightGear
    def _getresp(self):
        (i,match,resp) = Telnet.expect(self, self.prompt, self.timeout)
        # Remove the terminating prompt.
        # Everything preceding it is the response.
        return split(resp, '\n')[:-1]

class FlightGear:
    """FlightGear interface class.

    An instance of this class represents a connection to a FlightGear telnet
    server.

    Properties are accessed using a dictionary style interface:
    For example:

    # Connect to flightgear telnet server.
    fg = FlightGear('myhost', 5500)
    # parking brake on
    fg['/controls/gear/brake-parking'] = 1
    # Get current heading
    heading = fg['/orientation/heading-deg']

    Other non-property related methods
    """

    def __init__( self, host = 'localhost', port = 5500 ):
        try:
            self.telnet = FGTelnet(host,port)
        except socket.error, msg:
            self.telnet = None
            raise socket.error, msg

    def __del__(self):
        # Ensure telnet connection is closed cleanly.
        self.quit();

    def __getitem__(self,key):
        """Get a FlightGear property value.
        Where possible the value is converted to the equivalent Python type.
        """
        s = self.telnet.get(key)[0]
        match = re.compile( '[^=]*=\s*\'([^\']*)\'\s*([^\r]*)\r').match( s )
        if not match:
            return None
        value,type = match.groups()
        #value = match.group(1)
        #type = match.group(2)
        if value == '':
            return None

        if type == '(double)':
            return float(value)
        elif type == '(int)':
            return int(value)
        elif type == '(bool)':
            if value == 'true':
                return 1
            else:
                return 0
        else:
            return value

    def __setitem__(self, key, value):
        """Set a FlightGear property value."""
        self.telnet.set( key, value )

    def set_bool (self, path, value):
        self.telnet.setb(path, value)

    def set_double (self, path, value):
        self.telnet.setd(path, value)

    def set_int (self, path, value):
        self.telnet.seti(path, value)

    def quit(self):
        """Close the telnet connection to FlightGear."""
        if self.telnet:
            self.telnet.quit()
            self.telnet = None



    def set_engine_action(self,ctype,cvalue):
        self.engine = EngineAction(self,ctype,cvalue);

    def view_next(self):
        #move to next view
        self.telnet.set( "/command/view/next", "true")

    def view_prev(self):
        #move to next view
        self.telnet.set( "/command/view/prev", "true")

