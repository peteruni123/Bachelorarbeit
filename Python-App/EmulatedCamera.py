import threading
import BasicClasses as bc
import os
import cv2

class EmulatedCameraClass():

    #Initialisierung des Kamera-Objekts
    def __init__(self, pathToImgs):
        self.evImgAcquiered = threading.Event()
        #--------------------------------------------
        self.isTriggering = threading.Event()
        #--------------------------------------------
        self.lockImage = threading.Lock()
        self.VisImg = bc.VisImage()
        #--------------------------------------------
        self.pathToImgs = pathToImgs
        self.files = []
        self.fIdx = 0

    #Bilderdatei Namen in Array speichern
    def open(self):
        self.files = [file for file in os.listdir(self.pathToImgs) if file.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        self.fIdx = 0

    def close(self):
        pass
    
    #Trtigger wird gestartet und ruft imageAcquisition auf
    def executeTrigger(self):
        if (self.isTriggering.is_set()):
            pass
        else:
            try:
                self.evImgAcquiered.clear()
                self.isTriggering.set()
                self.imageAcquisition()
                self.evImgAcquiered.set()
                self.isTriggering.clear()
            finally:
                pass
                
    #Nimmt Bild aus dem in self.files[self.index] angegebenem Dateipfad und erhöht Index
    def imageAcquisition(self):
            self.VisImg = bc.VisImage()
            self.VisImg.valText = self.files[self.fIdx]
            self.fIdx = self.fIdx + 1 if self.fIdx < len(self.files)-1 else 0
            self.VisImg.valimage = cv2.imread(os.path.join(self.pathToImgs, self.VisImg.valText))
            self.VisImg.CamIndex = 0
            print(os.path.join(self.pathToImgs, self.VisImg.valText))
            

        