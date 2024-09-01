# Import dependencies
import cv2
import torch
import matplotlib.pyplot as plt
import ffmpeg
import numpy as np

# Download the MiDaS
midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")
midas.to("cpu")
midas.eval()
# Input transformation pipeline
transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
transform = transforms.small_transform

img = cv2.imread("input/IMG_3133.JPG")
width = img.shape[0]
height = img.shape[1]
new_size = (750, int(750 * (width / height)))
print(new_size, (width, height))
img = cv2.resize(img, new_size)


# Transform input for midas
imgbatch = transform(img).to("cpu")


# Make a prediction
with torch.no_grad():
    prediction = midas(imgbatch)
    prediction = torch.nn.functional.interpolate(
        prediction.unsqueeze(1),
        size=img.shape[:2],
        mode="bicubic",
        align_corners=False,
    ).squeeze()

    output = prediction.cpu().numpy()

output = (output * 255) / 1600

cv2.imwrite("output/output_midas.jpeg", output)
cv2.imwrite("output/output_img.jpeg", img)
