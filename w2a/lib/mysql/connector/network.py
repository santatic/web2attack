# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2012, Oracle and/or its affiliates. All rights reserved.

# MySQL Connector/Python is licensed under the terms of the GPLv2
# <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>, like most
# MySQL Connectors. There are special exceptions to the terms and
# conditions of the GPLv2 as it is applied to this software, see the
# FOSS License Exception
# <http://www.mysql.com/about/legal/licensing/foss-exception.html>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""Module implementing low-level socket communication with MySQL servers.
"""

from w2a.lib import socket
import struct
from collections import deque
import zlib
try:
    import ssl
except:
    # If import fails, we don't have SSL support.
    pass
    
from . import (constants, errors)

def _prepare_packets(buf, pktnr):
    """Prepare a packet for sending to the MySQL server"""
    pkts = []
    pllen = len(buf)
    maxpktlen = constants.MAX_PACKET_LENGTH
    while pllen > maxpktlen:
        pkts.append(b'\xff\xff\xff' + struct.pack('<B',pktnr) 
            + buf[:maxpktlen])
        buf = buf[maxpktlen:]
        pllen = len(buf)
        pktnr = pktnr + 1
    pkts.append(struct.pack('<I',pllen)[0:3]
                + struct.pack('<B',pktnr) + buf)
    return pkts

class BaseMySQLSocket(object):
    """Base class for MySQL socket communication

    This class should not be used directly but overloaded, changing the
    at least the open_connection()-method. Examples of subclasses are
      mysql.connector.network.MySQLTCPSocket
      mysql.connector.network.MySQLUnixSocket
    """
    def __init__(self):
        self.sock = None # holds the socket connection
        self._connection_timeout = None
        self._packet_number = -1
        self._packet_queue = deque()
        self.recvsize = 8192

    @property
    def next_packet_number(self):
        self._packet_number = self._packet_number + 1
        return self._packet_number
    
    def open_connection(self):
        """Open the socket"""
        raise NotImplementedError

    def get_address(self):
        """Get the location of the socket"""
        raise NotImplementedError
    
    def close_connection(self):
        """Close the socket"""
        try:
            self.sock.close()
            del self._packet_queue
        except (socket.error, AttributeError):
            pass

    def send_plain(self, buf,  packet_number=None):
        """Send packets to the MySQL server"""
        if packet_number is None:
            self.next_packet_number
        else:
            self._packet_number = packet_number
        packets = _prepare_packets(buf, self._packet_number)
        for packet in packets:
            try:
                self.sock.sendall(packet)
            except Exception as err:
                raise errors.OperationalError(str(err))
    send = send_plain

    def send_compressed(self, buf, packet_number=None):
        """Send compressed packets to the MySQL server"""
        if packet_number is None:
            self.next_packet_number
        else:
            self._packet_number = packet_number
        pktnr = self._packet_number
        pllen = len(buf)
        zpkts = []
        maxpktlen = constants.MAX_PACKET_LENGTH
        if pllen > maxpktlen:
            pkts = _prepare_packets(buf,pktnr)
            tmpbuf = b''.join(pkts)
            del pkts
            seqid = 0
            zbuf = zlib.compress(tmpbuf[:16384])
            zpkts.append(struct.pack('<I', len(zbuf))[0:3]
                         + struct.pack('<B', seqid)
                         + b'\x00\x40\x00' + zbuf)
            tmpbuf = tmpbuf[16384:]
            pllen = len(tmpbuf)
            seqid = seqid + 1
            while pllen > maxpktlen:
                zbuf = zlib.compress(tmpbuf[:maxpktlen])
                zpkts.append(struct.pack('<I', len(zbuf))[0:3]
                             + struct.pack('<B', seqid)
                             + b'\xff\xff\xff' + zbuf)
                tmpbuf = tmpbuf[maxpktlen:]
                pllen = len(tmpbuf)
                seqid = seqid + 1
            if tmpbuf:
                zbuf = zlib.compress(tmpbuf)
                zpkts.append(struct.pack('<I',len(zbuf))[0:3]
                                         + struct.pack('<B',seqid)
                                         + struct.pack('<I',pllen)[0:3]
                                         + zbuf)
            del tmpbuf
        else:
            pkt = (struct.pack('<I', pllen)[0:3] +
                struct.pack('<B', pktnr) + buf)
            pllen = len(pkt)
            if pllen > 50:
                zbuf = zlib.compress(pkt)
                zpkts.append(struct.pack('<I', len(zbuf))[0:3]
                             + struct.pack('<B', 0)
                             + struct.pack('<I', pllen)[0:3]
                             + zbuf)
            else:
                zpkts.append(struct.pack('<I', pllen)[0:3]
                             + struct.pack('<B', 0)
                             + struct.pack('<I', 0)[0:3]
                             + pkt)

        for zip_packet in zpkts:
            zpktlen = len(zip_packet)
            try:
                self.sock.sendall(zip_packet)
            except Exception as e:
                raise errors.OperationalError(str(e))
    
    def recv_plain(self):
        """Receive packets from the MySQL server"""
        try:
            header = self.sock.recv(4)
            if len(header) < 4:
                raise errors.InterfaceError(errno=2013)
            self._packet_number = header[3]
            payload_length = struct.unpack("<I", header[0:3] + b'\x00')[0]
            payload = b''
            while len(payload) < payload_length:
                chunk = self.sock.recv(payload_length - len(payload))
                if len(chunk) == 0:
                    raise errors.InterfaceError(errno=2013)
                payload = payload + chunk
            return header + payload
        except socket.timeout as e:
            raise errors.InterfaceError(errno=2013)
        except socket.error as err:
            raise errors.InterfaceError(
                errno=2055, values=(self.get_address(), err.errno))
    recv = recv_plain
    
    def _split_zipped_payload(self, packet_bunch):
        """Split compressed payload"""
        while packet_bunch:
            payload_length = struct.unpack("<I",
                                           packet_bunch[0:3] + b'\x00')[0]
            self._packet_queue.append(packet_bunch[0:payload_length + 4])
            packet_bunch = packet_bunch[payload_length + 4:]

    def recv_compressed(self):
        """Receive compressed packets from the MySQL server"""
        try:
            return self._packet_queue.popleft()
        except IndexError:
            pass
        
        packets = []
        try:
            header = self.sock.recv(7)
            while header:
                if len(header) < 7:
                    raise errors.InterfaceError(errno=2013)
                zip_payload_length = struct.unpack("<I",
                                                   header[0:3] + b'\x00')[0]
                payload_length = struct.unpack("<I", header[4:7] + b'\x00')[0]
                zip_payload = b''
                while len(zip_payload) < zip_payload_length:
                    chunk = self.sock.recv(zip_payload_length
                                           - len(zip_payload))
                    if len(chunk) == 0:
                        raise errors.InterfaceError(errno=2013)
                    zip_payload = zip_payload + chunk
                if payload_length == 0:
                    self._split_zipped_payload(zip_payload)
                    return self._packet_queue.popleft()
                packets.append(header + zip_payload)
                if payload_length != 16384:
                    break
                header = self.sock.recv(7)
        except socket.timeout as e:
            raise errors.InterfaceError(errno=2013)
        except socket.error as e:
            raise errors.InterfaceError(
                errno=2055, values=(self.get_address(), err.errno))
        
        tmp = []
        for packet in packets:
            payload_length = struct.unpack("<I", header[4:7] + b'\x00')[0]
            if payload_length == 0:
                tmp.append(packet[7:])
            else:
                tmp.append(zlib.decompress(packet[7:]))

        self._split_zipped_payload(b''.join(tmp))
        del tmp

        try:
            return self._packet_queue.popleft()
        except IndexError:
            pass
    
    def set_connection_timeout(self, timeout):
        """Set the connection timeout"""
        self._connection_timeout = timeout

    def switch_to_ssl(self, ca, cert, key):
        """Switch the socket to use SSL"""
        if not self.sock:
            raise errors.InterfaceError(errno=2048)

        try:
            self.sock = ssl.wrap_socket(
                self.sock, keyfile=key, certfile=cert, ca_certs=ca,
                cert_reqs=ssl.CERT_NONE, do_handshake_on_connect=False,
                ssl_version=ssl.PROTOCOL_TLSv1)
            self.sock.do_handshake()
        except NameError:
            raise errors.NotSupportedError(
                "Python installation has no SSL support")
        except ssl.SSLError as err:
            raise errors.InterfaceError("SSL error: {}".format(str(err)))
        except socket.error as err:
            raise errors.InterfaceError("Socket error: {}".format(str(err)))
        
class MySQLUnixSocket(BaseMySQLSocket):
    """MySQL socket class using UNIX sockets

    Opens a connection through the UNIX socket of the MySQL Server.
    """
    def __init__(self, unix_socket='/tmp/mysql.sock'):
        super().__init__()
        self.unix_socket = unix_socket
    
    def get_address(self):
        return self.unix_socket
        
    def open_connection(self):
        try:
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.sock.settimeout(self._connection_timeout)
            self.sock.connect(self.unix_socket)
        except socket.error as err:
            try:
                msg = err.errno
                if msg is None:
                    msg = str(err)
            except AttributeError:
                msg = str(err)
            raise errors.InterfaceError(
                errno=2002, values=(self.get_address(), msg))
        except Exception as err:
            raise errors.InterfaceError(str(err))
        
class MySQLTCPSocket(BaseMySQLSocket):
    """MySQL socket class using TCP/IP

    Opens a TCP/IP connection to the MySQL Server.
    """
    def __init__(self, host='127.0.0.1', port=3306):
        super().__init__()
        self.server_host = host
        self.server_port = port
    
    def get_address(self):
        return "{}:{}".format(self.server_host, self.server_port)
        
    def open_connection(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self._connection_timeout)
            self.sock.connect((self.server_host, self.server_port))
        except socket.error as err:
            try:
                msg = err.errno
                if msg is None:
                    msg = str(err)
            except AttributeError:
                msg = str(err)
            raise errors.InterfaceError(
                errno=2002, values=(self.get_address(), msg))
        except Exception as err:
            raise errors.OperationalError(str(err))
