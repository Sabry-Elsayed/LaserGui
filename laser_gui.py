from laser import *
from tkinter import *
from PIL import ImageTk , Image
import  serial,time

# from serial import Serial

# ttl = serial.Serial('COM4', 9600, 8, 'N', 1) # open serial connection

FIRST_TARGET  = 0                                                               
LAST_TARGET  = 1    
MULTIPLE_TARGET  = 2    

TargetConfigCMD   = [[0xEE,0x16,0x03,0x03,0x03,0x01,0x07],[0xEE,0x16,0x03,0x03,0x03,0x02,0x08],[0xEE,0x16,0x03,0x03,0x03,0x03,0x09]]

ContinousModeCMD = [0xEE,0x16,0x04,0x03,0xA1,0x01,0x00,0xA5]

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
        if retStat == True :
             print("First Target has been set")
             Target_Mode = FIRST_TARGET_MODE
             
        else :
             print("Error In Setting First Target , Please Try Again")     
             
        # ttl.write(serial.to_bytes(TargetConfigCMD[FIRST_TARGET]))
    elif val == 2:
         print("Last Target")
         WriteDataToSerialPort(TargetConfigCMD[LAST_TARGET])
         retStat = LR_Recieve_Target_Type_ACK()
         if retStat == True :
             print("Last Target has been set")
             Target_Mode = LAST_TARGET_MODE
         else :
             print("Error In Setting Last Target , Please Try Again")     
    elif val == 3:
        print("Multiple Target")
        WriteDataToSerialPort(TargetConfigCMD[MULTIPLE_TARGET])
        retStat = LR_Recieve_Target_Type_ACK()
        if retStat == True :
             print("Multiple target has been set")
             Target_Mode = MULTIPLE_TARGET_MODE
        else :
             print("Error In Setting Multiple Target , Please Try Again")     
   
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
        print("hello distance " ,ret_laser_data)
        disVal.set(str(ret_laser_data[0]))
        type_of_target_val.set(str(ret_laser_data[1]))
        no_of_target.set(str(ret_laser_data[2]))
    else:
        disVal.set(str("not respond "))
        type_of_target_val.set(str(" not respond"))
        no_of_target.set(str("not respond "))

    


def UpdateReadyFlag():
    global readyFlag
    readyFlag = True


count = 10

readyFlag = False



# initialize the GUI 
root = Tk()
root.title("Iono Laser Test")
root.geometry("800x800+150+200")
root.resizable(False,False)
v = IntVar()
############# Laser Data #################
disVal = StringVar()
type_of_target_val = StringVar()
no_of_target = StringVar()
##########################################


# Initialize background 
bg=Image.open("./IonoBg.PNG").resize((800,800))
bgImage = ImageTk.PhotoImage(bg)
lb5 = Label(root,image=bgImage )
lb5.place(x=0,y=0,relwidth=1,relheight=1)


# bg.resize(800,800)

########################################## Target Menu ########################################################## 
Radiobutton(root,text="First Target",variable=v,value=1 ,command=TypeOfTargetHandler ).grid(row=1 , column= 0)
Radiobutton(root,text="Last Target",variable=v,value=2,command=TypeOfTargetHandler).grid(row=2,   column= 0)
Radiobutton(root,text="Multiple Target",variable=v,value=3,command=TypeOfTargetHandler).grid(row=3 ,column= 0)
lb1 = Label(root,text="Configure Type of Target",fg="red" , font=('Helvetica', 10, 'bold'))
#################################################################################################################


#########################    Save Setting Button, Start Button and GetDistance Button    ######################## 
bt2 = Button(root,text = "save setting" , fg = "red",command=UpdateReadyFlag , font=('Helvetica', 10, 'bold'))
bt3 = Button(root,text = "start", fg = "red" , font=('Helvetica', 10, 'bold'))


bt4 = Button(root ,text = "Get Laser Data",fg="red",command=UpdateDistance , font=('Helvetica', 15, 'bold'))

lb1.grid(row=0 , column = 0)
bt2.grid(row=4 , column = 500)
bt3.grid(row=5 , column = 500)
bt4.place(x=10,y=170)


############################## Laser Data lables #############################################
lb4= Label(root,text="distance  ",fg="black" , font=('Helvetica', 10, 'bold'))
distanceLable = Label(root,textvariable=disVal,fg="black" ,bg="gray", width=9)

typeOftarget_lable= Label(root,text="type of target   ",fg="black" , font=('Helvetica', 10, 'bold') , width=15, anchor='w' )
typeOftarget = Label(root,textvariable=type_of_target_val,fg="black" ,bg="gray", width=17)

no_of_target_label = Label(root,text="number of current target   ",fg="black" , font=('Helvetica', 10, 'bold') )
no_Of_target = Label(root,textvariable=no_of_target,fg="black" ,bg="gray", width=24)
################################################################################################
lb4.place(x=15,y=220)
distanceLable.place(x = 15 , y = 240)


typeOftarget_lable.place(x=10,y=280)
typeOftarget.place(x=10, y=300)

no_of_target_label.place(x=10,y=340)
no_Of_target.place(x=10,y=360)





root.update()




###################################################################################################################
BufferSize = 0
while True:

    # print("Hello")
    # if(readyFlag == 1):
    #  BufferSize =ttl.in_waiting()
    # if(BufferSize == 5):
    #   bufferBytes=ttl.read(10)
    #   print(bufferBytes
    root.update()
    root.mainloop()

