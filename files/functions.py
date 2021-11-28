from .videos import *
import ffmpeg
import subprocess
import os
import re
import tempfile


DURATION = re.compile(r'(?<=Duration: )(\d{2}):(\d{2}):(\d{2}.\d+)(?=, start)')
RESOLUTION = re.compile(r'(?<=, )(\d+)x(\d+)')
FPS = re.compile(r'\d+(?= fps)')
TEMPS = []


def add_video(filename, name):
    stream = ffmpeg.input(filename)
    commands = ['ffmpeg', '-i', filename]
    data, errs = subprocess.\
        Popen(commands, stderr=subprocess.PIPE, shell=True).communicate()
    errs = errs.decode()
    duration = DURATION.search(errs)
    duration = 60 * (60 * float(duration.group(1))
                     + float(duration.group(2))) + float(duration.group(3))
    resolution = RESOLUTION.search(errs)
    width = int(resolution.group(1))
    height = int(resolution.group(2))
    fps = FPS.search(errs)
    fps = int(fps.group(0))
    video = Video(filename, stream.video, stream.audio,
                  width, height, fps, duration)
    VIDEOS[name] = video


def crop(name, x, y, width, height, new_name):
    new_stream = ffmpeg.crop(VIDEOS[name].stream_v, x, y, width, height)
    video = Video(new_name + ".mp4", new_stream, VIDEOS[name].stream_a,
                  width, height, VIDEOS[name].fps, VIDEOS[name].duration)
    VIDEOS[new_name] = video


def output(name):
    try:
        ffmpeg.output(VIDEOS[name].stream_v, VIDEOS[name].stream_a,
                      VIDEOS[name].filename).run()
        return True
    except ffmpeg._run.Error:
        return False


def concat(first_name, second_name, new_name):
    video_1 = VIDEOS[first_name]
    video_2 = VIDEOS[second_name]
    width = max(video_1.width, video_2.width)
    height = max(video_1.height, video_2.height)
    if output(first_name):
        TEMPS.append(first_name)
    if output(second_name):
        TEMPS.append(second_name)
    with tempfile.NamedTemporaryFile(dir="temp", suffix=".mp4") as file_1:
        name_1 = os.path.join('temp', file_1.name)
    args = ['ffmpeg', '-i', video_1.filename, '-vf', 'scale=' + str(width)
            + ':' + str(height), name_1]
    subprocess.call(args)
    stream_1 = ffmpeg.input(name_1)
    with tempfile.NamedTemporaryFile(dir="temp", suffix=".mp4") as file_2:
        name_2 = os.path.join('temp', file_2.name)
    args = ['ffmpeg', '-i', video_2.filename, '-vf', 'scale=' + str(width)
            + ':' + str(height), name_2]
    subprocess.call(args)
    stream_2 = ffmpeg.input(name_2)
    stream_v = ffmpeg.concat(stream_1.video,
                             stream_2.video)
    stream_a = ffmpeg.concat(video_1.stream_a,
                             video_2.stream_a, v=0, a=1)
    video = Video(new_name + ".mp4", stream_v, stream_a,
                  width, height,
                  max(VIDEOS[first_name].fps, VIDEOS[second_name].fps),
                  VIDEOS[first_name].duration + VIDEOS[second_name].duration)
    VIDEOS[new_name] = video
    TEMPS.append(name_1)
    TEMPS.append(name_2)


def get_info(video):
    video = VIDEOS[video]
    print("filename: {0}\nwidth: {1}\nheight: {2}\nfps: {3}\nduration: {4} sec"
          .format(video.filename, video.width, video.height, video.fps,
                  video.duration))


def change_speed(videoname, mult, new_name):
    video = VIDEOS[videoname]
    pts = str(1/mult) + "*PTS"
    stream_v = ffmpeg.setpts(video.stream_v, pts)
    stream_a = video.stream_a.filter_('asetpts', pts)
    result_video = Video(new_name + ".mp4", stream_v, stream_a, video.width,
                         video.height, video.fps, video.duration / mult)
    VIDEOS[new_name] = result_video


def trim(videoname, start, end, new_name):
    start = start.split(':')
    end = end.split(':')
    start = 60*(60*int(start[0]) + int(start[1])) + int(start[2])
    end = 60*(60*int(end[0]) + int(end[1])) + int(end[2])
    video = VIDEOS[videoname]
    stream_v = ffmpeg.trim(video.stream_v, start=start, end=end)
    stream_v = ffmpeg.setpts(stream_v, 'PTS-STARTPTS')
    stream_a = video.stream_a.filter_("atrim", start=start, end=end)
    VIDEOS[new_name] = Video(new_name + '.mp4', stream_v, stream_a,
                             video.width, video.height, video.fps, end - start)


def clear_temps():
    for i in TEMPS:
        os.remove(i)
