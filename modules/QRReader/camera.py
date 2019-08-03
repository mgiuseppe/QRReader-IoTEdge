import io
import picamera
from PIL import Image
from time import sleep

class Camera():

    def Capture(self, camera_delay):
        # crea uno stream dati in memoria
        stream = io.BytesIO()

        #  visualizzazione dello streaming della camera
        with picamera.PiCamera() as camera:
            camera.exposure_mode = 'auto'
            camera.preview_fullscreen = False
            # ridimensiono il preview per poter interrompere in caso di problemi
            camera.preview_window = (300, 200, 640, 480)
            camera.start_preview()
            sleep(camera_delay)  # aumentare se si vuole inquadrare meglio
            camera.capture(stream, format='jpeg')

        # recupera tutto il flusso per creare l'immagine
        stream.seek(0)
        pil = Image.open(stream)

        # mode "L" = 8-bit pixels, black and white
        # recupera i byte dell'immagine
        pil = pil.convert('L')
        width, height = pil.size
        raw = pil.tobytes()

        return (width, height, raw)