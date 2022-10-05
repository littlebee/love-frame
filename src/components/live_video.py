import cv2
import pyaudio
import threading
import time
import wave

from lib.image_utils import opencv_to_pyg


CAPTURE_FPS = 30
FRAME_SIZE = (1280, 720)
RAW_VIDEO_FILE = "data/raw.mp4"

AUDIO_CHUNK = 1024  # Record in chunks of 1024 samples
AUDIO_SAMPLE_FORMAT = pyaudio.paInt16  # 16 bits per sample
AUDIO_CHANNELS = 2
# AUDIO_RATE = 44100  # Record at 44100 samples per second
# 44100 causes pyaudio to freak if using sudo. R    oot has a lower sample rate?
AUDIO_RATE = 32000
RAW_AUDIO_FILE = "data/raw.wav"


class LiveVideo(object):

    def __init__(self, screen):
        self.screen = screen
        self.has_closed = False

        # start the capture
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_SIZE[0])
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_SIZE[1])
        camera.set(cv2.CAP_PROP_FOURCC,
                   cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        camera.set(cv2.CAP_PROP_FPS, CAPTURE_FPS)
        self.camera = camera

        self.audio = pyaudio.PyAudio()  # Create an interface to PortAudio

        self.last_frame = None
        # this thread is running until we are closed and is responsible
        # for setting self.last_frame with either the last frame captured
        # from the camera or the current frame of playback
        self.video_thread = threading.Thread(
            target=self._video_thread)
        self.video_thread.start()

        # this thread is instantiated at record() to capture audio
        self.recording_thread = None

        self.recording_started_at = None
        self.recording_duration = 0
        self.recorded_video_frames = []
        self.recorded_audio_frames = []

    def __del__(self):
        self.close()

    # needs to be called externally.  This component doesn't self destruct
    def close(self):
        if not self.has_closed:
            self.has_closed = True
            self.video_thread.join()
            self.camera.release()

    # record() needs to be async
    def record(self, duration):
        self.recording_duration = duration
        self.recorded_video_frames = []
        self.recorded_audio_frames = []

        self.recording_thread = threading.Thread(
            target=self._recording_thread)
        self.recording_thread.start()

    def render(self, t):
        if self.has_closed:
            return False

        if self.last_frame:
            self.screen.blit(self.last_frame, (0, 0))

        return True

    # video capture thread is always running from init to close()
    def _video_thread(self):
        print("_video_thread starting")

        frame_buffer = []
        while not self.has_closed:
            ret, frame = self.camera.read()
            self.last_frame = opencv_to_pyg(frame)
            if self.recording_started_at != None and time.time() - self.recording_started_at < self.recording_duration:
                frame_buffer.append(frame)
            elif len(frame_buffer) > 0:
                self.recorded_video_frames = frame_buffer
                self.recording_started_at = None
                frame_buffer = []

        print("_video_thread stopping")

    # audio capture thread is started by record() and runs for
    # self.recording_duration
    def _recording_thread(self):
        print("_recording_thread starting")

        # tell the already running video thread to start saving frames
        self.recording_started_at = time.time()

        self._record_audio()
        self._save_raw_audio()

        # video thread should be long done saving frames
        self._save_raw_video()
        print("_recording_thread finished")

    # synchronous
    def _record_audio(self):
        duration = self.recording_duration
        stream = self.audio.open(format=AUDIO_SAMPLE_FORMAT,
                        channels=AUDIO_CHANNELS,
                        rate=AUDIO_RATE,
                        frames_per_buffer=AUDIO_CHUNK,
                        input=True)

        audio_frames = []

        # Store data in chunks for 20 seconds
        for i in range(0, int(AUDIO_RATE / AUDIO_CHUNK * duration)):
            data = stream.read(AUDIO_CHUNK)
            audio_frames.append(data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        self.audio.terminate()

        self.recorded_audio_frames = audio_frames

    def _save_raw_audio(self):
        print(f"saving audio to {RAW_AUDIO_FILE}")
        t_start = time.time()
        # now save the audio frames to a .wav
        wf = wave.open(RAW_AUDIO_FILE, 'wb')
        wf.setnchannels(AUDIO_CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(AUDIO_SAMPLE_FORMAT))
        wf.setframerate(AUDIO_RATE)
        wf.writeframes(b''.join(self.recorded_audio_frames))
        wf.close()

        print(f"saved audio to {RAW_AUDIO_FILE} in {time.time() - t_start}s")

    def _save_raw_video(self):
        print(
            f"saving file {RAW_VIDEO_FILE} - {len(self.recorded_video_frames)} frames")

        capture_fps = len(self.recorded_video_frames) / self.recording_duration
        t_start = time.time()
        writer = cv2.VideoWriter(
            RAW_VIDEO_FILE,
            cv2.VideoWriter_fourcc(*'mp4v'),
            capture_fps,
            FRAME_SIZE,
        )
        for frame in self.recorded_video_frames:
            writer.write(frame)

        writer.release()
        print(
            f"saved file {RAW_VIDEO_FILE} in {time.time() - t_start}s")
