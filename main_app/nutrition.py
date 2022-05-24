import requests

def get(query):
	url = "https://calorieninjas.p.rapidapi.com/v1/nutrition"
	querystring = {"query":query}
	headers = {
		"X-RapidAPI-Host": "calorieninjas.p.rapidapi.com",
		"X-RapidAPI-Key": "b7cdab9648msh48c8c9f16a4b05dp1a5a8ajsn60e2f660bcac"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	return response.json()

print(get('tomato'))