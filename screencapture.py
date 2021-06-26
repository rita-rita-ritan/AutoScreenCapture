import subprocess
import time
from PIL import Image
import imagehash
import argparse
import mss
import pathlib
from gooey import Gooey, GooeyParser

import region_selector

def init_saved_image_number(directory):
    # 前回と同じディレクトリに再び保存する場合に、前回の保存写真の後に続くようにナンバリングする
    # When saving again to the same directory as last time,
    # number the photos to follow the last saved photo.
    saved_image_number = 0
    path_objects = pathlib.Path(directory)
    files = {p.name for p in path_objects.glob("sct-*.jpg")}
    while f"sct-{saved_image_number}.jpg" in files:
        saved_image_number += 1
    return saved_image_number

def get_screenshot_image(display, region = None):
    with mss.mss() as sct:
        if region == None:
            sct_img = sct.grab(sct.monitors[display])
        else:
            top = region[0][1]
            left = region[0][0]
            width = region[1][0] - region[0][0]
            height = region[1][1] - region[0][1]
            monitor = {"top": int(top), "left": int(left), "width": int(width), "height": int(height)}
            sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        return img

def calculate_hamming_distance(image1, image2):
    hash1 = imagehash.average_hash(image1)
    hash2 = imagehash.average_hash(image2)
    hamming_distance = hash1 - hash2
    return hamming_distance

def is_similar_image(image1, image2, similarity_tolerance=0):
    hamming_distance = calculate_hamming_distance(image1, image2)
    if hamming_distance <= similarity_tolerance:
        return True
    return False

def is_movie(successive_non_similar_count):
    if successive_non_similar_count >= 1:
        return True
    return False

def increment_value_with_reset(value, threshold):
    value += 1
    if value >= threshold:
        value = 0
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", 
        help="Directory where screenshots will be saved.")
    parser.add_argument("-i", "--interval", type=int, help="Time interval for taking a screenshot. default=4", default=4)
    parser.add_argument("-t", "--timeout", type=int, 
        help="Time to keep taking screenshots (minutes). default=120", default=120)
    parser.add_argument("-s", "--similarity_tolerance", type=int,
        help="Maximum value of the Hamming distance at which two screenshots are considered to be similar. The larger this value is, the more likely it is that the same page of slides will be saved multiple times. default=5", 
        default=5)
    parser.add_argument("-d", "--display", type=int,
        help="Display where the screenshot will be taken. 1 is main, 2 secondary, etc. default=1",
        default=0)
    parser.add_argument("-m", "--movie_interval", type=int,
        help="(beta) Time interval to save the video. For example, 1 if it is the same as the interval of time to take a screenshot, and 2 if it is twice as long. This option is still in beta, so it may not work properly for you. default=1", 
        default=1)
    parser.add_argument("-r", "--region-selection", action="store_true",
        help="(beta) Select screen region to capture. (Ubuntu, OSX)")

    args = parser.parse_args()

    directory = args.directory
    interval = args.interval
    timeout_minute = args.timeout
    similarity_tolerance = args.similarity_tolerance
    display = args.display
    movie_interval = args.movie_interval
    region_selection = args.region_selection

    subprocess.run(["mkdir", "-p", directory])

    # select region
    if region_selection:
        region = region_selector.get_region(display)
        time.sleep(0.5) # delay
    else:
        region = None

    print("Directory:", directory)
    print(f"progress: 0/{timeout_minute}")

    start_time = time.time()
    elapsed_time_second = 0
    elapsed_time_minute = 0
    saved_image_number = init_saved_image_number(directory)
    timeout_second = timeout_minute * 60
    successive_non_similar_count = 0

    current_image = get_screenshot_image(display, region)
    current_image.save(f'{directory}/sct-{saved_image_number}.jpg', 'JPEG')
    print(f"Saved screenshot: sct-{saved_image_number}.jpg\n")
    saved_image_number += 1
    pre_image = current_image

    while elapsed_time_second < timeout_second:
        current_image = get_screenshot_image(display, region)

        if is_similar_image(current_image, pre_image, similarity_tolerance):
            successive_non_similar_count = 0
        else:
            if not is_movie(successive_non_similar_count):
                current_image.save(f'{directory}/sct-{saved_image_number}.jpg', 'JPEG')
                print(f"Saved screenshot: sct-{saved_image_number}.jpg")
                print("(Hamming Distance)", calculate_hamming_distance(current_image, pre_image), "\n")
                saved_image_number += 1
            successive_non_similar_count = increment_value_with_reset(successive_non_similar_count, movie_interval)
            pre_image = current_image

        elapsed_time_second = time.time() - start_time
        if elapsed_time_minute != int(elapsed_time_second/60):
            elapsed_time_minute = int(elapsed_time_second/60)
            print(f"progress: {elapsed_time_minute}/{timeout_minute}")
        time.sleep(interval)
    

if __name__ == "__main__":
    main()