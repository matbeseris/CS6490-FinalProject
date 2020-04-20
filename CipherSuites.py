# This file contains the main TLS cipher suits whose energy use will be analyzed
import ssl

class CipherSuites(Enum):
    DHERSA_AES256 = "DHE-RSA-AES256-GCM-SHA384"
    DHERSA_CHACHA20 = "DHE-RSA-CHACHA20-POLY1305"
    DHEPSK_AES256 = "DHE-PSK-AES256-GCM-SHA384"
    DHEPSK_CHACHA20 = "DHE-PSK-CHACHA20-POLY1305"

def getSSLContext_server(ciphers):
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.set_ciphers(ciphers)

    if ciphers == CipherSuites.DHERSA_AES256 or ciphers == CipherSuites.DHERSA_CHACHA20:
        ssl_context.load_cert_chain(certfile="cert.pem", keyfile="cert.pem") # load serve certificate and private key
        ssl_context.load_dh_params("dhparams.pem") # load the parameters for Diffie-Hellman

    if ciphers == CipherSuites.DHEPSK_AES256 or ciphers == CipherSuites.DHEPSK_CHACHA20:
        ssl_context.load_cert_chain(certfile="cert.pem", keyfile="cert.pem") # load serve certificate and private key
        ssl_context.load_dh_params("dhparams.pem") # load the parameters for Diffie-Hellman

    return ssl_context

def getSSLContext_client(ciphers):
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.set_ciphers(ciphers)
    