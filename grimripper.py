import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import src.const.profiles as PROFILES
import src.methods as METHODS
 
def parse_args():
    parser = argparse.ArgumentParser(
        description="Rip DVDs using HandBrakeCLI with GPU/CPU support and resolution presets."
    )
    parser.add_argument(
        "-i", "--input", required=True,
        help="DVD input path. A directory containing multiple mounted DVDs (e.g. /media/user)."
    )
    parser.add_argument(
        "-o", "--output", required=True,
        help="Directory where output video files will be saved."
    )
    parser.add_argument(
        "-g", "--gpu", action="store_true",
        help="Use GPU encoding (nvenc_h264). If not set, uses CPU encoding (x264)."
    )
    parser.add_argument(
        "-r", "--resolution", required=True, choices=PROFILES.RESOLUTION_PROFILES.keys(),
        help="Set the output resolution. Options: 720p, 1080p, 2160p."
    )
    parser.add_argument(
        "-s", "--speed", required=True, choices=["slow", "mid", "fast"],
        help="Encoding speed and quality. slow = best quality, fast = fastest rip."
    )
    parser.add_argument(
        "--custom-args-file", type=str,
        help="Path to a file containing full custom HandBrakeCLI arguments. If provided, it replaces all default parameters."
    )

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    custom_args = []
    if args.custom_args_file:
        try:
            custom_args = METHODS.read_custom_args(args.custom_args_file)
        except Exception as e:
            print(f"Warning: failed to read custom args: {e}")

    try:
        dvd_mounts = METHODS.resolve_dvd_paths(args.input)

        with ProcessPoolExecutor() as executor:
            futures = {
                executor.submit(
                    METHODS.process_dvd,
                    path,
                    args.gpu,
                    args.resolution,
                    args.speed,
                    args.output,
                    custom_args
                ): path
                for path in dvd_mounts
            }

            for future in as_completed(futures):
                result = future.result()
                if result:
                    print(f"Completed: {result}")
                else:
                    print(f"Failed to process: {futures[future]}")

        print("\nAll DVDs processed.")

    except Exception as e:
        print(f"Failed: {e}")
