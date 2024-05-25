###################################################################################
# Author : Sabry Elsayed 
# Data   : 25 /3 / 2024
############################### Laser HIL Test #####################################                    
#
#
####################################################################################


import  serial,time

import sys
import struct


#################### LASER ID,SEQUENCE,COMMAND and TimeStamp INDICES ################

LR_MSG_ID_L_INDX  = 0
LR_MSG_ID_H_INDX  = 1
LR_SEQUENCE_INDX  = 2 
LR_CMD_INDX       = 3
LR_TIME_STAMP_L_INDX   = 8
LR_TIME_STAMP_H_INDX   = 9

############################# Laser Data Frame Indicies ##########################
LR_DISTANCE_H_INDX     = 4
LR_DISTANCE_L_INDX     = 5
LR_TYPE_OF_TARGET_INDX = 6
LR_NO_OF_TARGET_INDX   = 7
####################################################################################


############################## Laser Error Frame Incies ###################################
LR_ERROR_CODE_INDX             = 4
LR_ERROR_TIME_STAMP_L_INDX     = 5
LR_ERROR_TIME_STAMP_H_INDX     = 6
#####################################################################################

LR_CONTINOUS_MODE_STAT = False

LR_TARGET_TYPE_RESPONSE    = [0xEE ,0x16 ,0x02 ,0x03 ,0x03 ,0x06]
LR_CONTINOUS_MODE_RESPONSE = [0XEE ,0x16 ,0x06 ,0x03 ,0x04 ,0x04 ,0x00 ,0x00 ,0x00 ,0x0B]
LR_DATA_FRAME  = [0XEE ,0x16 ,0x06 ,0x03 ,0x04 ,0x01 ,0x01 ,0xf4 ,0x00 ,0xfd]
LR_DATA_FRAME_2  = [0XEE ,0x16 ,0x06 ,0x03 ,0x04 ,0x03 ,0x05 ,0xde ,0x04,0xf1]
LR_NOT_DATA_FRAME_CMD = [0XEE ,0x16 ,0x06 ,0x03 ,0x05 ,0x04 ,0x00 ,0x00 ,0x00 ,0x0C]
LR_WRONG_RESPONSE_FRAME = [0XEE ,0x16 ,0x06 ,0x03 ,0x04 ,0x04 ,0x00 ,0x00 ,0x00 ,0x0A]
'''
 To indicate to constant bytes of the laser commands
  that is the same at all commands
'''
LR_HEADER_HIGH  = 0xEE
LR_HEADER_LOW   = 0x16
LR_EQ_CODE      = 0x03


'''
To indicate to the indices of command information or response 
'''
LR_HEAD_H_IND   =   0
LR_HEAD_L_IND   =   1
LR_LEN_IND      =   2
LR_EQ_CODE_IND  =   3
LR_CMD_IND      =   4

'''
Commands 
'''
SET_TARGET_TYPE_CMD    = 0x03
SET_CONTINOUS_RANGING  = 0x04
LR_ID  = 0x04

############################################################################
LR_DATA_CMD_ID  = 0x01
LR_ERROR_CMD_ID = 0x00
#############################################################################


######################### Laser Data Global Variables #######################
LR_SINGLE_RANGING_CMD = [0xEE,0x16,0x02,0x03,0x02,0x05]
target_type = 0
no_of_target = 0
distance_h = 0
distance_l = 0
decimal_places = 0
distance = 0
##############################################################################
FIRST_TARGET_MODE    = 1
LAST_TARGET_MODE     = 2
MULTIPLE_TARGET_MODE = 3
################################################################################
Target_Mode = 2
# Target_Mode = 2
# ######################## Configure Serial Paramters #########################
uart_serial = serial.Serial('COM4', 9600, 8, 'N', 1 , timeout=.2) # open serial connection

# #############################################################################
# print("sum = " , val)

#########################################################################
def WriteDataToSerialPort(Data):     
            print(Data)
            uart_serial.write(serial.to_bytes(Data))                #(uart_serial.to_bytes(Data))
##########################################################################            


############################## Read Serial ###################################### 
def Read_Serial_Port(serial_type,Data_Len):
    Serial_Value = serial_type.read(Data_Len)
    Serial_Value_len = len(Serial_Value)
    if Serial_Value_len <= 0 :
         return None
#     while Serial_Value_len <= 0:
#         Serial_Value = serial_type.read(Data_Len)
#         Serial_Value_len = len(Serial_Value)
    return Serial_Value         
    # return Serial_Value
########################################################################################

########################### Calculate CheckSum ###########################################
def calc_cs(data):
    checksum = 0
    for byte in data:
        if isinstance(byte, str):
            try:
                checksum += int(byte, 16)  # Convert hexadecimal string to integer
            except ValueError:
                pass  # Ignore non-convertible elements
        else:
            checksum += byte  # If it's not a string, assume it's already an integer
    checksum %= 256
    return checksum     
##########################################################################################

################################## Validate Command ######################################    
def check_cmd(cmd_info) :
     cs_data = cmd_info[3:-1]
     cs = calc_cs(cs_data)
     rec_cs = int(cmd_info[-1] , 16)
     if cs == rec_cs:
          return True
     else:
          return False
##########################################################################################     
type_of_target_list_1 = ["Single Target" , "Front Traget" , "Rear Target" , "None" , "Out Of Range" , "None"]

type_of_target_list_2 = ["Single Target" , "Front Traget" , "Rear Target" , "Front and Rear Target" , "Out Of Range" , "None"]

################################## To Receive Command #####################################
def Reveive_CMD():
     Serial_Value = Read_Serial_Port(uart_serial,2)
     if Serial_Value[0] == LR_HEADER_HIGH and Serial_Value[1] == LR_HEADER_LOW: 
           data_len = Read_Serial_Port(uart_serial,1)
           cmd_info = Read_Serial_Port(uart_serial,data_len[0])
           rec_cs = calc_cs(cmd_info)
           cmd_cs   = Read_Serial_Port(uart_serial,1) 
        #    retVal = hex([Serial_Value , data_len , cmd_info , cmd_cs])   
           retVal = [hex(item) for sublist in [Serial_Value, data_len, cmd_info, cmd_cs] for item in sublist]
           return retVal
     return None
        #    if check_cmd(cmd_cs[0] , rec_cs):

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





#################################Parse Command ###########################################    
def LR_ParseCMD(cmd_info):

     
     global target_type
     global no_of_target
     global distance_h 
     global distance_l
     global decimal_places
     global distance
     global Target_Mode

     target_type = (int( (cmd_info[5])   ,16) & 0x0f)
     no_of_target = ((int( cmd_info[5] ,16) & 0xf0 ) >> 4) + 1

     target_type_val = get_type_of_target(target_type)

     
     distance_h = int( (cmd_info[6])   ,16)
     distance_l = int( (cmd_info[7])   ,16) 
     decimal_places = int( (cmd_info[8])   ,16)
     distance = (distance_h * 256) + (distance_l) + (decimal_places * 0.1)

     retData_Info = [distance , target_type_val , no_of_target]
     return retData_Info
###################################################### Check Response #################################################################

def check_response(actual_response , expected_response):
     if actual_response == expected_response :
          return True
     else:
          return False
########################################################################################################################################
# ee 16 02 03 02 05

def LR_Set_Single_Ranging_CMD():
     WriteDataToSerialPort(LR_SINGLE_RANGING_CMD)
     print(len(LR_SINGLE_RANGING_CMD))
     print("writing data to serial")


########################################################## Resceive Response ############################################################
def LR_ReceiveResponse():
     global Target_Mode
     response = Read_Serial_Port(uart_serial , 10)
     if response != None:
          temp=[]
          for item in response:
               temp.append(hex(item))
          
          response = temp
          print(response)
          retState = check_cmd(response)
          print("ret stat = " , retState)
          if retState == True:
               retDistance = LR_ParseCMD(response) 
       
               return retDistance
               
          else:
               return None
     else:
          return None
       
##########################################################################################################################################
Target_Type_ACK_Frame=[0xEE, 0x16 , 0x02 , 0x03 , 0x03 , 0x06]
def Check_Recieve_Target_Type_ACK(response):
     for i in range(0 , 6):
          if response[i] != Target_Type_ACK_Frame[i]:
               return False
     return True     


def LR_Recieve_Target_Type_ACK():
     response = Read_Serial_Port(uart_serial , 6)
     if response is not None:
          retstat = Check_Recieve_Target_Type_ACK(response)
          return retstat
     return None


l = ["hello" , 5 , 20.5]
print(l)