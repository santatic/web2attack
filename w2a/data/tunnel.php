<?php
/*
This version is not compatible with previous versions of the client
*/

define('vpsp_version', '2.5.0');

/*
Set your password here
Leave the variable empty to use no password
! Remove { and }
*/
define('vpsp_pwd', 'P@55w0rD_FuCk3r');

/*
Set encryption key here
Don't leave the variable empty.
In order to enable/disable encryption use 'Enable traffic encryption' setting in the GUI client.
! Remove { and }
*/
define('vpsp_enc_key', 'ldasufyq8723rq9721*&(^q234asd');

/*
Displaying of any messages is suppressed.
In order to keep downloaded file integrity, no extraneous data must be ouptut by this script
*/
error_reporting(~E_ALL);

@set_time_limit(0);
ob_implicit_flush(1);
ignore_user_abort(0);

header('Content-type: application/octet-stream');
header('Content-Transfer-Encoding: binary');
header('X-VPSP-VERSION: ' . vpsp_version);

$input = fopen('php://input', 'r');
define('vpsp_enc',  ord(fread($input, 1)) != 0);
$ok;

if (vpsp_enc) {
	if (isset($GLOBALS['vpsp_pe']) == false) {
		$GLOBALS['vpsp_ks'] = VC_GenerateKeyHash(vpsp_enc_key);
		$GLOBALS['vpsp_pe'] = VC_Init(vpsp_enc_key, $GLOBALS['vpsp_ks']);
	}
	$GLOBALS['vpsp_pd'] = array_flip($GLOBALS['vpsp_pe']);
	
	$ok = VC_Decrypt(fread($input, 2));
	if ($ok != 'OK') {
		header('X-VPSP-ERROR: bad_enc_key');
		header('X-VPSP-HOST: ' . (isset($_SERVER['HTTPS']) ? 'https://' : 'http://') . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI']);
		exit;
	}
	$rBuffLen = ord(VC_Decrypt(fread($input, 1))) * 256 * 256 * 256 + ord(VC_Decrypt(fread($input, 1))) * 256 * 256 + ord(VC_Decrypt(fread($input, 1))) * 256 + ord(VC_Decrypt(fread($input, 1)));
	$sBuffLen = ord(VC_Decrypt(fread($input, 1))) * 256 * 256 * 256 + ord(VC_Decrypt(fread($input, 1))) * 256 * 256 + ord(VC_Decrypt(fread($input, 1))) * 256 + ord(VC_Decrypt(fread($input, 1)));
	$reqPwdLen = ord(VC_Decrypt(fread($input, 1)));
	$reqPwd = ($reqPwdLen > 0) ? VC_Decrypt(fread($input, $reqPwdLen)) : '';
	$https = ord(VC_Decrypt(fread($input, 1)));
	$host = VC_Decrypt(fread($input, ord(VC_Decrypt(fread($input, 1)))));
	$port = ord(VC_Decrypt(fread($input, 1))) * 256 + ord(VC_Decrypt(fread($input, 1)));
} else {
	$ok = fread($input, 2);
	if ($ok != 'OK') {
		header('X-VPSP-ERROR: bad_request');
		header('X-VPSP-HOST: ' . (isset($_SERVER['HTTPS']) ? 'https://' : 'http://') . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI']);
		exit;
	}
	$rBuffLen = ord(fread($input, 1)) * 256 * 256 * 256 + ord(fread($input, 1)) * 256 * 256 + ord(fread($input, 1)) * 256 + ord(fread($input, 1));
	$sBuffLen = ord(fread($input, 1)) * 256 * 256 * 256 + ord(fread($input, 1)) * 256 * 256 + ord(fread($input, 1)) * 256 + ord(fread($input, 1));
	$reqPwdLen = ord(fread($input, 1));
	$reqPwd = ($reqPwdLen > 0) ? fread($input, $reqPwdLen) : '';
	$https = ord(fread($input, 1));
	$host = fread($input, ord(fread($input, 1)));
	$port = ord(fread($input, 1)) * 256 + ord(fread($input, 1));
}

if ($reqPwd !== vpsp_pwd) {
	$resp = "HTTP/1.0 401 Unauthorized\r\nX-VPSP-VERSION: " . vpsp_version . "\r\nX-VPSP-ERROR: bad_password\r\nX-VPSP-HOST: " . (isset($_SERVER['HTTPS']) ? 'https://' : 'http://') . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI']  . "\r\nConnection: close\r\n\r\n";
	if (vpsp_enc) {
		echo VC_Encrypt($resp);
	} else {
		echo $resp;
	}
	exit;
}

if ($https == 1) {
	$host = 'ssl://' . $host;
}

$fsok = fsockopen($host, $port, $errno, $errstr, 20);
if ($fsok == false) {
	$resp = "HTTP/1.0 503 Service Unavailable\r\nX-VPSP-VERSION: " . vpsp_version . "\r\nX-VPSP-ERROR: host_down\r\nX-VPSP-ERROR-TEXT: " . base64_encode($errstr) ."\r\nX-VPSP-HOST: " . (isset($_SERVER['HTTPS']) ? 'https://' : 'http://') . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'] . "\r\nX-VPSP-TARGET: " . str_replace('ssl://', '', $host) . "\r\nConnection: close\r\n\r\n";
	if (vpsp_enc) {
		echo VC_Encrypt($resp);
	} else {
		echo $resp;
	}
	exit;
}

while ($wbuffer = fread($input, $rBuffLen)) {
	if (vpsp_enc) {
		fwrite($fsok, VC_Decrypt($wbuffer));
	} else {
		fwrite($fsok, $wbuffer);
	}
}

fflush($fsok);

while ($rbuffer = fread($fsok, $sBuffLen)) {
	if (vpsp_enc) {
		echo VC_Encrypt($rbuffer);
	} else {
		echo $rbuffer;
	}
}
fflush($fsok);
fclose($fsok);

function MD5Hash($str) {
	$m = md5($str);
	$s = '';
 	foreach(explode("\n", trim(chunk_split($m, 2))) as $h) {
 		$s .= chr(hexdec($h));
 	}
	return $s;
}

function VC_Init($key, $ks) {
	$s = range(0, 255);
	if (strlen($key) == 0) {
		return $s;
	}
	$km = MD5Hash($key);
	$kx = '';
	for ($i = 0; $i < 16; $i++) {
		$kx .= MD5Hash($km . $km[$i] .  chr($ks));
	}
	$r = ($ks % 0x0F) + 1;
	$j = $ks;
	for ($n = 0; $n < $r; $n++) {
		for ($i = 0; $i < 256; $i++) {
			$j = (($j + $s[$i] + $n + ord($kx[$i])) ^ $ks) % 256;
			$t = $s[$i];
			$s[$i] = $s[$j];
			$s[$j] = $t;
		}
	}
	for ($i = 0; $i < 256; $i++) {
		$s[$i] = $s[$i] ^ $ks;
	}
	return $s;
}

function VC_GenerateKeyHash($key) {
	$m = MD5Hash($key);
	$kt = 0;
	for ($i = 0; $i < 16; $i++) {
		$kt += ord($m[$i]);
	}
	return $kt % 256;
}

function VC_Encrypt($str) {
	$pe = $GLOBALS['vpsp_pe'];
	$out = '';
	$len = strlen($str);
	for ($y = 0; $y < $len; $y++) {
		$out .= chr($pe[ord($str[$y])]);
	}
	return $out;
}

function VC_Decrypt($str) {
	$pd = $GLOBALS['vpsp_pd'];
	$out = '';
	$len = strlen($str);
	for ($y = 0; $y < $len; $y++) {
		$out .= chr($pd[ord($str[$y])]);
	}
	return $out;
}