import base64

def encode(oid):
    enc = str(base64.b64encode(bytes(str(oid), 'utf-8')))
    enc = enc[2 : len(enc)-1]
    return enc

def decode(id):
    return base64.b64decode(id).decode('utf-8')