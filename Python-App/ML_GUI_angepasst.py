
from tkinter import *
from tkinter import messagebox
import threading
import BasicClasses as bc
import logging
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W

logger = logging.getLogger(__name__)


class ConsoleUi:
    #Dieses Objekt ist das Log-Fenster und wird von Haupt-GUI aufgerufen
    def __init__(self, frame, log_queue: bc.PeterQueue):
        self.frame = frame
        self.scrolled_text = ScrolledText(frame, state='disabled', height=12)
        self.scrolled_text.grid(row=0, column=0)
        self.scrolled_text.configure(font='TkFixedFont')
        self.log_queue = log_queue
        self.frame.after(100, self.poll_log_queue)


    #Diese Funktion schreibt record in das Log-Fenster
    def display(self, record):
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(END, record + '\n')
        self.scrolled_text.configure(state='disabled')
        self.scrolled_text.yview(END)

    #Überpüft alle 100ms ob sich etwas in der Log-Queue befindet und ruft display auf falls True
    def poll_log_queue(self):
        while True:
            if (not self.log_queue.empty()):
                record=self.log_queue.get()
                self.display(record.v_text)
            else:
                break
        self.frame.after(100, self.poll_log_queue)

class VisionGUITkClass(Tk):
    #Initalisierung der GUI
    def __init__(self, val_queue : bc.PeterQueue, log_queue: bc.PeterQueue):
        
        super().__init__()
        self.title("Basic GUI Layout")
        self.config(bg="skyblue") 
        self.maxsize(2900,2600)
        self.protocol('WM_DELETE_WINDOW', self.on_exit) 
        self.log_queue = log_queue
        self.evShouldStop = threading.Event()
        self.lock = threading.Lock()
        self.myQueue = val_queue

        #Initalisierung der GUI Komponenten
        self.left_frame = Frame(self, width=250, height=100, bg='grey')
        self.left_frame.grid(row=0, column=0, padx=10, pady=5)

        # Initialisierung des rechten Frames
        right_frame = Frame(self, width=250, height=100, bg='grey')
        right_frame.grid(row=0, column=1, padx=10, pady=5)

        #Initialisierung des Log-Fensters
        self.console = ConsoleUi(right_frame, self.log_queue)

        # Initialisierung des linken Frames
        self.tool_bar = Frame(self.left_frame, width=280, height=285)
        self.tool_bar.grid(row=2, column=0, padx=5, pady=5)

        # Inhalt des linken Frames 
        self.cam = Label(self.tool_bar, text="Cam_Idx")
        self.cam.grid(row=0, column=0, padx=5, pady=3, ipadx=10)
        self.cam1 = Label(self.tool_bar, text="none")
        self.cam1.grid(row=0, column=1, padx=5, pady=3, ipadx=10)

        self.ID = Label(self.tool_bar, text="ID")
        self.ID.grid(row=1, column=0, padx=5, pady=3, ipadx=10)
        self.ID1 = Label(self.tool_bar, text="none")
        self.ID1.grid(row=1, column=1, padx=5, pady=3, ipadx=10)
        
        Label(self.tool_bar, text="Result").grid(row=2, column=0, padx=5, pady=5)
        self.result = Label(self.tool_bar, text="none")
        self.result.grid(row=2, column=1, padx=5, pady=5)

        Label(self.tool_bar, text="Timestemp").grid(row=3, column=0, padx=5, pady=5)
        self.timestemp = Label(self.tool_bar, text="none")
        self.timestemp.grid(row=3, column=1, padx=5, pady=5)


    #Beenden der Applikation
    def on_exit(self):
        if messagebox.askyesno("Exit", "Do you want to quit the application?"):
            self.evShouldStop.set()
            self.after(500, self.quit)
            

    #Prüft ob etwas in der Ergebnis-Queue falls ja wird callback ausgeführt
    def check_update(self):
        if not self.evShouldStop.is_set():
            needed_update = not self.myQueue.empty()
            
            while not self.myQueue.empty():
                #--------------------------------
                item = self.myQueue.get()
                self.myQueue.task_done()
                self.callback(1,item)
                #------------------------------
            if needed_update:
                self.after(300, self.check_update)
            else:
                self.after(100, self.check_update)


    #Visualisiert das Ergebnis in der GUI
    def callback(self,step,item):
        self.log_queue.put(bc.LogMsg("GUI: Ergebnisse werden in GUI geschrieben"))
        self.ID1.configure(text = item.valID)
        self.cam1.configure(text = item.CamIndex)
        self.result.configure(text = item.valResult)
        self.timestemp.configure(text = item.valTimestemp)

