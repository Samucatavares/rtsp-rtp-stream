class VideoStream:
    FRAME_HEADER_LENGTH = 5
    DEFAULT_IMAGE_SHAPE = (380, 280)
    VIDEO_LENGTH = 500
    DEFAULT_FPS = 24

   #
    # it's the last chunk for current jpeg (end of frame)
    JPEG_EOF = b'\xff\xd9'

    def __init__(self, file_path: str):
        # o mjpeg foi aceito como o arquivo do diretório.
        self._stream = open(file_path, 'rb') #rb significa que o arquivo é leitura+escrita e binário
        # frame number is zero-indexed
        # after first frame is sent, this is set to zero
        self.current_frame_number = -1

    def close(self):
        self._stream.close()

    def get_next_frame(self) -> bytes:
        #a amostra de video tem um formato de inteiros de 5 digítod, escritos como 5 bytes, um para cada digito, aç´rm do tamanho de frames, isso repetindo até o END OF frame.
        # sample video file format is as follows:
        # - 5 digit integer `frame_length` written as 5 bytes, one for each digit (ascii)
        # - `frame_length` bytes follow, which represent the frame encoded as a JPEG
        # - repeat until EOF
        try:
            frame_length = self._stream.read(self.FRAME_HEADER_LENGTH)
        except ValueError:
            raise EOFError
        frame_length = int(frame_length.decode())
        frame = self._stream.read(frame_length)
        self.current_frame_number += 1
        return bytes(frame)
