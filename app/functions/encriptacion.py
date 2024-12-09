import base64

def decode(text):
    """ Función para decodificar un string de base64, actualmente el token de rut """
    # encoded_bytes = base64.b64decode(text.encode("utf-8"))
    try:
        encoded_bytes = base64.b64decode(text)
        encoded_str = str(encoded_bytes, "utf-8")
        resultado = encoded_str
        return resultado
    except:
        return text

def encode(text):
    """ función para encriptar la data """ #cambiar de ubicación cuando se mejore a una función más segura
    encoded_bytes = base64.b64encode(text.encode("utf-8"))
    encoded_str = str(encoded_bytes, "utf-8")
    return encoded_str