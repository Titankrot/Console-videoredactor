VIDEOS = dict()


class Video:
    def __init__(self, filename, stream_v, stream_a,
                 width, height, fps, duration):
        self.filename = filename
        self.stream_v = stream_v
        self.stream_a = stream_a
        self.width = width
        self.height = height
        self.fps = fps
        self.duration = duration
