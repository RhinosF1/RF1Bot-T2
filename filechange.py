# Pastebin xEWKC8sO
#!/usr/bin/env python3.6
import configparser, json, mwclient
from mwclient import errors
import JustIRC
import random
import requests
import re
import time
lastuser = ''
pages = ''

bot = JustIRC.IRCConnection()

def on_connect(bot):
    bot.set_nick("") #bot name goes here and on below line
    bot.send_user_packet("")

def on_welcome(bot):
    bot.send_message('NickServ', 'identify ') #enter bot password here
    print('Authed to NickServ')
    time.sleep(10)
    bot.join_channel('') #enter channel to be contolled from here
def save_wrap(site):
    print('line 9')
    global pages
    pagename1 = '' #enter pages to edit here - up to 5
    pagename2 = ''
    pagename3 = ''
    pagename4 = ''
    pagename5 = ''
    page1 = site.Pages[pagename1]
    page2 = site.Pages[pagename2]
    page3 = site.Pages[pagename3]
    page4 = site.Pages[pagename4]
    page5 = site.Pages[pagename5]
    pagec1 = open('statuschange.txt', 'r') #reads files for those pages - keep or change names but ones with these names are included in the repo
    print('Line 12')
    content1 = pagec1.read()
    pagec2 = open('statusmonitor.txt', 'r')
    content2 = pagec2.read()
    pagec3 = open('smdoc.txt', 'r')
    content3 = pagec3.read()
    pagec4 = open('ubx.txt', 'r')
    content4 = pagec4.read()
    pagec5 = open('clog.txt', 'r')
    content5 = pagec5.read()
    print('Line 13')
    print('Content: ' + content1)
    pages = pagename1
    save_edit(page1, site, content1) #calls edit function ## hash out any not needed ##
    pages = pagename2
    save_edit(page2, site, content2)
    pages = pagename3
    save_edit(page3, site, content3)
    pages = pagename4
    save_edit(page4, site, content4)
    pages = pagename5
    save_edit(page5, site, content5)
    print('Line 17')

def save_edit(page, site, content):
    import time
    global senders
    global pages
    time.sleep(5)
    edit_summary = """BOT: Updating script components ([[User:#Tasks|Task 2]]) - Requested by  using  on chat.freenode.net""" #complete this sentence or use variables if multiple operators
    times = 0
    while True:
        if times > 1:
            break
        try:
            page.save(content, summary=edit_summary, bot=False, minor=True)
            print('Line 27')
            bot.send_message('', senders + ": I've updated " + pages ) #add channel name as first param
        except errors.ProtectedPageError:
            print('Could not edit ' + page + ' due to protection')
            times += 1
        except errors.EditError:
            print("Error")
            times += 1
            time.sleep(5)  # sleep for 5 seconds before trying again
            continue
        break




def main():
    site = mwclient.Site(('https', 'en.wikipedia.org'), '/w/') #change this if site not enwiki ##works with all MW sites
    config = configparser.RawConfigParser()
    config.read('credentials.txt')
    print('Line 45')
    try:
        site.login(config.get('enwiki_sandbot', 'username'), config.get('enwiki_sandbot', 'password'))
    except errors.LoginError as e:
        print(e)
        raise ValueError("Login failed.")
    save_wrap(site)

def on_message(bot, channel, sender, message):
    global lastuser
    global senders
    if '!run' == message.lower():
        senders = sender
        if 'rhinosf1' == sender.lower():
            if __name__ == "__main__":
                main()
        else:
            if lastuser == sender.lower(): ##COMPLETE SENTENCES BELOW##
                bot.send_message(sender, 'You have been quited for misuse of ')
                bot.send_message('', (str(sender) + ':quited in , +z activated'))
                message = str('flags ##channel ' + sender + " -e+q")
                print(message)
                bot.send_message('ChanServ', message)
                message2 = 'quiet ##channel ' + sender
                print(message2)
                bot.send_message('ChanServ', message2)
                bot.send_message('ChanServ', 'set mlock ##channel +z')
            else:
                bot.send_message(sender, 'You can not use !run')
                bot.send_message('', (str(sender) + ' attempted to use !run'))
                lastuser = sender
    if  '!stop' == message.lower():
        if 'rhinosf1' == sender.lower():
            quit()
        else:
            if lastuser == sender.lower(): ##SAME AS ABOVE##
                bot.send_message(sender, 'You have been quited for misuse of ')
                bot.send_message('', (str(sender) + ':quited in , +z activated'))
                message = str('flags  ' + sender + " -e+q")
                print(message)
                bot.send_message('ChanServ', message)
                message2 = 'quiet  ' + sender
                print(message2)
                bot.send_message('ChanServ', message2)
                bot.send_message('ChanServ', 'set mlock  +z')
            else:
                bot.send_message(sender, 'You can not use !stop')
                bot.send_message('', (str(sender) + ' attempted to use !stop'))
                lastuser = sender

    
bot.on_connect.append(on_connect)
bot.on_welcome.append(on_welcome)
bot.on_public_message.append(on_message)
bot.connect("chat.freenode.net") ##CHANGE IF NETWORK NOT FREENODE
bot.run_loop()
