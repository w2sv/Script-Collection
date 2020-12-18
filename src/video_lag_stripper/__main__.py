""" Strips consecutive frames of insufficient rate of pixel change of passed video
    and writing the thus resulting one to the video source path with a indicating file name 
    extension marking it as the lag stripped file. The original video will remain untouched.
    Video audio will not be passed along to the delagged file. 

    The absolute video file path is to be passed by means of the -p or --path option during 
    program command line invocation """


from typing import List

import cv2
import numpy as np
from tqdm import tqdm


def consecutive_frames_of_insufficient_rate_of_change_stripped(video_capture: cv2.VideoCapture, n_frames_original: int) -> List[np.ndarray]:
    """ Maintains merely consecutive frames of rate of pixel change
        bigger than heuristically determined treshold 

        Returns:
            list of filtered frames """

    MIN_RATE_OF_CHANGE = 0.20

    _, last_distinct_frame = video_capture.read()

    distinct_frames = []

    i, p_bar = 0, tqdm(total=n_frames_original)
    while True:
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


def get_write_path(path: str, video_format='avi') -> str:
    """ Parameters:
            path: absolute with data format suffix
            video_format: target video format 

        Returns:
            {path_w/o_data_format_suffix} delagged.{video_format} """

    return path[:path.find('.')] + f' delagged.{video_format}'


def new_fps(original_fps: int, n_frames_original: int, n_frames_new: int) -> int:
    """ Heuristically adjusts fps of delagged video to the new number of frames
        by reducing the original fps and thus leveling the increased speed of the 
        filtered video being a side-effect of the frame discarding

        Returns:
            original video fps reduced by what corresponds to the
            percental change between n_frames_original and n_frames_new """

    return int(original_fps - original_fps * n_frames_new / n_frames_original)


def write_video(frames: List[np.ndarray], fps: int, write_path: str):
    height, width = frames[0].shape[:2]
    video = cv2.VideoWriter(write_path, cv2.VideoWriter_fourcc(*"XVID"), fps, (width, height))

    for frame in frames:
        video.write(frame)

    print(f'Writing stripped video to {write_path} with {fps} fps...')

    cv2.destroyAllWindows()
    video.release()


def main(file_path: str):
    # provide video capture, retrieve/compute variables
    video_capture = cv2.VideoCapture(file_path)

    n_frames_original = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    print(f'Original fps: {fps}')

    # remove consecutive frames of insufficient rate of change
    distinct_consecutive_frames = consecutive_frames_of_insufficient_rate_of_change_stripped(video_capture,
                                                                                             n_frames_original=n_frames_original)

    # write processed video
    write_path = get_write_path(file_path)
    write_video(frames=distinct_consecutive_frames,
                fps=new_fps(fps, n_frames_original, len(distinct_consecutive_frames)), write_path=write_path)

    # display number of discarded frames
    n_discarded_frames = n_frames_original - len(distinct_consecutive_frames)
    print(f'Discarded {n_discarded_frames} frames, equaling {n_discarded_frames / n_frames_original * 100:.3f}%')


if __name__ == '__main__':
    from src.utils import parse_args, run

    args = parse_args(
        ('-p', '--path', str, 'path to the video file whose smoothness ought to be increased', None),
        include_dir_argument=True
    )

    FILE_PATH = args.path
    DIRECTORY_PATH = args.dir

    run(main, file_path=FILE_PATH, directory_path=DIRECTORY_PATH)
