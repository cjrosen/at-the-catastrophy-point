import cv2

def extractFrames(movie_path, output_path, frames):
    vidcap = cv2.VideoCapture(movie_path)
    for frame in frames:
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        success, image = vidcap.read()
        print(f"Read frame {frame:04}: {success}")
        cv2.imwrite( f"{output_path}/frame_{frame:04}.jpg", image)

def extractFrameRange(movie_path, output_path, start = 0, step = 1, stop = None):
    vidcap = cv2.VideoCapture(movie_path)
    success = True
    frame = start
    while success and (stop is None or frame < stop):
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        success, image = vidcap.read()
        print(f"Read frame {frame:04}: {success}")
        if not success:
            return
        cv2.imwrite( f"{output_path}/frame_{frame:04}.jpg", image)
        frame += step

if __name__ == "__main__":
    print("Extract video frames.")
    print(f"OpenCV version: {cv2.__version__}")

    extractFrameRange(f"data/Mohr_CC_half.mov", f"output/original_frames", 0, 1, None)
