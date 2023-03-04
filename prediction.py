import requests
import json
import datetime
from datetime import datetime as dt


date = datetime.date.today()

time = str(dt.now())
metaData = {}


def fetchResponse(imgURL):
	data = requests.get(imgURL).content;

	url = "https://agrithon-backend-production-e144.up.railway.app/predict"
	print(data)

	response = requests.post(url,files = {"image": data})

	if response.status_code==200:
		data = response.json()
	else:
		print("Unknown Error Occured")
	getMetaData(data)
	print(getMetaData(data))
	return getMetaData(data) 
	


def writeLog(metaData):
	f = open(str(date)+"log.db","ab")

	f.write(json.dumps(f"Time %s "%(time)).encode("utf-8"))
	f.write(b" \n")

	f.write(json.dumps(metaData).encode("utf-8"))
	f.write(b" \n")
	f.write(b" \n")
	f.write(b" \n")

	f.close()

def getMetaData(data):
	


	indices = ["Grassy Shoots","Healthy","Mites","Ring Spot","Yellow Leaf Disease"]


	desc = {"Grassy Shoots" : "Phytoplasma-infected sugarcane plants show a proliferation of tillers, which give it typical grassy appearance, hence the name grassy shoot disease. The leaves of infected plants do not produce chlorophyll, and therefore appear white or creamy yellow. The leaf veins turn white first as the phytoplasma resides in leaf phloem tissue. Symptoms at the early stage of the plant life cycle include leaf chlorosis, mainly at the central leaf whorl. Infected plants do not have the capacity to produce food in the absence of chlorophyll, which results in no cane formation." ,
	"Healthy" : "Your plant is perfectly fine and their is nothing alarming about it.Although if you want you can connect to an expert in order to verify it completely. Happy Gardening!!",
	"Mites" : "The mites feed by scraping the epidermis and sucking the juice. Heavily infested leaves give a sickly appearance and later dry up completely. Colonies appear grayish due to webbing, cast skins and soil particles caught in the webbing under the surface of the leaf.",
	"Ring Spot" : "Ring spot is a common disease that occurs in all sugarcane growing regions of the world. The disease usually only affects older leaves and as a consequence has no economic impact on crop yields. Ring spot is caused by the fungus Leptosphaeria sacchari.",
	"Yellow Leaf Disease" : "Yellow leaf disease (YLD) is a recently identified disease of sugarcane, affecting sugarcane production significantly in all sugarcane growing areas of the world. Yellow leaf disease (YLD) of sugarcane was first reported in Hamakua (Hawaii) on variety H65-0782 in 1989 as yellow leaf syndrome and subsequently from the United States mainland and many other sugarcane growing countries. The disease is reported worldwide in more than 30 countries."}


	control = {"Grassy Shoots" : "Moist hot air treatment of sets is suggested to control infection\n Phytoplasma infection also spreads through insect vectors; it is, therefore, important to control them." , "Healthy" : "None" , "Mites" : "A thysanopterous predator known as Scolothrips indicus Pr is a natural enemy capable of destroying the mite-eggs within the webs. Spray the crop with lime-sulphur, or fish oil rosin soap.\n Spraying with Kelthane can also be effective.",
	"Ring Spot" : " Use Calcium Silicate Slag as a soil amendment to reduce ring spot severity. \n Always consider an integrated approach with preventive measures together with biological treatments, if available. As of today, no chemical control methods have been developed against these fungi.",
	"Yellow Leaf Disease" :'''Selection of disease free setts for planting 
	Field should be maintain with proper hygiene 
	Application proper nutritional management and use resistant varieties.
	To avoid this disease first plant the setts in nursery and then transplant to main field.
	Selection of tissue culture plant especially meristem culture plant is used for planting in field'''}

	metaData["Disease"]=indices[int(data['class_index'])]

	metaData["Probab"] = str(float(data['probability'])*100)

	metaData["Desc"] = desc[metaData["Disease"]]

	metaData["Control"] = control[metaData["Disease"]]

	return metaData
		
	writeLog(metaData)


if __name__ == "__main__":
	print(date,end=' ')
	print("Connecting to API ")
	fetchResponse()
