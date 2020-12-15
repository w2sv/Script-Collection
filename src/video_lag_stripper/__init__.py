from typing import List, Tuple

import cv2
import numpy as np
from tqdm import tqdm


def identical_consecutive_frames_stripped_file(video_capture: cv2.VideoCapture) -> Tuple[List[np.ndarray], int]:
    MIN_RATE_OF_CHANGE = 0.20

    _, last_distinct_frame = video_capture.read()

    distinct_frames = []

    i, p_bar = 0, tqdm(total=n_frames_original)
    while(True):
        i += 1

        p_bar.set_description(f'Processing frame {i}')
        p_bar.update(1)

        success, frame = video_capture.read()

        if not success:
            break

        if _rate_of_change(frame, last_distinct_frame) >= MIN_RATE_OF_CHANGE:
            distinct_frames.append(last_distinct_frame)
            last_distinct_frame = frame

    distinct_frames.append(last_distinct_frame)
    return distinct_frames


def _rate_of_change(frame1: np.ndarray, frame2: np.ndarray) -> float:
    diff = cv2.absdiff(frame1, frame2).astype(np.uint8)
    return np.count_nonzero(diff) / diff.size


def get_write_path(path: str, data_format='avi') -> str:
    return path[:path.find('.')] + f' delagged.{data_format}'


def new_fps(original_fps: int, n_frames_original: int, n_frames_new: int) -> int:
    return int(original_fps - n_frames_new / n_frames_original * original_fps)


def write_mp4(frames: List[np.ndarray], fps: int, write_path: str):
    height, width = frames[0].shape[:2]
    video = cv2.VideoWriter(write_path, cv2.VideoWriter_fourcc(*"XVID"), fps, (width, height))

    for frame in frames:
        video.write(frame)

    print(f'Writing stripped video to {write_path} with {fps} fps...')

    cv2.destroyAllWindows()
    video.release()


if __name__ == '__main__':
    import argparse

    # parse path from command option
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str, help='path to the video file whose smoothness ought to be increased')

    args = parser.parse_args()
    file_path = args.path

    # provide video capture, retrieve/compute variables
    video_capture = cv2.VideoCapture(file_path)
    
    n_frames_original = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    print(f'Original fps: {original_fps}')

    # remove consecutive frames of insufficient rate of change
    distinct_consecutive_frames = identical_consecutive_frames_stripped_file(video_capture)

    # write processed video
    write_path = get_write_path(file_path)
    write_mp4(frames=distinct_consecutive_frames, fps=new_fps(fps, n_frames_original, len(distinct_consecutive_frames)), write_path=write_path)

    # display number of discarded frames
    n_discarded_frames = n_frames_original - len(distinct_consecutive_frames)
    print(f'Discarded {n_discarded_frames} frames, equaling {n_discarded_frames / n_frames_original * 100:.3f}%')
