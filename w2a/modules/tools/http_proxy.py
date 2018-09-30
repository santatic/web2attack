# modules/tools/http_proxy.py
#
# Copyright 2012 Kid :">
# to run it,requite tunnel.php

from w2a.core.templates import Templates
from w2a.lib.thread import Thread
# from w2a.lib.net.http import HTTP
from w2a.lib import socket
from w2a.config import CONFIG

from random import choice
from urllib import parse
from hashlib import md5
from binascii import unhexlify
from base64 import b64encode

class Module(Templates):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		############################
		self.version		= 1
		self.author			= [ 'Kid' ]
		self.description 	= 'Http Proxy with php host'
		self.detailed_description	= 'This module retreives create virtual http proxy with php host'
		############################
		self.options.add_boolean('ENCRYPT', 'Encrypt data ?', default = True)
		
		############################
		self.advanced_options.add_integer('SERVERPORT', 'Port of Proxy Server', default = 9000)
		self.advanced_options.add_integer('TIMEOUT', 'Time out request', default = CONFIG.TIME_OUT)

	def run(self, frmwk, args):
		self.frmwk 			= frmwk
		self.encrypt 		= self.options['ENCRYPT']
		self.r_buffer 		= 4096
		self.s_buffer 		= 4096
		self.https 			= 0

		self.server_host 	= ''
		self.server_port 	= self.advanced_options['SERVERPORT']
		self.connect_timout	= self.advanced_options['TIMEOUT']
		self.tunnel_list 	= [
								['http://127.0.0.1/pen/gate.php', b'P@55W0rK_FuCkeR__', b'K3y_3nCrYpT_$_$'],
								['http://127.0.0.1/pen/gate.php', b'P@55W0rK_FuCkeR__', b'K3y_3nCrYpT_$_$']
							]
		self.tunnel_server()

	def tunnel_server(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		try:
			sock.bind((self.server_host, self.server_port))
			sock.listen(5)
			self.frmwk.print_status("Server listen on port : " + str(self.server_port))
			while True:
				conn, addr	= sock.accept()
				Thread(target = self.worker, args =(conn, addr,)).start()
		finally:
			sock.close()

	def worker(self, c_conn, c_addr):
		self.frmwk.print_status("Accept new connect from  " + str(c_addr))
		################### CONNET TUNNEL #####################
		### choin and connect to tunnel
		c_tunnel	= self.choin_tunnel()	# chon 1 tunnel
		t_conn		= None
		# t_conn		= HTTP(c_tunnel[0], timeout = self.connect_timout)
		
		### check tunnel is open
		if not t_conn:
			self.frmwk.print_error('Can\'t connect to tunnel')
			return None
		### encrypt/decrypt init
		# tunnel_ks 	= self.vc_generatekeyhash(c_tunnel[2])
		# tunnel_pe 	= self.vc_init(c_tunnel[2],tunnel_ks)
		# tunnel_pd 	= dict((tunnel_pe[i],i) for i in range(0,len(tunnel_pe)))
		if self.encrypt:
			crypt 	= crypton(c_tunnel[2])
		else:
			crypt 	= None
		################### START READ DATA CLIENT #####################
		### get status and header from sockert
		c_status, c_headers, c_content_len	= self.socket_receiver(c_conn)

		### set url, host, port, method
		s_https	= 0
		host 	= c_status[1]
		if host.startswith(b'http'):
			parser		= parse.urlparse(host)
			s_host		= parser.hostname
			s_port 		= parser.port
			s_path 		= b'/' + host.split(b'/', 3)[3]
			if not s_port:
				if parser.scheme == 'https':
					s_port	= 443
				else:	
					s_port	= 80
			if parser.scheme == 'https':
				s_https	= 1
		else:
			self.frmwk.print_error("Unknown client request connect !")
			return None

		### set status
		c_send_header 	= [b' '.join([c_status[0], s_path, c_status[2]])]

		### set header for send
		c_headers.update({b'Connection': b'close'})	# fix host delay
		for k,v in c_headers.items():
			if k.startswith(b'Proxy'):
				continue
			c_send_header.append(k+ b': ' +v)

		## add headers to send all data
		c_send_header 		= b"\r\n".join(c_send_header) + b"\r\n\r\n"

		### set init param of tunnel
		c_send_init 		= self.send_init(s_host, s_port, self.r_buffer, self.s_buffer, s_https, c_tunnel, crypt)

		### init and send tunnel parameter
		t_conn.init(c_tunnel[0], 'POST', {'Content-Length': len(c_send_init)+ len(c_send_header) + c_content_len})
		t_conn.send(c_send_init)

		del c_send_init 	# clear memory

		### get content from client and send to server with r_buffer
		if c_content_len > 0:
			c_sent 	= 0
			####### send header with content for full r_buffer encrypt
			if self.encrypt:
				mod_len 	= len(c_send_header) % len(c_tunnel[2])
				data 		= c_conn.recv(mod_len)
				data 		= c_send_header + data
				data_len 	= len(data)
				for i in range(0, data_len, self.r_buffer):
					t_conn.send(crypt.vc_encrypt(data[i:min(i + self.r_buffer, data_len - i)]))
				c_sent 		= mod_len	
			else:
				t_conn.send(c_send_header)

			###### send content
			if c_sent < c_content_len:
				while True:
					data	= c_conn.recv(min(self.r_buffer, c_content_len - c_sent))
					if self.encrypt:
						t_conn.send(crypt.vc_encrypt(data))
					else:
						t_conn.send(data)

					c_sent 	+= len(data)
					if not data or c_sent == content_lent:
						break
		else:
			if self.encrypt:
				t_conn.send(crypt.vc_encrypt(c_send_header))
			else:
				t_conn.send(c_send_header)
		del c_send_header 		# clear memory
		############## END SEND ################
		############# START RECV ###############
		try:
			for res_chunk in t_conn.recv(self.s_buffer):
				if self.encrypt:
					c_conn.send(crypt.vc_decrypt(res_chunk))
				else:
					c_conn.send(res_chunk)
		except Exception as e:
			self.frmwk.print_error(str(e))
		finally:
			t_conn.request.close()
			c_conn.close()
			
		self.frmwk.print_status("Closed connect from  " + str(c_addr))

	def socket_receiver(self, conn):
		## read header
		fs 				= conn.makefile('rb')
		res_status 		= fs.readline()[0:-2].split(b" ",2)
		res_header 		= dict()
		res_content_len	= 0
		while True:
			h	= fs.readline()
			if h == b"\r\n":
				break
			if h:
				if h.startswith(b'Content-Length'):
					res_content_len 	= int(h.split(b': ', 1)[1])
				key, val 	= tuple(h.split(b": ", 1))
				res_header.update({	key : val[0:-2]})

		return res_status, res_header, res_content_len

	##############################
	def send_init(self, host, port, r_buffer, s_buffer, https, c_tunnel, crypt):
		res	= bytes()
		if self.encrypt:
			res 	+= bytes([1])	# 1b init char is encrypt
			res 	+= crypt.vc_encrypt(b'OK')	#2b init ok connect
			# len of read buffer
			res 	+= crypt.vc_encrypt(bytes([int(r_buffer / (256*256*256))]))\
						+ crypt.vc_encrypt(bytes([int(r_buffer / (256*256))]))\
						+ crypt.vc_encrypt(bytes([int(r_buffer / 256)]))\
						+ crypt.vc_encrypt(bytes([r_buffer % 256]))

			# len of s_buffer
			res 	+= crypt.vc_encrypt(bytes([int(s_buffer / (256*256*256))]))\
						+ crypt.vc_encrypt(bytes([int(s_buffer / (256*256))]))\
						+ crypt.vc_encrypt(bytes([int(s_buffer / 256)]))\
						+ crypt.vc_encrypt(bytes([s_buffer % 256]))

			res 	+= crypt.vc_encrypt(bytes([len(c_tunnel[1])]))	# password len
			res 	+= crypt.vc_encrypt(c_tunnel[1]) 	#password
			res 	+= crypt.vc_encrypt(bytes([https]))	# is https
			res 	+= crypt.vc_encrypt(bytes([len(host)]))	# host len
			res 	+= crypt.vc_encrypt(host)	#host
			res 	+= crypt.vc_encrypt(bytes([int(port / 256)])) + crypt.vc_encrypt(bytes([port % 256]))	# port
		else:

			res 	+= bytes([0])	# 1b init char is encrypt
			res 	== b'OK' 		# 2b init ok connect
			res 	+= bytes([int(r_buffer / (256*256*256)), int(r_buffer / (256*256)), int(r_buffer / 256), r_buffer % 256]) # reader buffer len
			res 	+= bytes([int(s_buffer / (256*256*256)), int(s_buffer / (256*256)), int(s_buffer / 256), s_buffer % 256]) # reader buffer len
			res 	+= bytes([len(c_tunnel[1])])	# password len
			res 	+= c_tunnel[1] 	#password
			res 	+= bytes([https])	# is https
			res 	+= bytes([len(host)])	# host len
			res 	+= host 	#host
			res 	+= bytes([int(port / 256), int(port % 256)]) #port
		return res

	def choin_tunnel(self, i = False):
		if i:
			return self.tunnel_list[i]
		else:
			return choice(self.tunnel_list)

############################### CRYPTION #################################
class crypton:
	def __init__(self, key):
		self._key 	= key
		## init
		self._ks 	= self.vc_generatekeyhash(self._key)
		self._pe 	= self.vc_init(self._key,self._ks)
		self._pd 	= dict((self._pe[i], i) for i in range(0, len(self._pe)))

	def md5hash(self, st):
		# function MD5Hash($str) {
		# 	$m = md5($str);
		# 	$s = '';
		#  	foreach(explode("\n", trim(chunk_split($m, 2))) as $h) {
		#  		$s .= chr(hexdec($h));
		#  	}
		# 	return $s;
		# }
		m 	= md5(st).hexdigest()
		return unhexlify(m.encode())

	def vc_init(self, key, ks):
		# function VC_Init($key, $ks) {
		# 	$s = range(0, 255);
		# 	if (strlen($key) == 0) {
		# 		return $s;
		# 	}
		# 	$km = MD5Hash($key);
		# 	$kx = '';
		# 	for ($i = 0; $i < 16; $i++) {
		# 		$kx .= MD5Hash($km . $km[$i] .  chr($ks));
		# 	}
		# 	$r = ($ks % 0x0F) + 1;
		# 	$j = $ks;
		# 	for ($n = 0; $n < $r; $n++) {
		# 		for ($i = 0; $i < 256; $i++) {
		# 			$j = (($j + $s[$i] + $n + ord($kx[$i])) ^ $ks) % 256;
		# 			$t = $s[$i];
		# 			$s[$i] = $s[$j];
		# 			$s[$j] = $t;
		# 		}
		# 	}
		# 	for ($i = 0; $i < 256; $i++) {
		# 		$s[$i] = $s[$i] ^ $ks;
		# 	}
		# 	return $s;
		# }

		_s = list(range(0, 256))
		
		if len(key) == 0:
			return _s
		
		_km 	= self.md5hash(key)
		_kx 	= b''
		for i in range(0,16):
			_kx 	+= self.md5hash(_km + bytes([_km[i],ks]))

		_r 	= (ks % 0x0F) + 1
		_j 	= ks
		
		for n in range(0, _r):
			for i in range(0, 256):
				_j 		= ((_j + _s[i] + n + _kx[i]) ^ ks) % 256
				_t 		= _s[i]
				_s[i]	= _s[_j]
				_s[_j] 	= _t

		for i in range(0, 256):
			_s[i] 	= _s[i] ^ ks
		return _s

	def vc_generatekeyhash(self, key):
		# function VC_GenerateKeyHash($key) {
		# 	$m = MD5Hash($key);
		# 	$kt = 0;
		# 	for ($i = 0; $i < 16; $i++) {
		# 		$kt += ord($m[$i]);
		# 	}
		# 	return $kt % 256;
		# }
		_m 		= self.md5hash(key)
		_kt 	= 0
		for i in range(0,16):
			_kt 	+= _m[i]
		return _kt % 256


	def vc_encrypt(self, t):
		# function VC_Encrypt($str) {
		# 	$pe = $GLOBALS['vpsp_pe'];
		# 	$out = '';
		# 	$len = strlen($str);
		# 	for ($y = 0; $y < $len; $y++) {
		# 		$out .= chr($pe[ord($str[$y])]);
		# 	}
		# 	return $out;
		# }
		_pe 	= self._pe
		_out 	= b''
		_len 	= len(t)
		for y in range(0,_len):
			_out 	+= bytes([_pe[t[y]]])
		return _out

	def vc_decrypt(self, t):
		# function VC_Decrypt($str) {
		# 	$pd = $GLOBALS['vpsp_pd'];
		# 	$out = '';
		# 	$len = strlen($str);
		# 	for ($y = 0; $y < $len; $y++) {
		# 		$out .= chr($pd[ord($str[$y])]);
		# 	}
		# 	return $out;
		# }
		_pd 	= self._pd
		_out 	= b''
		_len 	= len(t)
		for y in range(0,_len):
			_out 	+= bytes([_pd[t[y]]])
		return _out