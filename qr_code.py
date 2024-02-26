import cv2
import threading
from pyzbar.pyzbar import decode

class BarcodeReader:
    def __init__(self):
        url = "http://10.42.0.118:4747/video"
        self.cap = cv2.VideoCapture(url)
        self.stopped = False

    def start(self):
        threading.Thread(target=self.read_barcodes).start()

    def read_barcodes(self):
        while not self.stopped:
            ret, frame = self.cap.read()
            if ret:
                barcodes = decode(frame)
                for barcode in barcodes:
                    x, y, w, h = barcode.rect
                    barcode_text = barcode.data.decode('utf-8')
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cv2.putText(frame, barcode_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                    print("Barcode:", barcode_text)

                cv2.imshow('Barcode/QR code reader', frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    self.stop()

    def stop(self):
        self.stopped = True
        self.cap.release()
        cv2.destroyAllWindows()

def main():
    barcode_reader = BarcodeReader()
    barcode_reader.start()

if __name__ == '__main__':
    main()
