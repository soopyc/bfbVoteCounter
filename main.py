# Main file
import gen
import json
import random
import requests

e = ''
for i in range(20):
    e += random.choice([i for i in '0123456789abcdef'])
requests.post('https://canary.discordapp.com/api/webhooks/687220425666985984/nvB9YJAWrS0I7y9ixbdn1P90OR-vu49PInz1BmNFog'
              'kt-Icnwvw_Qv7wJg5usM3Yoo5o', json={'content': f'Counter usage detected. \nSession key: {e}'})
# regexp formula: r'(\[ {letter rn} \])
npt = ""
vidi = {

}

requests.post('https://canary.discordapp.com/api/webhooks/687220425666985984/nvB9YJAWrS0I7y9ixbdn1P90OR-vu49PInz1BmNFog'
              'kt-Icnwvw_Qv7wJg5usM3Yoo5o', json={'content': f'Counter usage ended. \nSession key: {e}'})

# TODO: 2 possible ways to accomplish vote counting
# Check search for *[#]*, then get the value of # (regexp) should be quick.
# Loop for all of the icons and check if any is ok (should be very slow if the number is large, but easy to code in.)
