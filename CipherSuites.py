# This file contains the main TLS cipher suits whose energy use will be analyzed
import ssl

from enum import Enum

######
# The cipher suites we are supporting and their SSL library string representation
######
class CipherSuites(Enum):
    DHERSA_AES256 = "DHE-RSA-AES256-GCM-SHA384"
    DHERSA_CHACHA20 = "DHE-RSA-CHACHA20-POLY1305"
    ECDHERSA_AES256 = "ECDHE-RSA-AES256-GCM-SHA384"
    ECDHERSA_CHACHA20 = "ECDHE-RSA-CHACHA20-POLY1305"

######
# Create a TLS 1.2 context for the given cipher suite
# Add the apporiote certificate and Diffie-Helman files if neccessary
######
def getSSLContext_server(ciphers):
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.set_ciphers(ciphers.value)

    if ciphers == CipherSuites.DHERSA_AES256 or ciphers == CipherSuites.DHERSA_CHACHA20:
        ssl_context.load_cert_chain(certfile="cert.pem", keyfile="cert.pem") # load serve certificate and private key
        ssl_context.load_dh_params("dhparams.pem") # load the parameters for Diffie-Hellman

    if ciphers == CipherSuites.ECDHERSA_AES256 or ciphers == CipherSuites.ECDHERSA_CHACHA20:
        ssl_context.load_cert_chain(certfile="cert.pem", keyfile="cert.pem") # load serve certificate and private key
        #ssl_context.set_ecdh_curve("prime256v1") # can optionally use a named curve

    return ssl_context

######
# Create a TLS 1.2 context with all cipher suites in the supported list
# The server will choose which one to use
######
def getSSLContext_client():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    
    # add all suites to the supported list, the server will choose which to use
    suites = ""
    for e in CipherSuites:
        suites += e.value + ":"
    ssl_context.set_ciphers(suites[:-1]) # omit the last :
    
    return ssl_context
