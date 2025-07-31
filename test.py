
import time

from python_zatobox.vanubus import Vanubus,  InputRegBattery , InputRegMainMeter, InputRegGasMeter, InputRegCharger, InputRegPV, InputRegUsage

# from zeroconf import ServiceBrowser, ServiceListener, Zeroconf


# class _MyListener(ServiceListener):
#     def __init__(self):
#         self.services = []

#     def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
#         print(f"Service {name} updated")

#     def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
#         print(f"Service {name} removed")

#     def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
#         info = zc.get_service_info(type_, name)
#         if info:
#             ip = ".".join(map(str, info.addresses[0]))
#             splitname = name.split('.')
#             service_data = {
#                 "name": splitname[0],
#                 "ip": ip,
#                 "port": info.port,
#                 "properties": info.properties
#             }
#             self.services.append(service_data)

# def discover_zt_devices(timeout = 3) -> list:

#     zeroconf = Zeroconf()
#     listener = _MyListener()
#     browser = ServiceBrowser(zeroconf, "_vanubus._tcp.local.", listener)

#     waittime = 0
#     while(waittime < timeout):            
#         time.sleep(0.1)
#         waittime = waittime + 0.1
    
#     zeroconf.close()

#     return listener.services




# discovered_devices = discover_zt_devices()


    
# options = {device["name"]: device["name"] for device in discovered_devices}
# print(options)



host = "192.168.68.109"  # Replace with the actual IP address of the device
client = Vanubus(host)

feedbackdata  = client.request_all_info()

if feedbackdata != None and len(feedbackdata.sensordata) > 0:
    listofids = [i.id for i in  feedbackdata.sensordata]

    devicesn  = "sdfsfdd"
    coordinator_data = {f"{devicesn}-{item}":  {"name": "sensor", "id": item} for item in listofids}


    for i in range(30):
        sensorsdata  = client.getdata(listofids)

        coordinator_data = {}
        for sensor in sensorsdata:


            for attribute in sensor.attributes:
                
                if (not(attribute.startswith("reserve"))):
                    value = getattr(sensor, attribute)
                    coordinator_data[f"{devicesn}-{sensor.id}-{attribute}"] =  {"value": value ,"name": "sensor", "id": sensor.id}

            # match sensor:
            #     case InputRegMainMeter():        
                            
            #         coordinator_data[f"{devicesn}-{sensor.id}-power"] =  {"value": sensor.power ,"name": "sensor", "id": sensor.id}
            #         coordinator_data[f"{devicesn}-{sensor.id}-power"] =  {"value": sensor ,"name": "sensor", "id": sensor.id}

 
            #     case InputRegGasMeter():     
            #         print("The color is red.")
            #     case InputRegBattery():     
            #         print("The color is red.")
            #     case InputRegPV():     
            #         print("The color is red.")
            #     case InputRegCharger():     
            #         print("The color is red.")
            #     case InputRegUsage():     
            #         print("The color is red.")
        
        print( coordinator_data)

        coordinator_data = {f"{devicesn}-{sensor.id}":  {"value": sensor.power ,"name": "sensor", "id": sensor.id} for sensor in sensorsdata}


        print( coordinator_data)
        time.sleep(2)

