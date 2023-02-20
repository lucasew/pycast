def fingerprint_string(s: str) -> str:
    from hashlib import sha256

    symboldict = [
        *map(chr, range(ord("A"), ord("Z") + 1)),
        *map(chr, range(ord("0"), ord("9") + 1)),
    ]
    m = sha256()
    chars = []
    for char in s.upper():
        if char in symboldict:
            chars.append(char)
    txt = "".join(chars)
    m.update(txt.encode())
    return m.hexdigest()


def strduration2seconds(duration: str) -> int:
    parts = duration.split(":")
    multiplier = 1
    ret = 0
    while len(parts) > 0:
        part = int(parts.pop())
        ret += multiplier * part
        multiplier *= 60
    return ret


def reexport_url(url: str):
    from io import BufferedReader
    from urllib.request import urlopen

    return BufferedReader(urlopen(url))


def make_error_response(message: str, status_code=500):
    from flask import jsonify, make_response

    return make_response(jsonify(error=message), status_code)


def not_implemented_response():
    return make_error_response("not implemented", 501)
