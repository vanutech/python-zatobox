

from datetime import datetime, timedelta


from python_zatobox.zatoboxcloud import ZatoboxCloud


cloud = ZatoboxCloud()

cloud.auth("test@vanutech.be", "test1234", "DEV")


list = cloud.getsensorslist()["succes"]

print(list)

today = datetime.now()

start_of_yesterday = datetime(year= today.year, month=today.month, day= today.day-5, hour= 0)
end_of_yesterday = datetime(year= today.year, month=today.month, day= today.day, hour= 0)

marketpricedata = cloud.getmarketpricedata(start_of_yesterday, end_of_yesterday)["succes"]
usagedata = cloud.getusageforcastdata()["succes"]

data = cloud.getsensordata('1', start_of_yesterday, end_of_yesterday)["succes"]


start_of_yesterday = datetime(year= today.year, month=today.month, day= today.day, hour= 0)
end_of_yesterday = datetime(year= today.year, month=today.month, day= today.day+1, hour= 0)
forecastdata = cloud.getforcastdata(start_of_yesterday, end_of_yesterday)["succes"]

print(forecastdata)
