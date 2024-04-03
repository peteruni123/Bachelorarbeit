import numpy as np
import tensorflow as tf
import cv2
import threading
from tensorflow.keras.models import load_model
import datetime
import BasicClasses as bc
import time

class MLThread(threading.Thread):

    #Initalisierung des Threads
    def __init__(self, val_queue : bc.PeterQueue, val_queue2 : bc.PeterQueue, val_queue3 : bc.PeterQueue, log_queue: bc.PeterQueue):
        super().__init__(target=self.check_update, args=())
        self.myImgQueue = val_queue
        self.myResultQueueDB = val_queue2
        self.myResultQueueGUI = val_queue3
        self.evShouldStop = threading.Event()
        self.new_model = load_model('models/imageclassifier.h5')
        self.log_queue = log_queue
        self.closed = False
        

    #Mainloop des Threads hier wird gepüft ob sich ein Item in der Img-Queue befindet,
    # falls dies der Fall ist wird die analyse begonnen
    def check_update(self):
        while not self.evShouldStop.is_set():
            needed_update = not self.myImgQueue.empty()
            while not self.myImgQueue.empty():
                #--------------------------------
                item = self.myImgQueue.get()

                if item.stageIdx == 0:
                    self.callback(1,item)
                self.myImgQueue.task_done()
                #------------------------------
            if needed_update:
                time.sleep(1)
            else:
                time.sleep(1) 
        self.closed = True


    # Hier wird das Bild analysiert und das Ergebnis in die Queue für die GUI und die Datenbank eingereiht
    def callback(self,item):
        #Vorbereitungen
        self.log_queue.put(bc.LogMsg("ML: Bild wird analysiert"))
        RGB_img = cv2.cvtColor(item.valimage, cv2.COLOR_BGR2RGB)
        resize = tf.image.resize(RGB_img, (256,256))
        resize = tf.cast(resize,'int64')
        #Prediction
        yhat = self.new_model.predict(np.expand_dims(resize/255, 0))

        #Ergebnis formattieren
        yhat_new = [i * 100 for i in yhat]
        np.set_printoptions(suppress=True)
        self.log_queue.put(bc.LogMsg("ML: Ergebnisse werden ausgewertet und in die Ergebnis-Queue geschrieben"))
        yhat_new[0] = np.round(yhat_new[0],2)
        max_index = np.argmax(yhat_new[0])

        #Ergebnis auswerten
        if yhat_new[0][max_index] < 65:

            if (max_index == 0 or max_index== 1) and ((yhat_new[0][0] + yhat_new[0][1]) > 80) :
                self.res_str = "This Wafer is mixed but it is dark"
                SQL_string = "Md"

            elif (max_index == 2 or  max_index == 3) and ((yhat_new[0][2] + yhat_new[0][3]) > 80) :
                self.res_str = "This Wafer is mixed but it is light"
                SQL_string = "Ml"

            else:
                self.res_str = "This Wafer is mixed and doesnt fit categorie"
                SQL_string = "no fit"

        elif max_index == 0 :
            self.res_str = "The Wafer is Darkblue"
            SQL_string = "Db"

        elif max_index == 1 :
            self.res_str = "The Wafer is DarkDarkblue"
            SQL_string = "Ddb"
        
        elif max_index == 2 :
            self.res_str = "The Wafer is Lightblue"
            SQL_string = "Lb"

        elif max_index == 3 :
            self.res_str = "The Wafer is LightLightblue"
            SQL_string = "Llb"
        else:
            self.res_str = "An Error has Occured check Code oder ImageFile"
            SQL_string = "Error"


        #Ergebnis in die Queues schreiben
        now = datetime.datetime.now()
        Zeitstempel = now.strftime("%m/%d/%Y, %H:%M:%S")

        result = bc.ResultImage()
        result.valID = item.valText
        result.valResult = SQL_string
        result.valTimestemp = Zeitstempel
        result.CamIndex = item.CamIndex
        
        self.myResultQueueDB.put(result)
        self.myResultQueueGUI.put(result)
        self.myResultQueueDB.fullhandling()
        self.myResultQueueGUI.fullhandling()
        

    #Thread stoppen
    def stopTask(self):
        self.evShouldStop.set()