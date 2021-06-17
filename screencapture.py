import subprocess
import time
from PIL import Image
import imagehash
import argparse
import mss
import pathlib
from gooey import Gooey

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

def get_screenshot_image(display):
    with mss.mss() as sct:
        sct_img = sct.grab(sct.monitors[display])
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

@Gooey
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", 
        help="Directory where screenshots will be saved. If the specified directory does not exist, a new directory will be created.")
    parser.add_argument("-i", "--interval", type=int, help="Time interval for taking a screenshot. default=4", default=4)
    parser.add_argument("-t", "--timeout", type=int, help="Time to keep taking screenshots (minutes). default=120", default=120)
    parser.add_argument("-s", "--similarity_tolerance", type=int,
        help="Maximum value of the Hamming distance at which two screenshots are considered to be similar. The larger this value is, the more likely it is that the same page of slides will be saved multiple times. default=5", 
        default=5)
    parser.add_argument("-d", "--display", type=int,
        help="Display where the screenshot will be taken. 1 is main, 2 secondary, etc. default=1",
        default=1)
    parser.add_argument("-m", "--movie_interval", type=int,
        help="(beta) Time interval to save the video. For example, 1 if it is the same as the interval of time to take a screenshot, and 2 if it is twice as long. This option is still in beta, so it may not work properly for you. default=1", 
        default=1)

    args = parser.parse_args()

    directory = args.directory
    interval = args.interval
    timeout_minute = args.timeout
    similarity_tolerance = args.similarity_tolerance
    display = args.display
    movie_interval = args.movie_interval


    subprocess.run(["mkdir", "-p", directory])

    start_time = time.time()
    elapsed_time = 0
    saved_image_number = init_saved_image_number(directory)
    timeout_second = timeout_minute * 60
    successive_non_similar_count = 0

    current_image = get_screenshot_image(display)
    current_image.save(f'{directory}/sct-{saved_image_number}.jpg', 'JPEG')
    saved_image_number += 1
    pre_image = current_image

    while elapsed_time < timeout_second:
        current_image = get_screenshot_image(display)

        if is_similar_image(current_image, pre_image, similarity_tolerance):
            successive_non_similar_count = 0
        else:
            print(calculate_hamming_distance(current_image, pre_image))
            if not is_movie(successive_non_similar_count):
                current_image.save(f'{directory}/sct-{saved_image_number}.jpg', 'JPEG')
                saved_image_number += 1
            increment_value_with_reset(successive_non_similar_count, movie_interval)

        pre_image = current_image
        elapsed_time = time.time() - start_time
        time.sleep(interval)
    

if __name__ == "__main__":
    main()