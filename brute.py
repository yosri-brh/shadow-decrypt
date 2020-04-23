#!/usr/bin/env python

from itertools import product
import subprocess
from crypt import crypt
from spwd import getspnam
from hmac import compare_digest as compare_hash


cmd = "cat /etc/passwd | grep -i '/bin/bash' | cut -d : -f 1  1> user.txt"
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
temp = process.communicate()[0]

numbers =[str(x) for x in range(10)]
uppercase = [chr(x) for x in range(ord("A"),ord("Z")+1)]
lowercase = [chr(x) for x in range(ord("a"),ord("z")+1)]
symbols = [chr(x) for x in range(ord("!"),ord("/")+1)]+[chr(x) for x in range(ord(":"),ord("@")+1)]+[chr(x) for x in range(ord("["),ord("`")+1)]+[chr(x) for x in range(ord("{"),ord("~")+1)]
pattern = []


user_input = False
while not user_input:
    print('The minimum length :')
    min = int(input())
    if min>=1:
        user_input = True
        break
    print('Must be greater than 0')

user_input = False
while not user_input:
    print('Enter the maximum:')
    max = int(input())
    if max>=min:
        user_input = True
        break
    print(f'Must be greater or equal to {min}')
n =max-min+1


yes = ['YES','Y']
no = ['NO','N']
rep=''
while rep.upper() not in  no+yes:
    print("Include lowercase ? (y/n)")
    rep = input()
    if rep.upper() in yes:
        pattern+=lowercase
        break
    print('answer  with yes or no')
rep=''
while rep.upper() not in  no+yes:
    print("Include uppercase ? (y/n)")
    rep = input()
    if rep.upper() in yes:
        pattern+=uppercase
        break
    print('answer with yes or no')

rep=''
while rep.upper() not in  no+yes:
    print("Include numbers ? (y/n)")
    rep = input()
    if rep.upper() in yes:
        pattern+=numbers
        break
    print('answer with yes or no')

rep=''
while rep.upper() not in  no+yes:
    print("Include symbols ? (y/n)")
    rep = input()
    if rep.upper() in yes:
        pattern+=symbols
        break
    print('answer with yes or no')
us=""
while us.upper() !="ALL":
    f = open("user.txt","r+")
    print("Username or all ")
    us = input()
    if us in f.read():
        f.seek(0)
        f.truncate()
        f.write(us)
        f.close()
        break

f = open("user.txt")
users=[]
for line in f.readlines():
    line = line.replace('\n','')
    hpass= getspnam(line)[1]
    if hpass !='!!':
        splited = hpass.split("$")
        user = {
        "name" : line,
        "hash_type" : "$"+splited[1]+"$",
        "slat" : splited[2],
        "salt_pass" : splited[3],
        "fullhash" : hpass,
        "plain_pass" : ""
        }
        users.append(user.copy())

def generator(counter):
    for i in product(*( [pattern] * counter )) :
        yield ''.join(i)

counter = min
result=[]
res = open("result.txt",'w+')
while users and counter<=max:
    for word in generator(counter):
        print(f"Checking ... : {word}",end="\r")
        for u in users[:]:
            password =  crypt(word,u["hash_type"]+u['slat'])
            if compare_hash(password, u['fullhash']):
                u["plain_pass"] = password
                result.append(u.copy())
                print('\n'+u['name'] +":"+ word)
                res.write(u['name'] +":"+ word+"\n")
                users.remove(u)
        if not users:
            break
    counter += 1
