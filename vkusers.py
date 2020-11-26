#!/usr/bin/python3.4

from sys import argv
import requests
import jsonlines

def collect_vk(group, count=1000):
    users = []
    fname = 'vkusers.json'
    offset = 0

    while len(users) < count:
        r = requests.get('https://api.vk.com/method/groups.getMembers', 
                            params={'group_id': group, 'count' : 1000, 'offset': offset})
        resp = r.json()
        accounts = resp['response']['users']
        s = ",".join(map(str, accounts))
        r = requests.post("https://api.vk.com/method/users.get", 
                            data={'user_ids': s, 'fields':'bdate', 'v':5.62})
        resp = r.json()
        info = resp['response']
        users += list(filter(lambda u: u.get("deactivated") is None, info))
        offset += 1001

    print('Save %d users to %s file ' % (len(users), fname))
    with jsonlines.open(fname, mode='w') as writer:
        writer.write_all(users)

def main():
    group_id = 83388025  # default group
    if len(argv) > 1 and argv[1].isdigit():
        group_id = argv[1]
    print('Processing users from group %d' % group_id)
    collect_vk(group_id)

if __name__ == '__main__':
    main()
