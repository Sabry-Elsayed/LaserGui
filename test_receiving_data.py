import  serial,time

import sys
import struct

##################################################################################################


# ######################## Configure Serial Paramters #########################
uart_serial = serial.Serial('COM4', 9600, 8, 'N', 1 ) # open serial connection

# #############################################################################

############################## Read Serial ###################################### 
def Read_Serial_Port(serial_type,Data_Len):
    Serial_Value = serial_type.read(Data_Len)
    # Serial_Value_len = len(Serial_Value)
    # while Serial_Value_len <= 0:
    #     Serial_Value = serial_type.read(Data_Len)
    #     Serial_Value_len = len(Serial_Value)
    return Serial_Value         
    # return Serial_Value
########################################################################################

# rerVal = Read_Serial_Port(uart_serial,10)
# print(rerVal)

retval = uart_serial.read(8)
print(retval)