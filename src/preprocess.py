import cv2
import numpy as np
from scipy import ndimage

def get_best_shift(img):

    cy, cx = ndimage.center_of_mass(img)
    rows, cols = img.shape
    shiftx = np.round(cols / 2.0 - cx)
    shifty = np.round(rows / 2.0 - cy)
    return shiftx, shifty

def shift(img, sx, sy):

    rows, cols = img.shape
    M = np.float32([[1, 0, sx], [0, 1, sy]])
    shifted = cv2.warpAffine(img, M, (cols, rows))
    return shifted

def preprocess_canvas_image(pil_image):


    image_np = np.array(pil_image)
    if len(image_np.shape) == 3:
        if image_np.shape[2] == 4:
            gray = cv2.cvtColor(image_np, cv2.COLOR_RGBA2GRAY)
        else:
            gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    else:
        gray = image_np.copy()

    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

    while np.sum(thresh[0, :]) == 0 and thresh.shape[0] > 1:
        thresh = thresh[1:, :]
    while np.sum(thresh[:, 0]) == 0 and thresh.shape[1] > 1:
        thresh = thresh[:, 1:]
    while np.sum(thresh[-1, :]) == 0 and thresh.shape[0] > 1:
        thresh = thresh[:-1, :]
    while np.sum(thresh[:, -1]) == 0 and thresh.shape[1] > 1:
        thresh = thresh[:, :-1]

    rows, cols = thresh.shape

    if rows <= 2 or cols <= 2:
        return np.zeros((1, 28, 28, 1), dtype="float32")

    if rows > cols:
        factor = 20.0 / rows
        rows = 20
        cols = int(round(cols * factor))
    else:
        factor = 20.0 / cols
        cols = 20
        rows = int(round(rows * factor))

    cols = max(1, cols)
    rows = max(1, rows)

    resized_digit = cv2.resize(thresh, (cols, rows), interpolation=cv2.INTER_AREA)

    padded_image = np.zeros((28, 28), dtype=np.uint8)
    start_row = (28 - rows) // 2
    start_col = (28 - cols) // 2
    padded_image[start_row:start_row + rows, start_col:start_col + cols] = resized_digit

    shiftx, shifty = get_best_shift(padded_image)
    shifted_image = shift(padded_image, shiftx, shifty)

    normalized = shifted_image.astype("float32") / 255.0
    reshaped = np.reshape(normalized, (1, 28, 28, 1))

    return reshaped