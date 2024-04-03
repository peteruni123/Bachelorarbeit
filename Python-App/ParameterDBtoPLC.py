import BasicClasses as bc
import threading
import time
import pyads
import ADS_Comm
import pymysql 

class ParameterTaskClass(threading.Thread):

    #Initialiserung des Threads
    def __init__(self, log_queue: bc.PeterQueue):
        super().__init__(target=self.do_run, args=())
        self.shouldStop = threading.Event()
        self.lock = threading.Lock()
        self.resetStates()
        self.log_queue = log_queue
        self.closed = False
        #--------------
        self.taskLock = threading.Lock()
        
    #Setzt den Vebindungsstatus zurück    
    def resetStates(self, val_isConn = False):
        try:
            self.lock.acquire()
            self.isConnected = val_isConn
        finally:
            self.lock.release()

    
    #Verbinung zur SPS und zur Datenbank wird hergestellt
    # Parameter Tabelle wird erstellt und die Paramtername und ihre Werte in die Datenbank geschrieben
    def prepareTask(self):
        #Verbindungen
        self.log_queue.put(bc.LogMsg("ParameterDBtoPLC: Connecting to SPS"))
        self.plc = pyads.Connection('xxx.xx.xx.xx.x.x', pyads.PORT_TC3PLC1)
        self.plc.open()
        self.isConnected = True
        self.log_queue.put(bc.LogMsg("ParameterDBtoPLC: Connected to SPS Adress: " +str({self.plc.get_local_address()})))
        self.count = self.plc.read_by_name(".Python_Kamera_Anzahl")
        #---------
        
        # Tabelle und Parameter Werte
        self.tablename = 'Paramter_Tabelle'
        self.mysql1 = f"INSERT INTO {self.tablename} (Indizes, Name, Value) VALUES (%s, %s, %s)"
        self.CheckConnection()
        self.CheckTable()
        try:
            for i in range(1, self.count + 1):

                Paramter = ADS_Comm.ReadParameter(self.plc, i)
                Name = ADS_Comm.ReadName(self.plc, i)
                self.mycursor = self.conn.cursor()
                self.sqlval = (i, Name, Paramter)
                self.mycursor.execute(self.mysql1, self.sqlval)
                self.conn.commit()
        except:
            self.CheckConnection()
         

    #Beenden des Threads: Parameter Tabelle wird geleert und die Verbindungen getrennt
    def exitTask(self):
        self.closed = True
        try:
            sql_query = f"DELETE FROM {self.tablename}"
            cursorObject = self.conn.cursor()
            cursorObject.execute(sql_query)
            self.conn.commit()
            self.conn.close()
            self.plc.close()
        except:
            self.log_queue.put(bc.LogMsg("ParameterDBtoPLC: Connection to Database already closed"))
        

    #mainloop des Threads
    def do_run(self):
        self.prepareTask()
        
        while ((not self.shouldStop.is_set())):
            time.sleep(5)
            self.CheckConnection()

            if(self.CheckConnection()):
                self.CompareParams()
            try:
                self.conn.commit()
            except:
                self.CheckConnection()
            
        self.exitTask()
    
    #Den Thread stoppen
    def stopTask(self):
        self.shouldStop.set()
        

    #Es wird überprüft ob sich ein Parameter Wert in der Datenbank geändert hat falls dies der Fall ist wird er in die SPS geschrieben
    def CompareParams(self):
        try:
            sql_query = f"select * from {self.tablename}"
            cursorObject = self.conn.cursor()
            cursorObject.execute(sql_query)
            rows = cursorObject.fetchall()
            for i in range(1, self.count + 1):
                Paramter_PLC = ADS_Comm.ReadParameter(self.plc, i)
                Paramter_DB = rows[i-1][2] 
                if (Paramter_DB != Paramter_PLC):
                    ADS_Comm.WriteParameter(self.plc, i, Paramter_DB)

        except:
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
                    user='xxxx', 
                    password = "xxxxxxxxxxx",
                    db='xxxxxxxxxxxx',
                    )
                return True
            except:
                self.log_queue.put(bc.LogMsg("ParameterDBtoPLC: Can not connect to Database"))
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
    
    #erstellt passende Tabelle falls noch keine Tabelle mit dem gleichen Namen in der Datenbank liegt
    def CheckTable(self):
        try:
            tablename = 'Paramter_Tabelle'
            if(self.checkTableExists(self.conn, tablename)):
                pass
            else:
                self.CheckConnection()
                self.mycursor = self.conn.cursor()
                self.mycursor.execute(f"CREATE TABLE {tablename} (Indizes VARCHAR(255), Name VARCHAR(255), Value VARCHAR(255))")
        except:
            self.CheckConnection()
        return tablename