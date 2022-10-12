import cv2
import pyaudio
import pygame
import threading
import time
import wave

import lib.constants as c
from lib.image_utils import opencv_to_pyg

pygame.mixer.init()

class PlayStates(object):
    STOPPED = 0
    PLAYING = 1


class RecordedVideo(object):
    """
        Used to playback AV from previous recordings.

        This component does not self destruct.  When the video finishes playing,
        the last frame of the video is displayed until `.close()` is called
    """

    def __init__(self, surface, video_file, audio_file, on_playback_complete=None):
        self.surface = surface
        self.video_file = video_file
        self.audio_file = audio_file
        self.on_playback_complete = on_playback_complete

        self.has_closed = False

        self.play_state = PlayStates.STOPPED
        self.last_frame = None

        self.video_thread = None

        self.start_playback()

    def __del__(self):
        self.close()

    def start_playback(self):
        mixer = pygame.mixer

        if not self.has_closed:
            self.play_state = PlayStates.PLAYING
            print(f"recorded_video: creating video thread")
            self.video_thread = threading.Thread(target=self._video_thread)

            print(f"recorded_video: loading audio file")
            mixer.music.load(self.audio_file)
            mixer.music.set_volume(.9)


            print(f"recorded_video: starting async audio playback")
            self.video_thread.start()
            time.sleep(1)
            mixer.music.play()


    def stop_playback(self):
        if self.play_state == PlayStates.PLAYING:
            self.play_state = PlayStates.STOPPED
            mixer.music.stop()



    # needs to be called externally.  This component doesn't self destruct
    def close(self):
        if hasattr(self, 'has_closed') and not self.has_closed:
            self.has_closed = True
            self.stop_playback();


    def render(self, t):
        if self.has_closed:
            return False

        if self.last_frame:
            self.surface.blit(self.last_frame, (0, 0))

        return True

    # video capture thread is always running from init to close()
    def _video_thread(self):
        print("recorded_video: _video_thread starting")

        t_load_start = time.time()
        video = cv2.VideoCapture(self.video_file)
        fps = video.get(cv2.CAP_PROP_FPS)

        clock = pygame.time.Clock()

        while not self.has_closed and self.play_state == PlayStates.PLAYING:
            success, video_image = video.read()
            if not success:
                break;
            self.last_frame = opencv_to_pyg(video_image)
            clock.tick(fps)

        print("recorded_video: _video_thread stopping")
        video.release()

        self.video_thread = None
        self.play_state = PlayStates.STOPPED
        callable(self.on_playback_complete) and self.on_playback_complete()



