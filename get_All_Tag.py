from pylogix import PLC

with PLC() as comm:
    comm.IPAddress = '192.168.1.10'
    tags = comm.GetTagList()
    
    for t in tags.Value:
        print(t.TagName, t.DataType)

