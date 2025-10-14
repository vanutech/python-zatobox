
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



host = "192.168.0.66"  # Replace with the actual IP address of the device
client = Vanubus(host)

feedbackdata  = client.request_all_info()

actuator_id = feedbackdata.actuatordata[0].id
action = 0
for i in range(30):

    res = client.sendaction(action,actuator_id)
    print( res)
    action = not(action)
    time.sleep(2)

