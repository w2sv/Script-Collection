""" Strips consecutive frames of insufficient rate of pixel change of passed video
    and writing the thus resulting one to the video source path with a indicating file name 
    extension marking it as the lag stripped file. The original video will remain untouched.
    Video audio will not be passed along to the delagged file. 

    The absolute video file path is to be passed by means of the -p or --path option during 
    program command line invocation """

import cv2

from src.video_lag_stripper import (
    consecutive_frames_of_insufficient_rate_of_change_stripped,
    get_write_path,
    write_video,
    new_fps
)


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
