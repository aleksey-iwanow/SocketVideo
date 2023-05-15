import cv2
import os

image_folder = 'video'
video_name = 'video.avi'

images = [f'image{i}.png' for i in range(len(os.listdir(image_folder)))]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 17, (width,height))
#                                     (fps)
for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()