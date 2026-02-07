

from datetime import datetime, timedelta

import boto3

import jwt
from pycognito.aws_srp import AWSSRP
import requests



class ZatoboxCloud:
    def auth(self, username, password, devstage)->str:
        if devstage == "DEV":
            regionname = 'eu-north-1'
            appClientId = '427t8ch50nuhd9sf3dpgg7pb8g'
            user_pool_id = 'eu-north-1_gqc771sGU'

        # Initialize the Cognito client
        client = boto3.client(
            'cognito-idp',
            region_name=regionname  # Replace with your region
        )
        aws = AWSSRP(username=username, password=password, pool_id=user_pool_id,
                    client_id=appClientId, client=client)
        tokens = aws.authenticate_user()
                            
        # Extract the Access Token (Bearer Token)
        self.access_token = tokens['AuthenticationResult']['AccessToken']
        self.id_token = tokens['AuthenticationResult']['IdToken']
        
        # Decode the ID Token (no verification for simplicity; in production, verify the token)
        decoded_token = jwt.decode(self.id_token, options={"verify_signature": False})

        # Extract the 'sub' (user ID)
        user_id = decoded_token['sub']

        plantuserinfo = self.apicall("getuser", user_id)

        #olny normal users with one plant
        if ("succes" in plantuserinfo):
            self.plantid = plantuserinfo["succes"][0]["plantid"]["S"]
            return ""
        else: 
            return "auth fail"




    def apicall(self, stage:str, id: str, startdate:str = "", enddate:str = "", startidentifier:str = "", endidentifier:str = ""):
        baseurl = "https://apidev.zatobox.com/"

        API_ENDPOINT = baseurl + stage + "/" + id
        try:
            headers = {
                "Authorization": self.id_token,
                "Content-Type": "application/json"  # Adjust based on your API requirements
            }
            if startdate != "" and enddate != "":
                headers["startdate"] = startdate
                headers["enddate"] = enddate

            # Make the GET/POST request (adjust method as needed)
            response = requests.get(API_ENDPOINT, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                if "error" in response.json():
                    return response.json()
                
                if "Items" in response.json():
                    return {"succes": response.json()["Items"]}
                else:
                    return {"succes":response.json()}

            else:
                return {"error":response.status_code}

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    def getsensorslist(self):
        return self.apicall("getsensors", self.plantid) 


    def getsensordata(self, sensorid, starttime: datetime, endtime: datetime):


        start_epoch =str( int(starttime.timestamp() * 1000 ))
        end_epoch = str( int(endtime.timestamp() * 1000 ))

        return self.apicall("getdata", self.plantid + '_' + str(sensorid), startdate=start_epoch, enddate=end_epoch) 

    def getforcastdata(self , starttime: datetime, endtime: datetime):

        start_epoch =str( int(starttime.timestamp()  ))
        end_epoch = str( int(endtime.timestamp()  ))

        return self.apicall("forecast/forecast", self.plantid, startdate=start_epoch, enddate=end_epoch) 
