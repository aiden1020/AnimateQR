import subprocess
import glob
import os

def convert_mp4_to_gif(input_mp4_path, output_gif_path, fps=10):
    """
    Convert an MP4 video to a GIF with a specified FPS using ffmpeg.

    Parameters:
        input_mp4_path (str): Path to the input MP4 file.
        output_gif_path (str): Path to save the output GIF.
        fps (int): Frames per second for the output GIF (default is 10).

    Returns:
        None
    """
    try:
        # Build the ffmpeg command
        command = [
            "ffmpeg",
            "-i", input_mp4_path,      # Input file
            "-vf", f"fps={fps}",     # Set the frame rate
            output_gif_path            # Output file
        ]

        # Run the ffmpeg command
        subprocess.run(command, check=True)
        print(f"GIF saved at {output_gif_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    video_root = 'demo/AnimateDiff_artcoder_seg'
    video_paths = glob.glob(f'{video_root}/*.mp4')
    os.makedirs(f'{video_root}/gif', exist_ok=True)
    for path in video_paths:
        basename = os.path.basename(path).split('.')[0]
        save_path = f'{video_root}/gif/{basename}.gif'

        convert_mp4_to_gif(path, save_path, fps=10)