import subprocess
import os
import shlex
from src.const import profiles as PROFILES

def resolve_dvd_paths(input_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input path not found: {input_path}")

    if os.path.isdir(input_path):
        subdirs = [
            os.path.join(input_path, d)
            for d in os.listdir(input_path)
            if os.path.isdir(os.path.join(input_path, d))
        ]
        if not subdirs:
            raise RuntimeError(f"No mounted DVDs found in: {input_path}")
        return subdirs
    elif os.path.ismount(input_path):
        return [input_path]
    else:
        raise ValueError(f"Invalid input path: {input_path}")


def read_custom_args(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Custom arguments file not found: {file_path}")

    with open(file_path, "r") as f:
        content = f.read()

    return shlex.split(content)


def rip_dvd_to_mp4(dvd_path, output_file, use_gpu, resolution, speed, custom_args):
    command = ["HandBrakeCLI", "-i", dvd_path, "-o", output_file]

    if custom_args:
        command.extend(custom_args)
    else:
        profile = PROFILES.RESOLUTION_PROFILES[resolution]
        encoder = "nvenc_h264" if use_gpu else "x264"
        preset = PROFILES.PRESET_PROFILES[resolution][speed]

        command.extend([
            "--main-feature",
            "-f", "mp4",
            "-e", encoder,
            "-q", profile["quality"],
            "--deinterlace",
            "--width", profile["width"],
            "--height", profile["height"],
            "--rate", "24",
            "--preset", preset,
            "--subtitle", "none"
        ])

    try:
        print(f"Starting rip: {output_file}")
        subprocess.run(command, check=True)
        print(f"Success: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error during ripping {output_file}: {e}")
        return None
    except FileNotFoundError:
        print("HandBrakeCLI not found.")
        return None



def process_dvd(dvd_path, use_gpu, resolution, speed, base_output_dir, custom_args):
    dvd_label = os.path.basename(dvd_path)
    output_dir = os.path.join(base_output_dir, dvd_label)
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"{dvd_label}.mp4")
    return rip_dvd_to_mp4(dvd_path, output_file, use_gpu, resolution, speed, custom_args)

