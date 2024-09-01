import cv2
import json

img = cv2.imread("output/output_midas.jpeg", cv2.IMREAD_GRAYSCALE)
data = {"width": len(img[0]), "height": len(img), "data": img.tolist()}

with open("output/midas_data.json", "w") as f:
    json.dump(data, f)
