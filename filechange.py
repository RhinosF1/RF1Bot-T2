#!/usr/bin/env python3.6
import configparser, json, mwclient
from mwclient import errors
import JustIRC
import random
import requests
import re
import time
lastuser = ''

bot = JustIRC.IRCConnection()

def on_connect(bot):
    bot.set_nick("") #add bot name to both this and the below line
    bot.send_user_packet("")

def on_welcome(bot):
    bot.send_message('NickServ', 'identify ') #place NickServ password here
    print('Authed to NickServ')
    time.sleep(10)
    bot.join_channel('') #place channel to run in here
def save_wrap(site):
    print('line 9')
    page = site.Pages[''] #place page to run on in mediawiki here
    pagec = open('statuschange.txt', 'r')
    print('Line 12')
    content1 = pagec.read()
    print('Line 13')
    print('Content: ' + content1)
    time.sleep(5)
    save_edit(page, site, content1)
    print('Line 17')

def save_edit(page, site, content):
    edit_summary = """BOT: Updating script components ([[User:RF1_Bot#Tasks|Task 2]])"""
    time = 0
    while True:
        if time > 1:
            break
        try:
            page.save(content, summary=edit_summary, bot=False, minor=True)
            print('Line 27')
            bot.send_message('', " I've updated /statuschange") #message to send to IRC when complete here
        except errors.ProtectedPageError:
            print('Could not edit ' + page + ' due to protection')
            time += 1
        except errors.EditError:
            print("Error")
            time += 1
            time.sleep(5)  # sleep for 5 seconds before trying again
            continue
        break




def main():
    site = mwclient.Site(('https', 'en.wikipedia.org'), '/w/') #change if not editing enwiki here
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
    if '!run' == message.lower():
        if '' == sender.lower(): #add user that can command it here
            if __name__ == "__main__":
                main()
        else:
            if lastuser == sender.lower():
                bot.send_message(sender, 'You have been quited for misuse of ##wikimedia-statuschange')
                bot.send_message('', (str(sender) + ':quited in , +z activated')) #add user to alert and channel here
                message = str('flags  ' + sender + " -e+q") #add channel after flags
                print(message)
                bot.send_message('ChanServ', message)
                message2 = 'quiet  ' + sender #add channel after quiet
                print(message2)
                bot.send_message('ChanServ', message2)
                bot.send_message('ChanServ', 'set mlock  +z') #add channel after mlock here
            else:
                bot.send_message(sender, 'You can not use !run')
                bot.send_message('', (str(sender) + ' attempted to use !run')) #add operator here
                lastuser = sender

    
bot.on_connect.append(on_connect)
bot.on_welcome.append(on_welcome)
bot.on_public_message.append(on_message)
bot.connect("chat.freenode.net") #change if network not freenode
bot.run_loop()
