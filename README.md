# AutoScreenCapture
AutoScreenCapture is a multi-platform program that automatically takes screenshots for you. 

This program, originally intended to take screenshots of classes with slides, can prevent you from saving the same page of slides over and over again.

## Setup
Install pipenv and then
```
$ pipenv install
```

You can also manually pip install the libraries you need.

## Quick Start

```
$ pipenv shell
$ python screencapture.py test-directory
```

## Usage


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