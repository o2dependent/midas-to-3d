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

cap = cv2.VideoCapture("andy_anderson_dark_slide_snake.mp4")


def get_save_video_process(saving_file_name, i_width, i_height, fps=33.0):
    return (
        ffmpeg.input(
            "pipe:",
            format="rawvideo",
            pix_fmt="rgb24",
            s="{}x{}".format(i_width, i_height),
        )
        .output(saving_file_name, pix_fmt="yuv420p", vcodec="libx264", r=fps, crf=37)
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )


process = None

# Hook into OpenCV
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("can't receive frame data")
        break

    # Transform input for midas
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imgbatch = transform(img).to("cpu")

    if process is None:
        process = get_save_video_process(
            "output.mp4", frame.shape[1], frame.shape[0], 60
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
        print(output)

    output = (output * 255) / 1600
    process.stdin.write(
        cv2.cvtColor(output, cv2.COLOR_GRAY2RGB).astype(np.uint8).tobytes()
    )
    # cv2.imwrite("output.jpeg", (output * 255) / 1000)
    cv2.imshow(
        "CV2Frame",
        output.astype(np.uint8),
    )
    plt.pause(0.000001)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        cap.release()
        cv2.destroyAllWindows()

plt.show()
cap.release()
