from PIL import Image , ImageEnhance , ImageFilter
import os
# img1 = Image.open('inam.jpg')
# img1.save('cat-3.pdf')
# img1.show()

# MAX_SIZE = (350,350)
# img1.thumbnail(MAX_SIZE)
# img1.save('inamsmall.jpg')

# for item in os.listdir():
#     if item.endswith('.jpg'):
#         img1 = Image.open(item)
#         filename , extension = os.path.splitext(item)
#         img1.save(f'{item}.png')

# -----------Sharpness--------
# img1 = Image.open('inam.jpg')
# enhancer = ImageEnhance.Sharpness(img1)
# enhancer.enhance(4).save('inamsharpness.jpg')


# --------Brightness---------
# img1 = Image.open('inam.jpg')
# enhancer = ImageEnhance.Brightness(img1)
# enhancer.enhance(1.5).save('inambrightness.jpg')

# -----------Contrast----------
# img1 = Image.open('inam.jpg')
# enhancer = ImageEnhance.Contrast(img1)
# enhancer.enhance(1.5).save('inamcontrast.jpg')


img1 = Image.open('inam.jpg')
img1.filter(ImageFilter.GaussianBlur(radius=4)).save('inamgaussinablur.jpg')