#!/usr/bin/python3.4
import sys
import requests
import jsonlines
if (len(sys.argv) > 1) and (sys.argv[1].isdigit()):
    groupid=sys.argv[1]
else:
    groupid=83388025
print('Processing users from group',groupid)
n_users=0
offset=0
users=[]
while n_users<1000:
    r=requests.get('https://api.vk.com/method/groups.getMembers',params={'group_id':groupid,'count':1000,'offset': offset})
    response=r.json()
    userlist=response['response']['users']
    userstr=",".join(map(str, userlist))
    r = requests.post("https://api.vk.com/method/users.get", data={'user_ids':userstr,'fields':'bdate','v':5.62})
    response=r.json()
    usersall=response['response']
    users+=list(filter(lambda u: u.get("deactivated") is None, usersall))
    n_users=len(users)
    offset+=1001
print('Saved ',len(users),' users to file vkusers.jsonl')
with jsonlines.open('vkusers.jsonl', mode='w') as writer:
    writer.write_all(users)
