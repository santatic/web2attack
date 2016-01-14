from w2a.config import CONFIG

from os import linesep
from sys import stdout

def output(message):
	# stdout.write(message + '\n')
	print(message)

def print_error(message, color = True):
	if color:
		output('\033[' + CONFIG.COLOR_ERROR + '[-] \033[1;m' + (linesep + '\033[' + CONFIG.COLOR_ERROR + '[-] \033[1;m').join(message.split(linesep)))
	else:
		output('[-] ' + (linesep + '[-] ').join(message.split(linesep)))

def print_success(message, color = True):
	if color:
		output('\033[' + CONFIG.COLOR_SUCCESS + '[+] \033[1;m' + (linesep + '\033[' + CONFIG.COLOR_SUCCESS + '[+] \033[1;m').join(message.split(linesep)))
	else:
		output('[+] ' + (linesep + '[+] ').join(message.split(linesep)))

def print_line(message = ''):
	output(message)

def print_status(message, color = True):
	if color:
		output('\033[' + CONFIG.COLOR_STATUS + '[*] \033[1;m' + (linesep + '\033[' + CONFIG.COLOR_STATUS + '[*] \033[1;m').join(message.split(linesep)))
	else:
		output('[*] ' + (linesep + '[*] ').join(message.split(linesep)))

def print_debug(message, color = True):
	if CONFIG.DEBUG_FLAG:
		if color:
			output('\033[' + CONFIG.COLOR_ERROR + '[*] \033[1;m' + (linesep + '\033[' + CONFIG.COLOR_ERROR + '[*] \033[1;m').join(message.split(linesep)))
		else:
			output('[*] ' + (linesep + '[*] ').join(message.split(linesep)))

def print_process(percent, color = True):
	if color:
		stdout.write('\r\033[' + CONFIG.COLOR_STATUS + '[\033[1;m\033[' + CONFIG.COLOR_SUCCESS + '=' * int(percent/2) + '>\033[1;m'+' '*int((100 - percent)/2 + 0.5)+'\033[' + CONFIG.COLOR_STATUS + '] [\033[1;m\033[' + CONFIG.COLOR_ERROR + str(percent) +'%\033[1;m\033[' + CONFIG.COLOR_STATUS + ']\033[1;m')
	else:
		stdout.write("\r[" + '=' * int(percent/2) + '>'+' '*(50 - percent)+'] ['+ str(percent) +'%%]')
	stdout.flush()

def color_status(str):
	return '\033[' + CONFIG.COLOR_STATUS + str +'\033[1;m'

def color_success(str):
	return '\033[0;32m'+str +'\033[0;m'