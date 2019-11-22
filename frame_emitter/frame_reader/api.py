import os

from frame_reader import frame_reader


class FrameAPIReader(frame_reader.FrameReader):
    def __init__(self):
        print("API based frame reader created, pid = %d" % os.getpid())
