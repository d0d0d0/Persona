"""
This file contains functions that are related to SSL connection.

	-SSL certificate generation
"""

from os.path import exists
from OpenSSL import crypto
from shutil import copyfile
import uuid


def ssl_certificate_generator(crt='certificate/client.crt', pem='certificate/cclient.pem'):
	"""
	SSL Certificate and PEM file generation
	"""
	try:
		if not exists(pem) or not exists(crt) or not exists(crt + '.key'):
			public_key = crypto.PKey()
			public_key.generate_key(crypto.TYPE_RSA, 1024)

			cert = crypto.X509()

			cert.get_subject().C = raw_input("Country: ")
			cert.get_subject().ST = raw_input("State: ")
			cert.get_subject().L = raw_input("City: ")
			cert.get_subject().O = raw_input("Organization: ")
			cert.get_subject().OU = raw_input("Organizational Unit: ")
			cert.get_subject().CN = crt

			cert.set_serial_number(int(str(uuid.uuid4().int)[:5]))
			cert.gmtime_adj_notBefore(0)
			cert.gmtime_adj_notAfter(315360000)

			cert.set_issuer(cert.get_subject())
			cert.set_pubkey(public_key)

			cert.sign(public_key, 'sha1')
			open(pem, "wt").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
			copyfile(pem, pem.split('.')[0] + '.crt')
			open(crt + '.key', "wt").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, public_key))

			with open(pem, 'a') as outfile:
				with open(crt + '.key') as infile:
					for line in infile:
						outfile.write(line)
	except Exception as e:
		print e