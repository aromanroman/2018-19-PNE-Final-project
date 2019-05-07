# This is a the client.
import http.client
import json


PORT = 8000
SERVER = 'localhost'

print("\nConnecting to server: {}:{}\n".format(SERVER, PORT))

# Connect with the server
conn = http.client.HTTPConnection(SERVER, PORT)


# 1st part
print("you will get the list of the the genes with the limit ")
conn.request("GET", "/listSpecies?limit=1&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)

# 2nd part
print("you will get the information about the karyotype of the specie introduced ")
conn.request("GET", "/karyotype?specie=mouse&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)

# 3rd part
print("you will get the length of the chromosome introduced of the specie selected ")
conn.request("GET", "/chromosomeLength?specie=mouse&chromo=1&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)

# 4th part
print("you will get the sequence of the given human gene ")
conn.request("GET", "/geneSeq?json=1&gene=FRAT1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)


# 5th part
print("you will get the information of the given human gene ")
conn.request("GET", "/geneInfo?json=1&gene=FRAT1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)


# 6th part
print("you will get the calculation of the given human gene ")
conn.request("GET", "/geneCal?gene=FRAT1&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)

# 7th part
print("you will get the list of the genes of the chromosome introduced in the start and end position selected")
conn.request("GET", "/geneList?chromo=1&start=3&end=300000&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)
