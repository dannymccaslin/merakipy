#python3
import requests
import simplejson

merakiAPIKey = "b9767658c5a56827060ec8dda3de347fcf9ab393"

headers = {
    'X-Cisco-Meraki-API-Key': merakiAPIKey,
    'Content-Type': 'application/json',
}

r= requests.get('https://dashboard.meraki.com/api/v0/organizations', headers=headers)

c = r.content
j = simplejson.loads(c)

orgId = j[0]['id']

n = requests.get('https://dashboard.meraki.com/api/v0/organizations/'+orgId+'/networks', headers=headers)

print(n.content)
c = n.content
j = simplejson.loads(c)
netId = j[0]['id']
print(netId)

d = requests.get('https://dashboard.meraki.com/api/v0/networks/'+netId+'/sm/devices?fields=name,id,ownerEmail', headers=headers)

dev = simplejson.loads(d.text)
print(d)
jsList = dev["devices"]
dannyiPhone = "575334852397107558"
#d = requests.get('https://dashboard.meraki.com/api/v0/networks/'+netId+'/sm/' +dannyiPhone+ '/cellularUsageHistory', headers=headers)
#dev = d.content
#print(jsList)
for i in jsList:
    print(f"Name: {i.get('name')} , ID: {i.get('id')} , Email: {i.get('ownerEmail','none listed')}")

 


