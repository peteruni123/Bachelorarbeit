import BasicClasses as bc
import threading
import time
import queue
import pyads
import ADS_Comm 
import EmulatedCamera

#Dieser Thread dient der Überwachung einer Kamera er liest die Trigger, 
#setzt die Kamera auf busy und gibt sie auch wieder frei(WriteIsDone, WritePicturevalid)
class VisionTaskClass(threading.Thread):

    #Initialisierung des Threads
    def __init__(self, val_queue  : queue.Queue, pathToImgs :str, log_queue: bc.PeterQueue, index):
        super().__init__(target=self.do_run, args=())
        self.shouldStop = threading.Event()
        self.myCam = EmulatedCamera.EmulatedCameraClass(pathToImgs)
        self.lock = threading.Lock()
        self.resetStates()
        self.log_queue = log_queue
        self.closed = False
        self.index = index
        #--------------
        self.taskLock = threading.Lock()
        self.myQueue = val_queue


    #Diese Funktion wird genutzt um die wichtigen Statuswerte wieder zurückzusetzten
    def resetStates(self, val_isConn = False):
        try:
            self.lock.acquire()
            self.isBusy = False
            self.isTrigger = False
            self.isConnected = val_isConn
        finally:
            self.lock.release()


    #Diese Funktion schaut ob die Kamera in der SPS einen Trigger erhalten hat,
    # falls dies der Fall ist wird self.isTrigger auf true gesetzt
    def readTrigger(self):
        if ((not self.isBusy) and ADS_Comm.ReadTrigger(self.plc,self.index)):  
            self.isTrigger = True
            self.log_queue.put(bc.LogMsg(f"{self.name}: Trigger von der SPS gelesen"))
            

    #Falls ein Trigger gelesen wurde und die Verbindung da ist wird die Kamera auf Busy gesetzt
    #  und True zurückgegeben andernfalls False          
    def startTrigger(self):
        if self.isConnected and self.isTrigger:
            self.log_queue.put(bc.LogMsg(f"{self.name}: Starting Trigger"))
            #---------------------------
            self.isBusy = True
            ADS_Comm.WriteBusy(self.plc, self.index, True)
            return True
        return False
    

    #Nachdem der Trigger ausgeführt wurde wird er wieder beendet und
    # es werden die entsprechenden Stati in die SPS geschrieben
    def endTrigger(self):
        if self.isConnected and self.isTrigger:
            #----------------------------
            self.isBusy = False
            self.isTrigger = False
            ADS_Comm.WritePictureValid(self.plc, self.index, True)
            ADS_Comm.WriteIsDone(self.plc, self.index, True)
            ADS_Comm.WriteBusy(self.plc, self.index, False)
            ADS_Comm.WriteTrigger(self.plc, self.index, False)
            self.log_queue.put(bc.LogMsg(f"{self.name}: Ending Trigger"))
            return True
        return False


    #Hier wird die Kamera geöffnet und die Verbindung zu der SPS etabliert
    # Außerdem wird der Kameraname aus der SPS ausgelesen
    def prepareTask(self):
        self.myCam.open()
        self.log_queue.put(bc.LogMsg("Kamera ?: Connecting to SPS"))
        self.plc = pyads.Connection('xxx.xx.xx.xx.x.x', pyads.PORT_TC3PLC1)
        self.plc.open()
        self.isConnected = True
        self.name = ADS_Comm.ReadName(self.plc,self.index)
        self.log_queue.put(bc.LogMsg(f"{self.name}: Connected to SPS Adress: " +str({self.plc.get_local_address()})))
        
        
    #Wird bei Beendung des Threads aufgerufen und schließt  die Kamera und die Verbindung zu der SPS
    def exitTask(self):
        self.plc.write_by_name(".Python_Checker.Python_Active",False)
        self.myCam.close()
        self.plc.close()
        self.isConnected = False
        self.closed = True


    #Diese Funktion ist der mainloop des Threads und befinden sich solange im while Loop bis die Applikation gestoppt wird
    #Wurde ein Trigger gelesen wird die Emulierte Kamera aktiviert und gibt ein Bild zurück dieses wird dann in der Img-Queue eingereiht
    def do_run(self):
        self.prepareTask()
        time.sleep(5)
        ADS_Comm.WriteCheckerActive(self.plc,True)
        self.log_queue.put(bc.LogMsg(f"{self.name}: Kamera und Applikation wird auf Aktiv gesetzt"))
        ADS_Comm.WriteKameraActive(self.plc, self.index, True)

        while ((not self.shouldStop.is_set())):
            time.sleep(0.2)
            self.readTrigger()
            test = self.startTrigger()
            if(ADS_Comm.ReadCheckerTest(self.plc)):
                ADS_Comm.WriteCheckerTest(self.plc,False)

            if (test):
                self.ID = ADS_Comm.ReadID(self.plc,self.index)
                self.log_queue.put(bc.LogMsg(f"{self.name}: Trigger"))
                acqThread = threading.Thread(target=self.myCam.executeTrigger, args=())
                acqThread.start()

                if (self.myCam.evImgAcquiered.wait(10)):
                    self.myCam.VisImg.valText = self.ID
                    self.myCam.VisImg.CamIndex = self.name
                    val_img = self.myCam.VisImg
                    self.myQueue.put(val_img)
                acqThread.join()

                if self.endTrigger():
                    pass            
        self.exitTask()
    

    #Thread wird gestoppt
    def stopTask(self):
        self.shouldStop.set()

