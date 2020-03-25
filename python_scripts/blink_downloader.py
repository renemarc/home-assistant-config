#!/bin/python
"""
Blink camera latest image downloader

This command-line script continuously polls Blink for a video created in the
last 60 seconds (arg --offset) for any device or a speficis one (arg --device).
Once found, the video is downloaded.

Based on Dullage's script:
https://github.com/Dullage/Home-AssistantConfig/blob/master/config/python_scripts/blink.py
"""
import argparse
import json
import os
import re
import time
from datetime import datetime, timedelta

import yaml
from blinkpy import api, blinkpy

# Extract command-line arguments.
parser = argparse.ArgumentParser()
parser.add_argument("--camera", help="Camera to fetch")
parser.add_argument(
    "--output", default="camera.blink_{DEVICENAME}", help="File name format",
)
parser.add_argument("--username", help="Blink username")
parser.add_argument("--password", help="Blink password")
parser.add_argument(
    "--secrets", default="/config/secrets.yaml", help="Secrets file",
)
parser.add_argument(
    "--secrets_username",
    default="blink_username",
    help="Blink username variable in secrets file",
)
parser.add_argument(
    "--secrets_password",
    default="blink_password",
    help="Blink password variable in secrets file",
)
parser.add_argument(
    "--offset", type=int, default=60, help="Offset in seconds",
)
parser.add_argument(
    "--timeout", type=int, default=60, help="Timeout in seconds",
)
parser.add_argument("--destination", default=".", help="Save path")
parser.add_argument(
    "--debug", action="store_true", help="Save matched list of videos to file"
)
args = parser.parse_args()

# Connect to Blink server.
if args.username and args.password:
    USERNAME = args.username
    PASSWORD = args.password
else:
    with open(args.secrets, "r") as secrets_file:
        secrets = yaml.load(secrets_file, Loader=yaml.BaseLoader)
    USERNAME = secrets[args.secrets_username]
    PASSWORD = secrets[args.secrets_password]
blink = blinkpy.Blink(username=USERNAME, password=PASSWORD)
blink.start()

# Fetch list of latest videos.
from_time = time.time() - args.offset
loop_start = datetime.today()
while True:
    videos = api.request_videos(blink, time=from_time)["media"]

    if args.camera:
        videos_device = []
        for video in videos:
            if video.get("device_name") == args.camera:
                videos_device.append(video)
        videos = videos_device

    if videos:
        break

    if datetime.today() >= (loop_start + timedelta(seconds=args.timeout)):
        break

    time.sleep(1)

if args.debug:
    with open("videos.json", "w") as f:
        f.write(json.dumps(videos, indent=4))

# Find and download the first video
if videos:
    # Use the first video in the list.
    video = videos[0]
    video_address = "{}{}".format(blink.urls.base_url, video.get("media"))

    response = api.http_get(blink, url=video_address, stream=True, json=False)

    OUTPUT_FILENAME = args.output
    DEVICE_NAME = video.get("device_name").lower()
    DEVICE_NAME = re.sub(r"[^a-z0-9]+", "-", DEVICE_NAME).strip("-")
    DEVICE_NAME = re.sub(r"--+", "-", DEVICE_NAME)
    filename = OUTPUT_FILENAME.format(DEVICENAME=DEVICE_NAME)
    VIDEO_FILE = os.path.join(args.destination, "{}.mp4".format(filename))

    with open(VIDEO_FILE, "wb") as video_file_content:
        video_file_content.write(response.content)

