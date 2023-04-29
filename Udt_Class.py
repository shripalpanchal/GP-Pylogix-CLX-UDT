
from struct import pack, unpack_from


def get_bit(value, bit_number):
    """
    Returns the specific bit of a word
    value = byte no.
    bit_number = bit no in byte.
    """
    mask = 1 << bit_number
    if value & mask:
        return True
    else:
        return False


class TC(object):
    
    def __init__(self, data):
         
        """
        This function reads Thermocouple type data type
        
        name            Datatype        No of bytes     staring byte 
        ===========================================================
        signal          floating        4                   0
        temp            floating        4                   4
        code            sint            1                   8
        fault           Bool            1 bit               9.0
        At_Alarm        Bool            1 bit               9.1
        At_Warn         Bool            1 bit               9.2
        Disabled        Bool            1 bit               9.3
        Out_of Range    Bool            1 bit               9.4
        At_Shutdown     Bool            1 bit               9.5

        """
        # UDT Structure
        self.signal = unpack_from('<f', data, 0)[0]
        self.temp = unpack_from('<f', data, 4)[0]
        self.code = unpack_from('<b', data, 8)[0]
        bits = unpack_from('<b', data, 9)[0]
        self.fault = get_bit(bits, 0)
        self.At_Alarm = get_bit(bits, 1)
        self.At_Warn = get_bit(bits, 2)
        self.Disabled = get_bit(bits, 3)
        self.Out_of_Range = get_bit(bits,4)
        self.At_Shutdown = get_bit(bits, 5)




class L2_Write_Data(object):
    
    def __init__(self, data):
        """
        This function reads L2 Write Datatype data type
        
        name            Datatype        No of bytes     staring byte 
        ============================================================
        watchdog        Dint            4                   0
        Ready           Dint            4                   4
        Sp              Dint[8]         4 byte each         8
       
        """
        # Define Array of length 8 to store temperature setpoint.
        self.Sp = [0] * 8
        #UDT structure
        self.watchdog = unpack_from('<i', data, 0)[0]
        self.Ready = unpack_from('<i', data, 4)[0]
        # Read Dint array of 8. Array starts at byte address 8
        for i in range(0,8):
            self.Sp[i] = unpack_from('<i', data, 8 + i*4)[0]
        





class GP_Pylogix_UDT(object):
     
   def __init__(self, data):
        
        """
        This function reads L2 Write Datatype data type
        
        name            Datatype        No of bytes     staring byte 
        ============================================================
        watchdog        Dint            4                   0
        cabinate_Temp   Dint            4                   4
        Weight          int             2                   8
        fault_code      byte            1                   10
        bit1            Bool            bit-0               11
        bit2            Bool            bit-1               11
        bit3            Bool            bit-2               11
        Temp            Dint[20]        4 byte each         12
        Id              Id(string11)    sint11              88
        ZoneNo          Dint[10]        Dint                412


        """
        # Create Class scope array's
        self.Temp = [0] * 20
        self.id = [''] * 11
        self.id_data = ['' ] * 20
        self.Zoneno = [0] * 10
        # UDT Structure
        self.watchdog = unpack_from('<i', data, 0)[0]
        self.cabinate_Temp = unpack_from('<f', data, 4)[0]
        self.Weight = unpack_from('<h', data, 8)[0]
        self.fault_code = unpack_from('<b', data, 10)[0]
        bits = unpack_from('<b', data, 11)[0]
        self.Bit1 = get_bit(bits, 0)
        self.Bit2 = get_bit(bits, 1)
        self.Bit3 = get_bit(bits, 2)
        Temp_index = 11 + 1
        #Read Real array of 20 in udt
        for i in range(0,20):
            self.Temp[i] = unpack_from('<f', data, Temp_index + i*4)[0]
            # print(i*4)
        # Get Stating Index for next byte.
        id_index = 12+i*4
        #print(id_index)
        #Read string array of 20 string 
        for j in range (0,20):
            value = ''
            # Read 11 Character of string. 
            for i in range(0,11):
                # 8 byte of padding for first character of first Array.
                self.id[i] = unpack_from('<b', data, id_index + i + 8)[0]
                # Check for non null value.
                # If self.id[i] is not null 
                if self.id[i] != 0: 
                    # convert ascii to character.
                    # Concatenate Value in each iteration.
                    value = value +''.join(chr(self.id[i]))
                
                #print(value)   
            #print(value)
            # 6 byte padding for Controllogix PLC for first character of next array.
            id_index = id_index + i + 6
            self.id_data[j] = value     
        
        # Get Starting index for next byte
        Zoneno_Index = id_index +4
        print(Zoneno_Index)
        for i in range(0,10):
            self.Zoneno[i] = unpack_from('<i', data, Zoneno_Index + i*4)[0]
            # print(i*4)
        

      

   
