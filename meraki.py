#python3
import requests
import simplejson
#import API key from your config file
from config import merakiAPIKey


#Set up default headers
headers = {
    'X-Cisco-Meraki-API-Key': merakiAPIKey,
    'Content-Type': 'application/json',
    'Accept': '*/*'
}
#getOrg function gets the OrgId
def getOrg():
    r= requests.get('https://api.meraki.com/api/v0/organizations', headers=headers)
    c = simplejson.loads(r.text)
    orgId = c[0]['id']
    return  orgId

#getNet function gets the only network ID in our environment
def getNet():
    r = requests.get('https://api.meraki.com/api/v0/organizations/'+ getOrg() +'/networks', headers=headers)
    c = simplejson.loads(r.text)
    netId = c[0]['id']
    return netId


#findDevice takes an email address and returns devices IDs that are associated with that address
def findDevice(email):
    d = requests.get('https://api.meraki.com/api/v0/networks/'+ getNet() +'/sm/devices?fields=name,id,ownerEmail' , headers=headers)
    dev = simplejson.loads(d.text)
    jsList = dev["devices"]
    idList = []
    for i in jsList:
        oemail = i.get('ownerEmail', 'none')
        if oemail == email:
            idList.append(i['id'])
    return idList
        

#lockDevice takes an email address, which it passes to findDevice. It takes the list that it gets back from findDevice and locks those devices
def lockDevice(email):
    lockList = findDevice(email) 

    #This loop should work but it doesn't See https://documenter.getpostman.com/view/7928889/SVmsVg6K?version=latest#5c4e48b6-1a5f-4c60-ae80-26bf1d64ec09
    #I've tried this using two differet formatting methods for the ID. Both fail if I roll through the loop.
    for i in lockList:
        payload = "\'{\"ids\":\""
        payload += i
        payload += "\"}\'"
        print(payload)
        response = requests.request("PUT", 'https://api.meraki.com/api/v0/networks/'+ getNet() +'/sm/devices/lock' , headers=headers, data= payload)
        print(response.text.encode('utf8'))
        # lockstr = "\"{\r\n \"ids\":"
        # lockstr += "\"\\\"" + i + "\\\"\"\r\n}\""
        # print(lockstr)
    #despite the documentation, this is how the ID needs to be formatted. But I can't figure out how to add a new lock code.   
    # payload = '{"ids":"575334852397107558"}'
    # response = requests.request("PUT", 'https://api.meraki.com/api/v0/networks/'+ getNet() +'/sm/devices/lock' , headers=headers, data= payload)
    
    



lockDevice("danny.mccaslin@frederickwater.com")

