import json
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
import json


def generate_qr(ip, room_code):

    data = json.dumps({
        "ip": ip,
        "room": room_code
    })

    img = qrcode.make(data)

    img.save("pairing_qr.png")

def read_qr(path):

    img = Image.open(path)

    decoded = decode(img)

    if not decoded:
        return None

    data = decoded[0].data.decode()

    return json.loads(data)