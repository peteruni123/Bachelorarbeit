import BasicClasses as bc
import threading
import queue
import pyads
import VisionTaskThread_ADS


class VisionTaskClass(threading.Thread):

    #Thread wird Initalisiert
    def __init__(self, val_queue  : queue.Queue, pathToImgs :str, log_queue: bc.PeterQueue):
        super().__init__()
        self.shouldStop = threading.Event()
        self.lock = threading.Lock()
        self.count = 1
        self.log_queue = log_queue
        self.closed = False
        self.pathToImgs = pathToImgs
        #--------------
        self.taskLock = threading.Lock()
        self.myQueue = val_queue
        self.prepareTask()
        self.InitKameraThreads()


    #Verbindung zur SPS wird hergestellt und die Anzahl der Kameras ausgelesen
    def prepareTask(self):
        self.log_queue.put(bc.LogMsg("Threadmaster: Connecting to SPS"))
        self.plc = pyads.Connection('xxx.xx.xx.xx.x.x', pyads.PORT_TC3PLC1)
        self.plc.open()
        self.isConnected = True
        self.log_queue.put(bc.LogMsg("Threadmaster: Connected to SPS Adress: " +str({self.plc.get_local_address()})))
        self.count = self.plc.read_by_name(".Python_Kamera_Anzahl")
        self.log_queue.put(bc.LogMsg(f"Threadmaster: {self.count} Kameras in SPS entdeckt"))


    #Für jede Kamera wird ein Thread initialisiert
    def InitKameraThreads(self):
        self.Thread_Array = []
        for index in range(1,self.count + 1):
            current_Thread = VisionTaskThread_ADS.VisionTaskClass(self.myQueue, self.pathToImgs, self.log_queue,index)
            current_Thread.start() 
            self.Thread_Array.append(current_Thread)
        self.log_queue.put(bc.LogMsg(f"Threadmaster: {self.count} Kamera-Threads initialisiert"))

    #Die count Kamera Threads werden gestoppt sowie der Threadmaster selber
    def stopTask(self):
        for Thread in self.Thread_Array:
            Thread.stopTask()
            Thread.join()
        while(not self.Thread_Array[-1].closed):
            pass
        self.closed = True