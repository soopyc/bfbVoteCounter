import json
import requests

key = "AIzaSyBmrmKQWJ38rv7MnjtDFdmaDSXQEubnSh8"
config = json.load(open('config.json', 'r'))

npt = ""
s = {
	shinyvotes = {},
	vidname = "",
	vidcomments = 0
}

vi = requests.get(f"https://content.googleapis.com/youtube/v3/videos?part=snippet,statistics&id= &key={key}")

# Example
seg = {
	shinyvotes = {
		"RandomUsername": 5,
		"iConker": 33,
		"george Source": 42
	}
	vidinfo = {
		"title": "vi['items'][0]['snippet']['title']",
		"publish": "vi['items'][0]['snippet']"
	}
}

def 