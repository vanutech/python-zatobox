

import socket

from zeroconf import ServiceBrowser, ServiceListener, Zeroconf

import time

import struct

class SensorData:
    def __init__(self, data: bytes) -> None:
    
        # Decode the bytes using little-endian byte order
        decoded_value = int.from_bytes( data[0:4], byteorder='little')
       
        match decoded_value:
            case 5:
                for i in range(30):

                    # Decode the bytes using little-endian byte order
                    decoded_value = int.from_bytes( data[(i+1)*4:(i+2)*4], byteorder='little')

                    # Convert the integer value to a float
                    float_value = struct.unpack('f', struct.pack('I', decoded_value))[0]
                    print(float_value)




class Vanubus:
    def __init__(self, host, port=3333) -> None:
        isipadress : bool = False
        try:
            socket.inet_aton(host)
            # legal
            isipadress = True
        except socket.error:
            # Not legal
            isipadress = False

        if (isipadress):
            self.ip_address = host
            self.port = port
        else:
            try:
                ip = socket.gethostbyname(host)
                print(f"{host} resolved to {ip}")
                self.ip_address = ip
            except socket.gaierror:
                print(f"Could not resolve {host}")
        
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setipadress(self, ipadress):
        self.ip_address = ipadress

    def discover(self, timeout = 3) -> list:

        zeroconf = Zeroconf()
        listener = self._MyListener()
        browser = ServiceBrowser(zeroconf, "_vanubus._tcp.local.", listener)

        waittime = 0
        while(waittime < timeout):            
            time.sleep(0.1)
            waittime = waittime + 0.1
        
        zeroconf.close()

        return listener.services

    def getdata(self, sensorids = []):
        if (not(self._is_connected())):
            connected = self._connect()
            if (not(connected)):
                return 

        # Create tx_buffer of 64 bytes, initialized with zeros
        tx_buffer = bytearray(64)

        # Set id for request
        tx_buffer[0] = 1

        # Fill the buffer with client ids, starting at index 1
        for i in range(len(sensorids)):
            tx_buffer[i + 1] = sensorids[i]  # or clientdata[i].id if objects

        # Send the buffer minus the last byte (63 bytes)
        try:
            sent_bytes = self.tcp_socket.send(tx_buffer[:63])
            print(f"Sent {sent_bytes} bytes")
        except socket.error as e:
            print(f"Socket send error: {e}")


        try:
            while True:
                data = self.tcp_socket.recv(1024)
                if data:
                    self._decode_rx_buffer(data, 1)
                    break
                time.sleep(1)
        except Exception as e:
            print(f"Error receiving data: {e}")
            
    def _decode_rx_buffer(self,  data : bytes, type):
        hex_representation = data.hex()
        print(hex_representation)  # Output: '01020304'


        match type:
            case 1:
                sensorsearch = True
                position = 0
                sensordataelength = (30*4 + 4)
                sensorlength = (len(data))/(sensordataelength)
                for i in range(round(sensorlength)):
                    sensorbytes = data[sensordataelength*i:sensordataelength*(i+1)]
                    print(sensorbytes)
                    sensor = SensorData(sensorbytes)
            case 2:
                return "two"

    def _is_connected(self) -> bool:
        try:
            # Check if socket is closed
            self.tcp_socket.getpeername()  # Raises error if not connected
        except socket.error:
            return False
        return True
    
    def _connect(self) -> bool:
        try:
            self.tcp_socket.connect((self.ip_address, self.port))
            print(f"Connected to {self.ip_address} on port {self.port}")
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
        
        return False


    def _listen(self):
        try:
            while True:
                data = self.tcp_socket.recv(1024)
                if not data:
                    break
                print(f"Received data: {data.decode('utf-8')}")
        except Exception as e:
            print(f"Error receiving data: {e}")
        finally:
            self.close()

    def _close(self):
        print("Closing socket")
        self.tcp_socket.close()

    class _MyListener(ServiceListener):
        def __init__(self):
            self.services = []

        def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
            print(f"Service {name} updated")

        def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
            print(f"Service {name} removed")

        def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
            info = zc.get_service_info(type_, name)
            if info:
                ip = ".".join(map(str, info.addresses[0]))
                splitname = name.split('.')
                service_data = {
                    "name": splitname[0],
                    "ip": ip,
                    "port": info.port,
                    "properties": info.properties
                }
                self.services.append(service_data)


# Example usage
if __name__ == "__main__":
    host = "192.168.68.102"  # Replace with the actual IP address of the device
    client = Vanubus(host)

    test = client.discover()
    print(test)

    client.getdata([1,2,6])