from __future__ import print_function
from threading import Thread

import requests
import hexchat

__module_name__ = 'PastePreview'
__module_version__ = '1.0'
__module_description__ = 'Lurks into messages to find links to pastebin services'

PASTEBIN_SERVICES = [
    [ 'https://pastebin.mozilla.org/', 'https://pastebin.mozilla.org/?dl='],
    [ 'https://irccloud.mozilla.com/pastebin/', 'https://irccloud.mozilla.com/pastebin/raw/']
]

def p(msg):
    print("\00304", __module_name__, msg, ".\003")

def s(msg):
    print("\00302", msg, "\003")

def c(id, msg):
    for l in msg.split('\n'):
        hexchat.emit_print("Channel Message", "<" + id + ">", "\00303" + l + "\003")

def lurk_pastebin(word, word_eol, event):
    user = word[0].strip()
    mess = word[1].strip()
    service = filter(lambda x: x[0] in mess, PASTEBIN_SERVICES)
    if len(service) == 0 or len(service) > 1:
        return

    service = service[0]
    pasteid = mess[mess.find(service[0]):].replace(service[0], "")
    rawurl = service[1] + pasteid
    r = requests.get(rawurl)
    if r.status_code != 200:
        s("Request failed for %s with %d" % (rawurl, r.status_code))
        return

    s("%s:" % (rawurl))
    c(pasteid, r.text)
    return

def new_msg(word, word_eol, event):
    t = Thread(target=lurk_pastebin, args=(word, word_eol, event, ))
    t.start()
    return None

hooks_new = ["Your Message", "Channel Message"]
for hook in hooks_new:
    hexchat.hook_print(hook, new_msg, hook, hexchat.PRI_LOWEST)

p("successfully loaded.")
