"""
 * \author     Hugo Silva
 * \version    1.0
 * \date       July 2014
 * 
 * \section LICENSE
 
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.
 
 You should have received a copy of the GNU Lesser General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
"""

import json
import traceback

import numpy as np
import peakutils

import pylab
from twisted.internet import protocol, reactor

from bitalino import *
from txws import WebSocketFactory

previous_ppg=np.zeros(10000)
global threshold



def tostring(data):

    """
    :param data: object to be converted into a JSON-compatible `str`
    :type data: any
    :return: JSON-compatible `str` version of `data`

    Converts `data` from its native data type to a JSON-compatible `str`.
    """
    left_alpha = 0;
    right_alpha = 0;
    aux_data = np.zeros([2, 1000])
    dtype = type(data).__name__
    if dtype == 'ndarray':
        if pylab.shape(data) != ():
            data = data.transpose()

            # DIVIDO POR MIL PARA ESCALAR AO NUMERO DE PONTOS NA AMOSTRA - IS CORRECT? CONFIRMAR!!!
            aux_data[0, :501] = np.square(np.absolute(np.fft.rfft(data[0, :])))/1000
            aux_data[1, :501] = np.square(np.absolute(np.fft.rfft(data[1, :])))/1000

            # ppg_no_baseline=peakutils.baseline(data[2])             #remove baseline from ppg signal
            indexes = peakutils.indexes(data[2], thres=max(data[2])/1023, min_dist=500) #find its peak
            print "max=", max(data[2]), " indexes = ", indexes
            for elmt in indexes:                                       #set up peak value in original ppg as 1023
                data[2][elmt]=1023

            csv_file = file('readings/potato.csv', 'a')
            np.savetxt(csv_file, data, delimiter=",", fmt="%.3e")
            csv_file.close()
            data = data.tolist()

            # data=list(data)
            aux_data=aux_data.tolist()
            data=data+aux_data

        else:
            data = '"' + data.tostring() + '"'
    elif dtype == 'dict' or dtype == 'tuple':
        try:
            data = json.dumps(data)
        except:
            pass
    elif dtype == 'NoneType':
        data = ''
    elif dtype == 'str' or dtype == 'unicode':
        data = json.dumps(data)

    return str(data)


class VS(protocol.Protocol):
    def connectionMade(self):
        """
		Callback executed when the client successfully connects to the server.
		"""
        print "CONNECTED"

        # Notify the client that a connection has been established
        self.transport.write('server.connected()')

    def dataReceived(self, req):
        """
		:param req: Python instruction sent by the client
		:type req: str

		Evaluates the instruction `req` sent by the client and responds with an identical instruction, in which the return value of that instruction is the input argument.
		"""
        try:
            # Show the request on the terminal window
            print '> ' + req

            # Evaluate the request and retrieve the result
            res = eval(req)

            # If the request is to shutdown the server no further action is needed
            if (req.find('shutdown') >= 0):
                return

            # Place the result as an argument to the instruction received as the request
            li = req.find('(')
            li = li if li >= 0 else None

            res = req[:li] + '(' + tostring(res) + ');'

            # Show the response on the terminal window
            print '< ' + res

        # Should an exceptio occur, the exception is propagated to the client
        except Exception as e:
            print traceback.format_exc()
            res = 'sys.exception("' + str(e) + '")'
            print 'recieved message is buggy: ' + req
        # Send the response to the client
        self.transport.write(res)

    def connectionLost(self, reason):
        """
		Callback executed when the connection to the client is lost.
		"""
        server.shutdown()
        return


class server(object):
    @staticmethod
    def BITalino(macAddress):
        """
		:param macAddress: string with a BITalino MAC address or COM port
		:type macAddress: str
		:return: status of the connection

		Proxy function that the client can use to initialize the connection to a BITalino device.
		"""
        global device
        try:
            device = BITalino(macAddress)
            res = True
        except Exception as e:
            print traceback.format_exc()
            res = 'sys.exception("' + str(e) + '")'

        return res

    @staticmethod
    def shutdown():
        """
		Utility function that the client can use to shutdown the server.
		"""
        connector.stopListening()
        try:
            reactor.stop()
        except:
            pass

        print "DISCONNECTED"


class VSFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return VS()


if __name__ == '__main__':
    try:
        ip_addr, port = "127.0.0.1", 9005

        device = None

        print "LISTENING AT %s:%s" % (ip_addr, port)

        connector = reactor.listenTCP(port, WebSocketFactory(VSFactory()))
        reactor.run()

    except Exception as e:
        print traceback.format_exc()
