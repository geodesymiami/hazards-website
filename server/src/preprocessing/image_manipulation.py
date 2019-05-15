from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageFont

"""

    Should include the following functions:

    - pad_image(image pad=(top, bottom, left, right))
    - add_text_to_image(image, text, size, location)
    - compress_image(image, compression)

"""


def pad_image(image):

    img = image.convert("RGB")
    width, height = img.size

    new_size = (width, height + int(round(height / 12)))  # White bar is 10% the height of the image
    padImg = Image.new("RGB", new_size, color='WHITE')

    return padImg, width, height


def add_text_to_image(image, text):
    pad_img, width, height = pad_image(image)

    loc = (round(width - (len(text) * round(height / 20)) * 1.5), 5)
    font = ImageFont.truetype("resources/arial.ttf", int(round(height / 20)))  # Font Size should fill the white bar

    pad_img.paste(image, (0, round(height / 12)))
    draw = ImageDraw.Draw(pad_img)
    draw.text(loc, text, (0, 0, 0), font=font)  # (0,0,0) is color Black
    draw = ImageDraw.Draw(pad_img)
    return pad_img


def compress_image(image_file, compression_amount=0.7):
    img = Image.open(image_file)
    img = img.convert("RGB")
    width, height = img.size
    img = img.resize((int(width*compression_amount), int(height*compression_amount)))
    return img


if __name__ == "__main__":
    """
    Please provide an example of how to use your functions. These test cases should
    work in general (minus the specification of the input files and output paths).
    """

    im = compress_image("/Users/joshua/Desktop/test.png")
    im = add_text_to_image(im, "Test Text 2")

    im.save("/Users/joshua/Desktop/new.jpg")
