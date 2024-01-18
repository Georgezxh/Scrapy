from moviepy.editor import *

video = VideoFileClip('C:\\Users\\zxh\\Videos\\a.mp4')# 本地视频路径
audio = video.audio
audio.write_audiofile('test.mp3')#生成的音频

