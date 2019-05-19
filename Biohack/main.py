from flask import Flask, redirect, request, render_template
import json
import time
import requests
import databaseAccess

app = Flask(__name__)

app.foodItem = "corn"
app.allergyList = []

@app.route("/")
def main():
	ingredients = []
	hazard = []
	try:
		name, ids = databaseAccess.getFoodName(app.foodItem)
		for value in ids:
			ingredientString = databaseAccess.getIngredients(value, app.allergyList)
			head, sep, tail = ingredientString.partition('...') 
			ingredients.append(tail)
			hazard.append(head)
		if(app.foodItem == "corn"):
			return render_template('splash.html', allergyList=app.allergyList)
		else:
			return render_template('landing.html', data=zip(name, ingredients, hazard), allergyList=app.allergyList)
	except:
		return render_template('sorry.html')

@app.route("/foodSearch", methods=['POST', 'GET'])
def foodSearch():
	if request.method == 'POST':
		app.foodItem = request.form['foodInput']
	return redirect('/')

@app.route("/allergyInput", methods=['POST', 'GET'])
def allergyInput():
	if request.method == 'POST':
		response = request.form['allergyInput'].upper()
		if(',' in response):
			result = [x.strip() for x in response.split(',')]
			for value in result:
				if value not in app.allergyList:
					app.allergyList.append(value)
		else:
			if response not in app.allergyList:
				app.allergyList.append(response)
	return redirect('/')

@app.route("/allergyClear", methods=['POST', 'GET'])
def clearAllergy():
	app.allergyList.clear();
	return redirect('/')

@app.route("/backHome", methods=['POST', 'GET'])
def backHome():
	app.foodItem = "corn"
	return redirect('/')

@app.route("/removeBadge/<badgeName>", methods=['POST', 'GET'])
def removeBadge(badgeName):
	app.allergyList.remove(badgeName)
	return	redirect('/')

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0", threaded=True)
