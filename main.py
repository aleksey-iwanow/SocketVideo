import socket as Socket
import sys
import pickle
import os

import PIL
import pygame
import io
import base64
import PIL.Image as Image


class Server:
    def __init__(self, address, port, dataPackageSize, dataClosingSequence, encoding):
        self.socket = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)
        self.socket.bind((address, port)), self.socket.listen(1)

        self.w, self.h = 900, 675
        self.index_ = 0

        self.dataPackageSize = dataPackageSize
        self.dataClosingSequence = dataClosingSequence
        self.encoding = encoding
        self.dataBytes = None
        self.mx = None
        self.folder_ = "video"
        # str(self.cl.get_fps())
        pygame.init()
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.screen.fill((0, 0, 0))
        self.cl = pygame.time.Clock()
        self.font_ = pygame.font.Font("fonts/CatV.ttf", 20)
        self.text_render = self.font_.render(f'None recording...', True, (141, 141, 141))
        text_rect = self.text_render.get_rect(center=(self.w // 2, self.h // 2))
        self.screen.blit(self.text_render, text_rect)
        pygame.display.flip()
        self.connection, self.clientAddress = self.socket.accept()
        self.update()

    def update(self):
        self.clear_folder()
        while self.check_active():
            self.listenClients()

    def check_active(self):
        return True  # пока что

    def clear_folder(self):
        filelist = [f for f in os.listdir(self.folder_)]
        for f in filelist:
            os.remove(os.path.join(self.folder_, f))

    def sender(self, user, text):
        user.send(text.encode(self.encoding))

    def listenClients(self):
        # self.sender(self.connection, "")

        self.dataBytes = self.connection.recv(self.dataPackageSize)

        if self.dataBytes:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    sys.exit()
            self.cl.tick(30)
            try:
                '''with open("my_file.wav", "wb") as binary_file:
                    binary_file.write(self.dataBytes)

                self.mx = pygame.mixer.Sound("my_file.wav")
                self.mx.play(maxtime=1000)'''
                img = Image.open(io.BytesIO(self.dataBytes))
                img.save(f'{self.folder_}/image{self.index_}.png')
                self.screen.fill((0, 0, 0))
                image_ = pygame.image.load(f'video/image{self.index_}.png')
                image_ = pygame.transform.scale(image_, (self.w, int(image_.get_size()[1] * (self.w / image_.get_size()[0]))))
                self.screen.blit(image_, (0, 0))
            except PIL.UnidentifiedImageError:
                pass
            self.text_render = self.font_.render(f'FPS: {round(self.cl.get_fps(), 2)}', True, (103,208,47))
            self.screen.blit(self.text_render, (10, 10))
            pygame.display.set_caption("CCTV")
            pygame.display.flip()

            self.index_ += 1

        else:
            print('байтов нема')


if __name__ == "__main__":
    server = Server("192.168.0.246",
                    22021,
                    1024*1024*10,
                    b"\r\n\r\n",
                    "utf-8")
