from tkinter import *
from PIL import ImageTk, Image
import serial
from laser import *
# import time

# from serial import Serial

# ttl = serial.Serial('COM4', 9600, 8, 'N', 1) # open serial connection

FIRST_TARGET = 0
LAST_TARGET = 1
MULTIPLE_TARGET = 2

TargetConfigCMD = [
    [0xEE, 0x16, 0x03, 0x03, 0x03, 0x01, 0x07],
    [0xEE, 0x16, 0x03, 0x03, 0x03, 0x02, 0x08],
    [0xEE, 0x16, 0x03, 0x03, 0x03, 0x03, 0x09],
]
##########################################################################################     
type_of_target_list_1 = ["Single Target" , "Front Traget" , "Rear Target" , "None" , "Out Of Range" , "None"]

type_of_target_list_2 = ["Single Target" , "Front Traget" , "Rear Target" , "Front and Rear Target" , "Out Of Range" , "None"]
##########################################################################################
ContinousModeCMD = [0xEE, 0x16, 0x04, 0x03, 0xA1, 0x01, 0x00, 0xA5]

LR_SINGLE_RANGING = 1
LR_CONTINOUS_RANGING = 2

LR_RANGING_MODE = 0

ConfigrationFlag = 0

print(type(FIRST_TARGET))
print(TargetConfigCMD[FIRST_TARGET])

print(ContinousModeCMD)



def TypeOfTargetHandler():
    global v
    global Target_Mode
    val = v.get()
    if val == 1:
        print("First Target")
        # for num in TargetConfigCMD[FIRST_TARGET]:
        WriteDataToSerialPort(TargetConfigCMD[FIRST_TARGET])
        retStat = LR_Recieve_Target_Type_ACK()
        if retStat:
            print("First Target has been set")
            set_target_mode(FIRST_TARGET_MODE)
            # Target_Mode = FIRST_TARGET_MODE
        else:
            print("Error In Setting First Target, Please Try Again")

        # ttl.write(serial.to_bytes(TargetConfigCMD[FIRST_TARGET]))
    elif val == 2:
        print("Last Target")
        WriteDataToSerialPort(TargetConfigCMD[LAST_TARGET])
        retStat = LR_Recieve_Target_Type_ACK()
        if retStat:
            print("Last Target has been set")
            set_target_mode(LAST_TARGET_MODE)
            # Target_Mode = LAST_TARGET_MODE
        else:
            print("Error In Setting Last Target, Please Try Again")
    elif val == 3:
        print("Multiple Target")
        WriteDataToSerialPort(TargetConfigCMD[MULTIPLE_TARGET])
        retStat = LR_Recieve_Target_Type_ACK()
        if retStat:
            print("Multiple target has been set")
            set_target_mode(MULTIPLE_TARGET_MODE)
            # Target_Mode = MULTIPLE_TARGET_MODE
        else:
            print("Error In Setting Multiple Target, Please Try Again")


def TypeOfRangingHandler():
    global LR_Ranging_Type
    global LR_RANGING_MODE
    global ConfigrationFlag
    val = LR_Ranging_Type.get()

    if val == 1 and ConfigrationFlag == 0:
        
        LR_RANGING_MODE = LR_SINGLE_RANGING
        print("Single Ranging Mode has been set")
    elif val == 2 and ConfigrationFlag == 0:
        
        LR_RANGING_MODE = LR_CONTINOUS_RANGING
        LR_Set_Continous_Ranging_CMD()
        print("Continous Ranging Mode has been set")

#########################################################################################
def get_type_of_target(type_of_trget_val):
     global Target_Mode
        
     if Target_Mode == FIRST_TARGET_MODE or Target_Mode == LAST_TARGET_MODE:
          retType_of_target = type_of_target_list_1[type_of_trget_val]
          print("<<<<<<<<<<<<<< Target Mode /////////////>>>>>>>>>>>>>>",Target_Mode)
     elif Target_Mode == MULTIPLE_TARGET_MODE:
          retType_of_target = type_of_target_list_2[type_of_trget_val]
          print("<<<<<<<<<<<<<< Target Mode >>>>>>>>>>>>>>",Target_Mode)
     return retType_of_target
#########################################################################################


def UpdateDistance():
    ## send single ranging command
    uart_serial.flushOutput()
    uart_serial.flushInput()
    LR_Set_Single_Ranging_CMD()
    ## receive the response
    ret_laser_data = LR_ReceiveResponse()
    if ret_laser_data is not None:
        global count
        global distance
        count = count + 1
        print("hello distance ", ret_laser_data)
        disVal.set(str(ret_laser_data[0]))
        type_of_target_val.set(str(ret_laser_data[1]))
        no_of_target.set(str(ret_laser_data[2]))
    else:
        disVal.set(str("not respond"))
        type_of_target_val.set(str("not respond"))
        no_of_target.set(str("not respond"))

dis_val = 0
target_type_val = 0
no_of_target_val = 0  

def UpdateDistance_2():
    global dis_val 
    global target_type_val 
    global no_of_target_val  
    ## send single ranging command
    uart_serial.flushOutput()
    uart_serial.flushInput()
    
    
    ret_laser_data = LR_ReceiveResponse_2()
    if ret_laser_data is not None:
        global count
        global distance
        count = count + 1
        dis_val = ret_laser_data[0]
        target_type_val = ret_laser_data[1]
        no_of_target_val = ret_laser_data[2]
        print("hello distance ", ret_laser_data)
       
    else:
        disVal.set(str(dis_val))
        type_of_target_val.set(str(target_type_val))
        no_of_target.set(str(no_of_target_val))
        # disVal.set(str("not respond"))
        # type_of_target_val.set(str("not respond"))
        # no_of_target.set(str("not respond"))


def UpdateReadyFlag():
    global readyFlag
    readyFlag = True


count = 10
readyFlag = False
running = True  # New flag to control task scheduling

# initialize the GUI
root = Tk()
root.title("Iono Laser Test")
root.geometry("800x800+150+200")
root.resizable(False, False)
v = IntVar()
LR_Ranging_Type = IntVar()
LR_Ranging_Type.set(0)
############# Laser Data #################
disVal = StringVar()
type_of_target_val = StringVar()
no_of_target = StringVar()
##########################################

# Initialize background
bg = Image.open("./IonoBg.PNG").resize((800, 800))
bgImage = ImageTk.PhotoImage(bg)
lb5 = Label(root, image=bgImage)
lb5.place(x=0, y=0, relwidth=1, relheight=1)

# bg.resize(800,800)

########################################## Target Menu ##########################################################
Radiobutton(
    root, text="First Target", variable=v, value=1, command=TypeOfTargetHandler
).grid(row=1, column=0)
Radiobutton(
    root, text="Last Target", variable=v, value=2, command=TypeOfTargetHandler
).grid(row=2, column=0)
Radiobutton(
    root, text="Multiple Target", variable=v, value=3, command=TypeOfTargetHandler
).grid(row=3, column=0)
lb1 = Label(
    root, text="Configure Type of Target", fg="red", font=("Helvetica", 10, "bold")
)
#################################################################################################################

########################################## Target Menu ##########################################################
Radiobutton(
    root, text="Single Ranging", variable=LR_Ranging_Type, value=1, command=TypeOfRangingHandler
).grid(row=1, column=800)
Radiobutton(
    root, text="Continous Ranging", variable=LR_Ranging_Type, value=2, command=TypeOfRangingHandler
).grid(row=2, column=800)
ranging_mode_lb = Label(
    root, text="Configure Type of Ranging Mode", fg="red", font=("Helvetica", 10, "bold")
)
ranging_mode_lb.grid(row=0, column=800)
#################################################################################################################

#########################    Save Setting Button, Start Button and GetDistance Button    ########################
bt2 = Button(
    root, text="save setting", fg="red", command=UpdateReadyFlag, font=("Helvetica", 10, "bold")
)
bt3 = Button(root, text="start", fg="red", font=("Helvetica", 10, "bold"))

lb1.grid(row=0, column=0)
bt2.grid(row=4, column=500)
bt3.grid(row=5, column=500)
################################################################################################################

############################## Laser Data lables ###############################################################
lb4 = Label(root, text="distance  ", fg="black", font=("Helvetica", 10, "bold"))
distanceLable = Label(root, textvariable=disVal, fg="black", bg="gray", width=9)

typeOftarget_lable = Label(
    root,
    text="type of target   ",
    fg="black",
    font=("Helvetica", 10, "bold"),
    width=15,
    anchor="w",
)
typeOftarget = Label(root, textvariable=type_of_target_val, fg="black", bg="gray", width=17)

no_of_target_label = Label(
    root, text="number of current target   ", fg="black", font=("Helvetica", 10, "bold")
)
no_Of_target = Label(root, textvariable=no_of_target, fg="black", bg="gray", width=24)
###############################################################################################################
lb4.place(x=15, y=220)
distanceLable.place(x=15, y=240)

typeOftarget_lable.place(x=10, y=280)
typeOftarget.place(x=10, y=300)

no_of_target_label.place(x=10, y=340)
no_Of_target.place(x=10, y=360)

def task():
    global ConfigrationFlag
    global LR_RANGING_MODE
    if running:  # Check if the task should continue
        
        if LR_RANGING_MODE == LR_SINGLE_RANGING and ConfigrationFlag == 0:
            ConfigrationFlag = 1
            bt4 = Button(root, text="Get Laser Data", fg="red", command=UpdateDistance, font=("Helvetica", 15, "bold"))
            bt4.place(x=10, y=170)
        elif LR_RANGING_MODE == LR_CONTINOUS_RANGING and ConfigrationFlag == 0:
             ConfigrationFlag = 1

        if LR_RANGING_MODE == LR_CONTINOUS_RANGING and ConfigrationFlag == 1:
            UpdateDistance_2()   
        global job_id
        job_id = root.after(1, task)  # reschedule event in 2 seconds

def on_closing():
    global running
    running = False  # Stop task scheduling
    if job_id is not None:
        root.after_cancel(job_id)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

job_id = root.after(1, task)

root.mainloop()
