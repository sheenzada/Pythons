# install
# pip install qrcode[pil]

import qrcode

text = input("Enter Your Text: ")

try:
    qr = qrcode.QRCode()
    qr.add_data(text)
    qr.make()
    img = qr.make_image()
    img.save("qrcode.png")
    print("Qr Code Generated.")
except:
    print("Unable To Generate Qr Code")