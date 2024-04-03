#MYSQL
import threading
import pymysql
import BasicClasses as bc
import time
from datetime import datetime

class DBThread(threading.Thread):

    #Initialisierung des Threads
    def __init__(self, val_queue : bc.PeterQueue, log_queue: bc.PeterQueue):
        super().__init__(target=self.check_update, args=())
        self.myResultQueue = val_queue
        self.evShouldStop = threading.Event()
        self.log_queue = log_queue
        self.closed = False
        #Verbindung zur Datenbank aufbauen
        try:
            self.conn = pymysql.connect(
                host='xxx.xx.xx.x',
                user='xxxxxxx', 
                password = "xxxxxxxxxxx",
                db='xxxxxxx',
                )
        except:
            self.log_queue.put(bc.LogMsg("DB: Can not connect to Database"))
        self.CheckConnection()
        self.tabelname = self.CheckTable()
            
            
    #Mainloop des Threads
    def check_update(self):
        while (1):
            #Überprüfen ob Datenbank-Thread beendet werden soll
            if self.evShouldStop.is_set():
                break

            #Überprüfen ob Connection zur Datenbank besteht
            if self.CheckConnection():
                pass
            else:
                time.sleep(1)
                continue

            #Überprüfen ob Tagesaktuelle Tabelle vorhanden ist, falls nicht wird eine erstellt
            self.tabelname =  self.CheckTable()

            #Überprüfen ob neue Elemente in die Datenbank geschreiben werden müssen
            needed_update = not self.myResultQueue.empty()    
            while not self.myResultQueue.empty():
                #--------------------------------
                item = self.myResultQueue.get()
                self.myResultQueue.task_done()
                Datenbank_erreicht = self.callback(1,item)

                if Datenbank_erreicht == False:
                    self.myResultQueue.put(item)
                    break
                
                #------------------------------
            if needed_update:
                time.sleep(0.3)
                
            else:
                time.sleep(0.1)
        self.closed = True
                

    #Schreibt ein Element in die Datenbank
    def callback(self,step,item):
        try:
            self.mysql1 = f"INSERT INTO {self.tabelname} (ID, Ergebnis, Zeitstempel, Kameraname) VALUES (%s, %s, %s, %s)"
            self.mycursor = self.conn.cursor()
            self.sqlval = (item.valID,item.valResult, item.valTimestemp, item.CamIndex)
            self.mycursor.execute(self.mysql1, self.sqlval)
            self.conn.commit()
            return True
        except Exception as error:
            self.CheckTable()
            return False
            
            
    #Überprüft ob es bereits eine Tabelle mit dem namen tabelname gibt
    def checkTableExists(self,dbcon, tablename):
        try:
            dbcur = dbcon.cursor()
            stmt = f"SELECT * FROM {tablename}"
            dbcur.execute(stmt)
            return True
            
        except Exception as error:
            return False
    

    #Erstellt tagesaktuellen Tabellenname und erstellt passende Tabelle falls
    #  noch keine Tabelle mit dem gleichen Namen in der Datenbank liegt
    def CheckTable(self):
        try:
            now = datetime.now()
            tablename = 'Peter_Wafer_Colorcheck_' + now.strftime("%d") + now.strftime("%m") +  now.strftime("%Y")
            
            if(self.checkTableExists(self.conn, tablename)):
                pass
            else:
                self.CheckConnection()
                self.mycursor = self.conn.cursor()
                self.mycursor.execute(f"CREATE TABLE {tablename} (ID VARCHAR(255), Ergebnis VARCHAR(255), Zeitstempel VARCHAR(255), Kameraname VARCHAR(255))")
            return tablename
        except Exception as error:
            self.CheckConnection()


    #Überprüft ob die Verbindung vorhanden ist falls nicht versucht es eine aufzubauen
    def CheckConnection(self):
        try:
            if self.conn.open:
                return True
        except:

            try:
                self.conn = pymysql.connect(
                    host='xxx.xx.xx.x',
                    user='xxxxxx', 
                    password = "xxxxxxxx",
                    db='xxxxxxxx',
                    )
            except:
                self.log_queue.put(bc.LogMsg("DB: Can not connect to Database"))
                return False
                   

    #Soll die Abläaufe des Threads beenden
    def stopTask(self):
        try:
            self.conn.close()
        except:
            print("No conection to close")
        self.evShouldStop.set()


        
    
