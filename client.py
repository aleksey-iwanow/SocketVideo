import socket as Socket
import pyautogui
import cv2
import pickle
import PIL.Image as Image
import pyaudio
import wave
import time


def read_audio():

    # Record in chunks of 1024 samples
    chunk = 1024

    # 16 bits per sample
    sample_format = pyaudio.paInt16
    chanels = 2

    # Record at 44400 samples per second
    smpl_rt = 44400
    seconds = 1
    filename = "path_of_file.wav"

    # Create an interface to PortAudio
    pa = pyaudio.PyAudio()

    stream = pa.open(format=sample_format, channels=chanels,
                     rate=smpl_rt, input=True,
                     frames_per_buffer=chunk)

    # Initialize array that be used for storing frames
    frames = []

    # Store data in chunks for 8 seconds
    for i in range(0, int(smpl_rt / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate - PortAudio interface
    pa.terminate()

    # Save the recorded data in a .wav format
    sf = wave.open(filename, 'wb')
    sf.setnchannels(chanels)
    sf.setsampwidth(pa.get_sample_size(sample_format))
    sf.setframerate(smpl_rt)
    sf.writeframes(b''.join(frames))
    sf.close()


socket = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)
socket.connect(("192.168.0.246", 22021))  # 192.168.233.88   192.168.0.246  192.168.137.44
cam_port = 0
cam = cv2.VideoCapture(cam_port)
sz = 1024*1024*10
start_time = time.time()
old_time = start_time

while True:
    result, image = cam.read()

    if result:
        # pyautogui.screenshot('image_server.png')
        cv2.imwrite("image_server.png", image)
        im = Image.open("image_server.png")
        im2 = im.resize((300, 225))
        im2.save('image_server.png')
        file = open('image_server.png', mode="rb")

        data = file.read(sz)
        socket.sendall(data)
        file.close()

        old_time = time.time()

