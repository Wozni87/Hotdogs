import tensorflow.keras
from PIL import Image, ImageOps, ImageDraw, ImageFont
import numpy as np
import os

#creates a new image with a Hotdog or Not Hotdog water mark in the Hotdog Analysis folder
def watermark(analysis):
    print(f'File: {filename} is a Hot Dog')
    width, height = image.size
    output = ImageDraw.Draw(image)
    font = ImageFont.truetype('arial.ttf', 42)
    textwidth, textheight = output.textsize(analysis, font)
    margin = 0
    x = width - textwidth - margin
    y = height - textheight - margin
    output.text((x, y), analysis, font=font)
    image.save(f'./Hotdog Analysis/{filename}')


# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Replace this with the path to your image
for filename in os.listdir('./Photo'):
    if filename.endswith('.jpg'):
        image = Image.open(str('./Photo/' + filename))

        # resize the image to a 224x224 with the same strategy as in TM2:
        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        # turn the image into a numpy array
        image_array = np.asarray(image)

        # display the resized image
        # image.show()

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = model.predict(data)
        hotdog_percent = prediction.item(0) * 100
        if hotdog_percent > 90:
            print(f'File: {filename} is a Hot Dog')
            analysis = 'HotDog'
            watermark(analysis)
        else:
            print(f'File: {filename} is not a Hot Dog')
            analysis = 'Not HotDog'
            watermark(analysis)
    else:
        print('JPG files only please')
