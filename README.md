

Example how to use vanubus for a zatobox device with python.

More information about the vanubus protocol can be found in the developer documentation. [https://web-documentation.zatobox.com/docs/developer/vanubus](https://web-documentation.zatobox.com/docs/developer/vanubus)

```python

from python_zatobox.vanubus import Vanubus


host = "192.168.68.102"  # Replace with the actual IP address of the device

from python_zatobox.vanubus import Vanubus
ip_adress = "192.168.68.103"

client = Vanubus(ip_adress)
infodata =client.request_all_info()


if infodata == None:
    return 

while True:
    sensorids = []
    for sensordata in infodata.sensordata:
        sensorids.append(sensordata.id)
    
    data = client.getdata(sensorids)
    print(data[0])
    time.sleep(5)

```

