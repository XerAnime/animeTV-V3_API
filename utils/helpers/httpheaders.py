import random

f = open("utils/useragents.txt","r")
useragentslist = f.read().split("\n")
f.close()

def request_headers():
    headers = {"User-Agent" : random.choice(useragentslist)}
    return headers