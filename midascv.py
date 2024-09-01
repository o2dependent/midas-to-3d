# Import dependencies
import cv2
import torch
import matplotlib.pyplot as plt
import numpy as np

# Download the MiDaS
midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")
midas.to("cpu")
midas.eval()
# Input transformation pipeline
transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
transform = transforms.small_transform

cap = cv2.VideoCapture("andy_anderson_dark_slide_snake.mp4")
out = None
fourcc = 0x7634706D

# Hook into OpenCV
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("can't receive frame data")
        break

    # Transform input for midas
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imgbatch = transform(img).to("cpu")

    if out is None:
        out = cv2.VideoWriter(
            "cv_output.mp4", fourcc, 30.0, (frame.shape[1], frame.shape[0])
        )

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

    # cv2.imwrite("output.jpeg", (output * 255) / 1000)
    cv2.imshow(
        "CV2Frame",
        output.astype(np.uint8),
    )
    plt.pause(0.000001)

    img_byte_arr = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    out.write(img_byte_arr)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        cap.release()
        cv2.destroyAllWindows()

plt.show()
cap.release()
out.release()
