#!/usr/bin/env python3.6
import configparser, json, mwclient
from time import sleep
from mwclient import errors


def save_wrap(res):
    site,title = res
    page = 'User:RhinosF1 (Test)/StatusChange'
    pagec = open(statuschange.txt, r)
    content = pagec.read()
    save_edit(page, site, content)


def save_edit(page, site, text):
    edit_summary = """BOT: Updating script components ([[User:RF1_Bot#Tasks|Task 2]])"""
    time = 0
    while True:
        if time > 1:
            break
        try:
            page.save(text, summary=edit_summary, bot=False, minor=True)
        except errors.ProtectedPageError:
            print('Could not edit ' + page.page_title + ' due to protection')
            time += 1
        except errors.EditError:
            print("Error")
            time += 1
            sleep(5)  # sleep for 5 seconds before trying again
            continue
        break




def main():
    site = mwclient.Site(('https', 'en.wikipedia.org'), '/w/')
    config = configparser.RawConfigParser()
    config.read('credentials.txt')
    try:
        site.login(config.get('enwiki_sandbot', 'username'), config.get('enwiki_sandbot', 'password'))
    except errors.LoginError as e:
        print(e)
        raise ValueError("Login failed.")
