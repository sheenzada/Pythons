# # install
# # pip install qrcode[pil]

# import qrcode

# text = input("Enter Your Text: ")

# try:
#     qr = qrcode.QRCode()
#     qr.add_data(text)
#     qr.make()
#     img = qr.make_image()
#     img.save("qrcode.png")
#     print("Qr Code Generated.")
# except:
#     print("Unable To Generate Qr Code")


# Install required library before running:
# pip install qrcode[pil]

import qrcode

def generate_qr_code():
    text = input("Enter Your Text: ")

    try:
        # Create a QRCode object with default settings
        qr = qrcode.QRCode(
            version=1,  # controls size of the QR Code, 1 is 21x21
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,  # size of each box in pixels
            border=4,     # thickness of border (minimum 4)
        )
        qr.add_data(text)
        qr.make(fit=True)

        # Generate the image
        img = qr.make_image(fill_color="black", back_color="white")

        # Save to a file
        img.save("qrcode.png")
        print("QR Code Generated and saved as qrcode.png")

    except Exception as e:
        print(f"Unable To Generate QR Code: {e}")

if __name__ == "__main__":
    generate_qr_code()
