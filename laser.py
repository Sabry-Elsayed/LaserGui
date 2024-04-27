from tkinter import *
from PIL import ImageTk , Image
import  serial,time
# from serial import Serial

# ttl = serial.Serial('COM4', 9600, 8, 'N', 1) # open serial connection

FIRST_TARGET  = 0                                                               
SECOND_TARGET  = 1    
THIRD_TARGET  = 2    

TargetConfigCMD   = [[0xEE,0x16,0x03,0x03,0x03,0x01,0x07],[0xEE,0x16,0x03,0x03,0x03,0x02,0x08],[0xEE,0x16,0x03,0x03,0x03,0x03,0x09]]

ContinousModeCMD = [0xEE,0x16,0x04,0x03,0xA1,0x01,0x00,0xA5]

print(type(FIRST_TARGET))
print(TargetConfigCMD[FIRST_TARGET])
print(ContinousModeCMD)
def TypeOfTargetHandler():
    global v
    val = v.get()
    if val == 1:
        print("First Target")
        # for num in TargetConfigCMD[FIRST_TARGET]:
        # ttl.write(serial.to_bytes(TargetConfigCMD[FIRST_TARGET]))
    elif val == 2:
        for num in TargetConfigCMD[FIRST_TARGET]:
            # ttl.write(num.encode())
            print("hello")
    elif val == 3:
        for num in TargetConfigCMD[FIRST_TARGET]:
            # ttl.write(num.encode())
            print("hello")

def UpdateDistance():
    global count
    count = count + 1
    disVal.set(str(count))

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

disVal = StringVar()

# Initialize background 
bg=Image.open("D:/LaserGUI/IonoBg.PNG").resize((800,800))
bgImage = ImageTk.PhotoImage(bg)
lb5 = Label(root,image=bgImage )
lb5.place(x=0,y=0,relwidth=1,relheight=1)


# bg.resize(800,800)

########################################## Target Menu ########################################################## 
Radiobutton(root,text="First Target",variable=v,value=1 ,command=TypeOfTargetHandler ).grid(row=1 , column= 0)
Radiobutton(root,text="Last Target",variable=v,value=2,command=TypeOfTargetHandler).grid(row=2,   column= 0)
Radiobutton(root,text="Multiple Target",variable=v,value=3,command=TypeOfTargetHandler).grid(row=3 ,column= 0)
lb1 = Label(root,text="Configure Type of Target",fg="black")
#################################################################################################################


#########################    Save Setting Button, Start Button and GetDistance Button    ######################## 
bt2 = Button(root,text = "save setting" , fg = "black",command=UpdateReadyFlag)
bt3 = Button(root,text = "start", fg = "black")
bt4 = Button(root ,text = "GetDistance",fg="black",command=UpdateDistance)

lb1.grid(row=0 , column = 0)
bt2.grid(row=4 , column = 500)
bt3.grid(row=5 , column = 500)
bt4.place(x=340,y=350)

lb4= Label(root,text="distance = ",fg="black" )
distanceLable = Label(root,textvariable=disVal,fg="black" ,bg="yellow", width=10)

lb4.place(x=340,y=400)
distanceLable.place(x = 400 , y = 400)
root.update()
###################################################################################################################
BufferSize = 0
while True:

    # print("Hello")
    # if(readyFlag == 1):
    #  BufferSize =ttl.in_waiting()
    # if(BufferSize == 5):
    #   bufferBytes=ttl.read(10)
    #   print(bufferBytes)
    root.update()
    root.mainloop()

