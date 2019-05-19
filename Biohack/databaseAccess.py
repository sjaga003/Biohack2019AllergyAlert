import requests
import json

def getFoodName(foodItem):
	food = []
	ids = []
	foodList = requests.get('https://api.nal.usda.gov/ndb/search/?format=json&q='+ foodItem +'&sort=r&ds=Branded+Food+Products&max=15&offset=0&api_key=JnvMcZzPi86ogoBuOcOXFhtoABkMZTLRvJSS8HnU')
	foodList = foodList.json()['list']['item']
	for item in foodList:
		head, sep, tail = item['name'].partition(', UPC: ') 
		food.append(head)
	for item in foodList:
		head, sep, tail = item['ndbno'].partition(', UPC: ') 
		ids.append(head)
	return food, ids


def getIngredients(itemId, allergies):
	food = requests.get('https://api.nal.usda.gov/ndb/reports/?ndbno='+ itemId +'&type=b&format=json&api_key=JnvMcZzPi86ogoBuOcOXFhtoABkMZTLRvJSS8HnU')
	food = food.json()['report']['food']['ing']['desc']
	cnt = 0
	for allergy in allergies:
		if(food.find(allergy) > -1):
			cnt = cnt + 1
	if(cnt > 0):
		food = "red..." + food
	else:
		food = "green..." + food
	return food

		