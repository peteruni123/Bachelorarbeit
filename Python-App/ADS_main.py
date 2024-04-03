import ML_Teil
import ML_GUI_angepasst
import Database
import BasicClasses as bc
import logging
import time
import TaskThreadMaster
import ParameterDBtoPLC

logger = logging.getLogger(__name__)
    
if __name__ == "__main__":
    print('Hello, You are now starting the Application')

    #Den Pfad zu den Bildern definieren
    path_to_imgs = "DataforDemo"

    #Initialisieren der verschiedenen Queues
    my_ImgQueue = bc.PeterQueue(10)
    my_ResultQueueDB = bc.PeterQueue(10)
    my_ResultQueueGUI = bc.PeterQueue(10)
    my_LogQueue = bc.PeterQueue(30)

    #Initialisierung der verschiedenen Threads (TaskThreadMaster, ML-Thread, DB-Thread, GUI-Thread)
    my_LogQueue.put(bc.LogMsg("ADS_main: Intialisierung Parameter Thread"))
    myParameter_thread = ParameterDBtoPLC.ParameterTaskClass(my_LogQueue)
    
    my_LogQueue.put(bc.LogMsg("ADS_main: Intialisierung Vision Thread"))
    myVisionTask_thread = TaskThreadMaster.VisionTaskClass(my_ImgQueue, path_to_imgs, my_LogQueue)

    my_LogQueue.put(bc.LogMsg("ADS_main: Intialisierung ML Modul"))
    ML_app = ML_Teil.MLThread(my_ImgQueue ,my_ResultQueueDB ,my_ResultQueueGUI, my_LogQueue)
    
    my_LogQueue.put(bc.LogMsg("ADS_main: Intialisierung DB"))
    db = Database.DBThread(my_ResultQueueDB, my_LogQueue)
    
    my_LogQueue.put(bc.LogMsg("ADS_main: Intialisierung GUI"))
    app = ML_GUI_angepasst.VisionGUITkClass(my_ResultQueueGUI, my_LogQueue)
    my_LogQueue.put(bc.LogMsg("ADS_main: Intialisierungen Abgeschlossen"))
    
    
    #Starte Threads (TaskThreadMaster, ML-Thread, DB-Thread)
    my_LogQueue.put(bc.LogMsg("ADS_main: Starte Threads"))
    myParameter_thread.start()
    myVisionTask_thread.start()
    ML_app.start()
    db.start()
    my_LogQueue.put(bc.LogMsg("ADS_main: Threads wurden gestarted"))


    #GUI Mainloop wird gestartet
    app.check_update()
    app.mainloop()
    print("Exited GUI...")

    #Threads werden gestoopt
    myVisionTask_thread.stopTask()
    ML_app.stopTask()
    db.stopTask()
    myParameter_thread.stopTask()
    while(not( ML_app.closed and db.closed and myVisionTask_thread.closed and myParameter_thread.closed)):
        time.sleep(0.2)
    print("Threads are stopped...")


    #Queues werden geleert
    while not my_ImgQueue.empty():
        item = my_ImgQueue.get()
        my_ImgQueue.task_done()
    
    while not my_ResultQueueDB.empty():
        item = my_ResultQueueDB.get()
        my_ResultQueueDB.task_done()

    while not my_ResultQueueGUI.empty():
        item = my_ResultQueueGUI.get()
        my_ResultQueueGUI.task_done()

    while not my_LogQueue.empty():
        try:
            item = my_LogQueue.get_nowait()
        except:
            pass

    print("Queues empty...")
        
    

    
    #Queues werden gejoined
    my_ImgQueue.join()
    my_ResultQueueDB.join()
    my_ResultQueueGUI.join()
    print('Queues done...')

    #Threads werden gejoined
    myVisionTask_thread.join()
    ML_app.join()
    db.join()
    myParameter_thread.join()
    print('Threads done...')
    print('Application Closed')