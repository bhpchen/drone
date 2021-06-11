import numpy as np
import cv2
from time import time as timer
import sys
import math
'''
def cut_video(video_filename):
    video = cv2.VideoCapture(video_filename)
    print("start")
    fps = video.get(cv2.CAP_PROP_FPS)
    print('fps:',fps)
    fps /= 30
    framerate = timer()
    elapsed = int()

    i = 1
    while(video.isOpened()):
        start = timer()
        ret, frame = video.read()
        if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
            break
        elapsed += 1
        print(f'Real frames: {elapsed}')
        video_name = video_filename.split('.')[0]
        if elapsed % 6 == 0:#and elapsed > 3000:
            cv2.imwrite(f"{video_name}/{i}.jpg",frame)
            print(f'image nunmber: {i}')
            i+=1
        

    video.release()
    cv2.destroyAllWindows()
'''



def calculate_time(fps,elapsed):
	total_second = math.floor(elapsed/fps)
	hour = math.floor(math.floor(total_second/60)/60)
	minute = math.floor(total_second/60) - hour * 60 
	second = total_second - minute * 60
	return hour,minute,second

def cut_video(video_filename):
    #video_filename = "drone_videos/drone_1.mp4"
    video = cv2.VideoCapture(video_filename)
    print("start")
    fps = video.get(cv2.CAP_PROP_FPS)
    print('fps:',math.ceil(fps))
    #fps /= 30
    framerate = timer()
    elapsed = int()


    i = 1
    while(video.isOpened()):
        start = timer()
        ret, frame = video.read()
        if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
            break
        elapsed += 1
        print(f'Real frames: {elapsed}')
        video_name = video_filename.split('.')[0]
        print(video_name)
        if elapsed % 6 == 0:#and elapsed > 3000:
            hour,minute,second = calculate_time(fps,elapsed)
            cv2.imwrite(f"{video_name}/{hour}_{minute}_{second}.jpg",frame)
            print(f'image number: {i}')
            i+=1


    video.release()
    cv2.destroyAllWindows()