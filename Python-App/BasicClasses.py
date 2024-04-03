import numpy as np
from datetime import datetime 
import queue
import logging

#Klasse Log-Nachricht Objekte dieser Klasse werden in die Log-Queue eingereiht 
class LogMsg():
    def __init__(self, val_text, val_msgType = 'I') -> None:
        self.msgType = val_msgType 
        date_time = datetime.fromtimestamp(datetime.now().timestamp())
        str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S.%f")[:-3]
        self.v_text = f'{str_date_time} :: {self.msgType} :: {val_text}'

#Klasse VisImage Objekte dieser Klasse werden in die Image-Queue eingereiht 
class VisImage():
    def __init__(self, val_imgEntry = np.zeros([20,20],dtype=np.uint8)) -> None:
        self.valimage = val_imgEntry
        self.valText = '' 
        self.stageIdx = 0
        self.CamIndex = ''

#Klasse ResultImage enthält Ergebnisse zur Analyse und Objekte dieser Klasse werden in die Ergebnis-Queues eingereiht 
class ResultImage():
    def __init__(self) -> None:
        self.valID = ''
        self.valResult= '' 
        self.valTimestemp = ''
        self.CamIndex = ''

#Queue-Klasse
class PeterQueue(queue.Queue):
    def __init__(self, maxsize: int = 0) -> None:
        super().__init__(maxsize)
        
    def fullhandling(self):
        if(self.full()):
            print('Achtung voll! Achtung voll!')

#Klasse für die Log-Queue
class QueueHandler(logging.Handler):

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def log(self, record):
        self.log_queue.put(record)
