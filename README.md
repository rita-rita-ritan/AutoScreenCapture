# AutoScreenCapture
AutoScreenCapture is a cross-platform program that automatically takes screenshots for you. 

## 📸 Feature

* <b>Cross-Platform</b>: Mac, Linux, Windows (Only tested on Mac, but should work on Linux and Windows as well. If not work on Linux or Windows, please [contact me](https://twitter.com/rita_rita_ritan))
* Support for <b>Multiple Displays</b>
* <b>Both GUI and CUI</b> are supported
* Equipped with <b>Slide Page-Turning Detection</b> function, which prevent you from saving the same page of slides over and over again.

<table>
<tr>
<td><img src="https://user-images.githubusercontent.com/38023004/122553526-c0893a00-d072-11eb-9b67-bf663ba34a5a.png"></td>
<td><img src="https://user-images.githubusercontent.com/38023004/122553849-2b3a7580-d073-11eb-84dc-cfc9964e9bce.png"></td>
</tr>
</table>

## 📸 Setup
[Install Pipenv](https://pipenv.pypa.io/en/latest/install/) and then
```
$ pipenv sync
```

You can also manually pip install the libraries you need.

## 📸 Quick Start

```
$ pipenv shell
$ python gui_screencapture.py
```
## 📸 Quick Start for CUI Lovers
```
$ pipenv shell
$ python screencapture.py test-directory
```

## 📸 Caution
The developer of this program is not responsible for any problems that may arise from the use of this program. If you have an important class or presentation where you cannot miss a single page of slides, please consider carefully whether to use this program.

## 📸 Tips
### Screenshot of Sub-display
If you want to take a screenshot of the sub-display, set "--display" to 2. If you are using more than two displays, you may need to set it to an integer greater than 2. Try using the program a few times to see which numbers correspond to which displays.

### Suspending and Resuming Program
Interrupting the program will not erase the saved screenshot file. The program will display "Interruption can corrupt your data!", but this is a problem with the framework we are using for development, so don't worry about it. If your saved file disappears, please [contact me](https://twitter.com/rita_rita_ritan).

If you save the screenshot again in the same directory, the file name number will be assigned to follow the end of the previous screenshot file.

### Turn Off Slide Page-Turning Detection
If you want to turn off the slide page-turning detection and save screenshots of all times, set "--similarity_tolerance" to a negative number such as -1.

### Reduce Number of Screenshots for Video Part
If you want to reduce the number of screenshots only for the video part, set "--movie_interval" to an integer greater than or equal to 2. The larger the value, the longer the interval between saving screenshots. However, this feature is still in beta, so it may not work properly.

### Very Short Intervals
If the value of "--interval" is very small, the program may not work properly. It is recommended that you do not make it smaller than the default value.

## 📸 CUI Usage

```
usage: screencapture.py [-h] [-i INTERVAL] [-t TIMEOUT]
                        [-s SIMILARITY_TOLERANCE] [-d DISPLAY]
                        [-m MOVIE_INTERVAL]
                        directory

positional arguments:
  directory             Directory where screenshots will be saved. If the
                        specified directory does not exist, a new directory
                        will be created.

optional arguments:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        Time interval for taking a screenshot. default=4
  -t TIMEOUT, --timeout TIMEOUT
                        Time to keep taking screenshots (minutes). default=120
  -s SIMILARITY_TOLERANCE, --similarity_tolerance SIMILARITY_TOLERANCE
                        Maximum value of the Hamming distance at which two
                        screenshots are considered to be similar. The larger
                        this value is, the more likely it is that the same
                        page of slides will be saved multiple times. default=5
  -d DISPLAY, --display DISPLAY
                        Display where the screenshot will be taken. 1 is main,
                        2 secondary, etc. default=1
  -m MOVIE_INTERVAL, --movie_interval MOVIE_INTERVAL
                        (beta) Time interval to save the video. For example, 1
                        if it is the same as the interval of time to take a
                        screenshot, and 2 if it is twice as long. This option
                        is still in beta, so it may not work properly for you.
                        default=1

```

## 📸 TODO
I don't know if I'll actually work on it, but here are some things I think could be improved about this program
* Distribution in the form of an application that launches when clicked
* Improving page-turning detection accuracy.
* Verification of the video detection function