
import  serial,time

import sys
import struct

# ######################## Configure Serial Paramters #########################
uart_serial = serial.Serial('COM4', 9600, 8, 'N', 1) # open serial connection

# #############################################################################
# print("sum = " , val)

#########################################################################
def WriteDataToSerialPort(Data):     
            print(Data)
            uart_serial.write(serial.to_bytes(Data))                #(uart_serial.to_bytes(Data))

############################## Read Serial ###################################### 
def Read_Serial_Port(serial_type,Data_Len):
    Serial_Value = serial_type.read(Data_Len)
    Serial_Value_len = len(Serial_Value)
    while Serial_Value_len <= 0:
        Serial_Value = serial_type.read(Data_Len)
        Serial_Value_len = len(Serial_Value)
    return Serial_Value         
    # return Serial_Value
########################################################################################
##########################################################################            
LR_SINGLE_RANGING_CMD = [0xEE,0x16,0x02,0x03,0x02,0x05]

# while True:
        # uart_serial.flushOutput()
        # uart_serial.flushInput()
for i in range(0,300):
    WriteDataToSerialPort(bytearray(LR_SINGLE_RANGING_CMD))
    time.sleep(0.010)
