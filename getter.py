import json
import requests

config = json.load(open('config.json', 'r'))

npt = ""
s = {
	shinyvotes = {},
	vidname = "",
	vidcomments = 0
}
# S Example
seg = 