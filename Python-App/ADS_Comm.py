import pyads
from pyads import constants

CONST_VAR_Kamera =".Python_Kamera_Daten.Lokal"
CONST_VAR_Kamera_Parameter =".Parameter.Lokal"
CONST_VAR_Checker =".Python_Checker"

#Diese Funktionen sind für das lesen und schreiben der Parameterwerte, sowie das lesen der Namen
def ReadParameter(conn :pyads.Connection,index):
    my_str = CONST_VAR_Kamera_Parameter + "[" + str(index) + "]" + ".Value"
    output = conn.read_by_name(my_str, constants.PLCTYPE_TIME)
    return output

def WriteParameter(conn :pyads.Connection,index, Wartezeit):
    my_str = CONST_VAR_Kamera_Parameter + "[" + str(index) + "]" + ".Value"
    output = conn.write_by_name(my_str, plc_datatype=constants.PLCTYPE_TIME, value=int(Wartezeit))
    return output

#Hier wird der Kameraname eingelesen
def ReadName(conn :pyads.Connection,index):
    my_str = CONST_VAR_Kamera_Parameter + "[" + str(index) + "]" + ".Name"
    output = conn.read_by_name(my_str, constants.PLCTYPE_STRING)
    return output


#Diese Funktionen sind für die Verarbeitung des Triggers sowie das
#Updaten und lesen der verschienden Stati

def ReadTrigger(conn :pyads.Connection,index):
    my_str = CONST_VAR_Kamera + "[" + str(index) + "]" + ".CMD.Trigger"
    output = conn.read_by_name(my_str)
    return output

def ReadID(conn :pyads.Connection,index):
    my_str = CONST_VAR_Kamera + "[" + str(index) + "]" + ".CMD.ID"
    output = conn.read_by_name(my_str, constants.PLCTYPE_STRING)
    return output

def WriteTrigger(conn :pyads.Connection,index,value):
    my_str = CONST_VAR_Kamera + "[" + str(index) + "]" + ".CMD.Trigger"
    output = conn.write_by_name(my_str,value)
    

def WriteBusy(conn :pyads.Connection,index, value):
    my_str = CONST_VAR_Kamera + "[" + str(index) + "]" + ".STAT.Busy"
    output = conn.write_by_name(my_str,value)
    
def WritePictureValid(conn :pyads.Connection,index, value):
    my_str = CONST_VAR_Kamera + "[" + str(index) + "]" + ".STAT.PictureValid"
    output = conn.write_by_name(my_str,value)
    

def WriteIsDone(conn :pyads.Connection,index, value):
    my_str = CONST_VAR_Kamera + "[" + str(index) + "]" + ".STAT.IsDone"
    output = conn.write_by_name(my_str,value)

def WriteKameraActive(conn :pyads.Connection,index, value):
    my_str = CONST_VAR_Kamera + "[" + str(index) + "]" + ".STAT.Active"
    output = conn.write_by_name(my_str,value)

def WriteCheckerActive(conn :pyads.Connection, value):
    my_str = CONST_VAR_Checker + ".Python_Active"
    output = conn.write_by_name(my_str,value)


# Diese Funktionen sind für den Python-Checker 

def WriteCheckerTest(conn :pyads.Connection, value):
    my_str = CONST_VAR_Checker + ".Test"
    output = conn.write_by_name(my_str,value)

def ReadCheckerTest(conn :pyads.Connection):
    my_str = CONST_VAR_Checker + ".Test"
    output = conn.read_by_name(my_str)
    return output