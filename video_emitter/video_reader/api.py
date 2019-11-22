import os

from video_reader import video_reader


class VideoPacketAPIReader(video_reader.VideoPacketReader):
    def __init__(self):
        print("API based video packet reader created, pid = %d" % (os.getpid()))
