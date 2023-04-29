from pylogix import PLC


from Udt_Class import TC, GP_Pylogix_UDT

list = ['Zn4_sim_air_FB','Zn4_sim_gas_FB','Znx_Temp_Hlimit']

with PLC() as comm:
    comm.IPAddress = '192.168.1.10'
    comm.ProcessorSlot = (0)


ret2 = comm.Read('DA_TC')

print(ret2.Status)
t2 = TC(ret2.Value)
ret5 = comm.Read('GP_PYLOGIX')
t6 = GP_Pylogix_UDT(ret5.Value)
tag1 = comm.Read(list)
# print(tag1)
for r in tag1:
    print( f"{r.TagName} = {r.Value}.") 
    
    
ret4 = comm.Read('Zone_Temp[0]',10)
print(ret4.Status)
print(ret4.Value)
print("DA_TC")
print(t2.signal, t2.temp, t2.code, t2.fault,t2.At_Alarm, t2.At_Warn, t2.Disabled, t2.Out_of_Range,t2.At_Shutdown)
print("GP_PYlogix_UDT")
print(t6.Temp, t6.fault_code, t6.Bit1, t6.Bit2,t6.Bit3)
print(t6.id)
print(t6.id_data)
print(t6.Zoneno)