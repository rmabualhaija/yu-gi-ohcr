import os
import cv2
import random
import numpy as np

def select_random_image_samples(sample_size: int) -> np.array:
    """Shuffle all the images then divide then into chunks of sample_size and return the 

    Args:
        sample_size (int): The number of images to sample 
    
    Returns:
        list[list[str]]: A list of grouped sample chunks e.g. [[img1, img4, img100], [img2, img3000, img2100]...]
    """
    
    image_files = os.listdir('card_images/')
    image_files = np.array(image_files)
    num_chunks = len(image_files)/sample_size
    samples = np.array_split(image_files, num_chunks)
    return samples


def select_random_bg_images(num_images) -> np.array:
    """ Select num_images random background images.

    Args:
        num_images (int): The number of background images to select.
    Returns:
        np.array: A numpy array of the selected background images
    """
    background_images = np.array(os.listdir('dtd/'))
    background_images = [np.random.choice(len(background_images), size=num_images, replace=False)]
    return background_images
    

def resize_image(image, scale_factor) -> np.array:
    """
    Resize the input image evenly on both axes by the scale factor.

    Args:
        image (np.array): The image to be scaled as a numpy array
        scale_factor (float): a number between 0 and 2 representing the percentage to scale the image by

    Returns:
        np.array: The rotated image as a numpy array
    """
    width = int(image.shape[1] * scale_factor)
    height = int(image.shape[0] * scale_factor)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return resized

def rotate_image(image: np.array, angle: int) -> np.array:
    """Rotate the image by the angle provided and return as a numpy array
    
    Args:
        image (np.array): the image to rotate as a numpy array
        angle (int): Angle of roation between 0 and 359

    Returns:
        np.array: The rotated image as a numpy array
    """
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def translate_image(image: np.array, x: int, y: int) -> np.array:
    """Tranlsate an image by x and y

    Args:
        image (np.array): The image to translate
        x (int): The horizontal translation of the image
        vertical_translation (int): The vertical translation of the image
    """
    rows,cols = image.shape
    translation_matrix = np.float32([[1,0,x],[0,1,y]])
    translated_image = cv2.warpAffine(image, translation_matrix, (cols,rows))

    return translated_image

def apply_random_orientation(image: np.array) -> np.array:
    """ Take an image and apply the following transformations:
        - Scale the image by 0.75
        - Rotate the image a random amount
        - Translate it a random amount on the x and y axis between -100 and 100

    Args:
        image (np.array): The image to apply transformations to

    Returns:
        _type_: The translated image
    """
     
    rotation_angle = random.randint(0,359)
    x_translation = random.randint(-100, 100)
    y_translation = random.randint(-100, 100)
    scaled_image = resize_image(0.75)
    transformed_image = rotate_image(scaled_image, rotation_angle)
    transformed_image = translate_image(transformed_image, x=x_translation, y=y_translation)
    return transformed_image

def generate_random_image():
    images = select_random_image_samples(10)
    loaded_images = []
    test_images = images[0]
    for image in test_images:
        loaded_images.append(cv2.imread(f'card_images/{image}'))
    
    transformed_images = []   
    for image in loaded_images:
         transformed_images.append(apply_random_orientation(image))
        
        
    
    

# img = cv2.imread('card_images/31230289.jpg')
# img2 = cv2.imread('card_images/38479725.jpg')
# rotated_image = rotate_image(img, 60)

# # concatenate image Horizontally
# horizontal_concat = np.concatenate((rotated_image, img2), axis=1)
  
# # concatenate image Vertically
# vertical_concat = np.concatenate((img, img2), axis=0)
  
# cv2.imshow('HORIZONTAL', horizontal_concat)
# cv2.imshow('VERTICAL', vertical_concat)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# print(select_random_image_samples(10))
print(select_random_bg_images(10))
