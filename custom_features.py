from enum import Enum

import cv2
import numpy as np
from scipy import spatial
from skimage.color import rgb2gray
from skimage.feature import hog
from skimage.feature import local_binary_pattern

from vgg16_features import extract_features_using_vgg16


# def extract_features(image_path, color_bins=(8, 8, 8), lbp_bins=256, P=8, R=1, resize_dim=(256, 256)):
#     # Load the image
#     image = cv2.imread(image_path)
#     # Resize the image to ensure consistency
#     image_resized = cv2.resize(image, resize_dim)
#
#     # Extract color histogram from the resized image
#     color_hist = extract_color_histogram(image_resized, bins=color_bins)
#
#     lbp_hist = extract_lbp_histogram(image_resized, P=P, R=R, bins=lbp_bins)
#
#     # print(color_hist)
#     # print(lbp_hist)
#     # Concatenate the color and texture histograms to form a single feature vector
#     features = np.hstack([color_hist, lbp_hist])
#     # print(features)
#
#     return features
#
#
# def extract_color_histogram(image, bins=(8, 8, 8)):
#     # Convert the image to HSV color-space
#     hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#     # Compute the color histogram
#     hist = cv2.calcHist([hsv_image], [0, 1, 2], None, bins,
#                         [0, 256, 0, 256, 0, 256])
#     # Normalize the histogram and ensure it's float32
#     hist = cv2.normalize(hist, hist).flatten().astype("float32")
#     return hist
#
#
# def extract_lbp_histogram(image, P=8, R=1, bins=256):
#     # Convert the resized image to grayscale for LBP histogram extraction
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # Apply LBP
#     lbp = local_binary_pattern(gray_image, P, R, method="uniform")
#     # Compute the LBP histogram and normalize
#     (hist, _) = np.histogram(lbp.ravel(), bins=np.arange(0, bins + 1), range=(0, bins))
#     hist = hist.astype("float")
#     hist /= (hist.sum() + 1e-7)
#     # Ensure the histogram is of type float32
#     hist = hist.astype("float32")
#     return hist


def extract_color_histogram(image, bins=(32, 32, 32), color_space='hsv'):
    # Convert the image to the specified color space
    if color_space == 'hsv':
        converted_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    elif color_space == 'lab':
        converted_img = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    elif color_space == 'ycrcb':
        converted_img = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    else:
        converted_img = image  # If no conversion is needed, use BGR

    # Compute the color histogram with increased bins for more detail
    hist = cv2.calcHist([converted_img], [0, 1, 2], None, bins,
                        [0, 256, 0, 256, 0, 256])

    # Normalize the histogram
    hist = cv2.normalize(hist, hist).flatten().astype("float32")
    return hist


def extract_lbp_features(image, numPoints=24, radius=3, bins=26):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Compute the Local Binary Pattern representation
    lbp = local_binary_pattern(gray, numPoints, radius, method="uniform")
    # Compute the histogram of the LBP with more points and a smaller radius
    (hist, _) = np.histogram(lbp.ravel(), bins=np.arange(0, bins + 3),
                             range=(0, numPoints + 2))
    # Normalize the histogram
    hist = hist.astype("float")
    hist /= (hist.sum() + 1e-7)
    hist = hist.astype("float32")
    return hist


def extract_hog_features(image):
    # If the image has more than one channel, convert it to grayscale
    if image.ndim > 2:
        image = rgb2gray(image)

    # Extract Histogram of Oriented Gradients (HOG) features
    hog_features = hog(image)

    return hog_features.astype("float32")


def extract_custom_features(image_path, bins=(32, 32, 32), color_space='hsv', numPoints=24, radius=8):
    # Load and resize the image to a fixed-size to ensure consistency
    image = cv2.imread(image_path)
    image = cv2.resize(image, (256, 256))

    # Extract color and LBP features
    color_feat = extract_color_histogram(image)
    lbp_feat = extract_lbp_features(image, numPoints=numPoints, radius=radius)
    hog_feat = extract_hog_features(image)

    # Concatenate the color and LBP histograms to form a single feature vector
    features = np.hstack([color_feat, lbp_feat, hog_feat])
    # features = np.hstack([lbp_feat])
    # features = np.hstack([color_feat])
    return features


class Mode(Enum):
    CUSTOM = 1
    VGG16 = 2


def extract_features(image_path, mode=Mode.VGG16):
    features = []
    if mode == Mode.CUSTOM:
        features = extract_custom_features(image_path)
    elif mode == Mode.VGG16:
        features = extract_features_using_vgg16(image_path)
    return features


def compare_features(features_a, features_b):
    score = 1 - spatial.distance.cosine(features_a, features_b)
    return score
