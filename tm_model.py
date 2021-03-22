import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

######
# Teachable Machine Model
# Required python v3.7.10
# Required tensorflow v2.
#####
class TM_Model:


    def __init__(self, model_path):

        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Load the model
        self.model = tensorflow.keras.models.load_model(model_path)

        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1.
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


    def predict(self, image, threshold=0.9):
        # Replace this with the path to your image
        # image = Image.open('dog.jpg')

        #resize the image to a 224x224 with the same strategy as in TM2:
        #resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        #turn the image into a numpy array
        image_array = np.asarray(image)

        # display the resized image
        # image.show()

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        self.data[0] = normalized_image_array

        # run the inference
        prediction = self.model.predict(self.data)
        print(prediction)
        max_value = np.max(prediction)
        print('max: ', max_value)
        if max_value > threshold:
            return np.argmax(prediction)
        return -1
