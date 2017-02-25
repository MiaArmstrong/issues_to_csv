#!/usr/bin/env python
"""
Exports Issues from a specified repository to a CSV file
Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.
Last Updated 1/10/2017 by Mia Armstrong
"""
import csv
import requests
import json


txtout = open('data.json', 'w')


def menu(answer):
    if answer != 4:
        print('***Menu***')
        print('1) Export all issues from a Repository')
        print('2) Export issues sorted by Label')
        print('3) Help')
        print('4) Exit')
        answer = input('Make a selection (1 - 4): ')
        if answer == '1':
            write_issues_all(validate_info())
        elif answer == '2':
            write_issues_label(validate_info())
        elif answer == '3':
            help_about()
        elif answer == '4':
            exit()
        else:
            print('Please try again.')


def validate_info():
    global github_user
    github_user = input('Enter your Github user ID: ')
    global github_password
    github_password = input('Enter your Github password: ')
    print('Enter the company/user name and the Repository name')
    global repo
    repo = input('(Format is username/repo, ex: ultratesting/knowledge-tree): ')   #format is username/repo
    global issues_for_repo
    issues_for_repo = 'https://api.github.com/repos/%s/issues' % repo
    ARGS = "?state=all"
    global authorization
    authorization = (github_user, github_password)
    global response
    response = requests.get(issues_for_repo + ARGS, auth=authorization)
    file_setup()
    return response


def file_setup():
    csvfilename = '%s-issues.csv' % (repo.replace('/', '-'))
    global csvfile
    csvfile = open(csvfilename, 'w', newline='')
    global csvout
    csvout = csv.writer(csvfile)
    csvout.writerow(('Labels', 'id', 'Title', 'Body', 'State', 'Created At', 'Updated At', 'Tester'))


def write_issues_all(r):
    #output a list of issues to csv
    if not r.status_code == 200:
        raise Exception(r.status_code)

    json.dump(r.json(), txtout, sort_keys=True, indent=4)

    for issue in r.json():
        global issues
        issues = 0
        issues += 1
        csvout.writerow(['', issue['number'], issue['title'].encode('utf-8'), issue['body'].encode('utf-8'),issue['state'].encode('utf-8'), issue['created_at'], issue['updated_at'], issue['user']['login']])

    if 'link' in r.headers:
        pages = dict(
            [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                [link.split(';') for link in
                    r.headers['link'].split(',')]])
        print("***")
        print(pages)
        while 'last' in pages and 'next' in pages:
            print(pages['next'])
            r = requests.get(pages['next'], auth=authorization)
            write_issues_all(r)
            if pages['next'] == pages['last']:
                break
            pages = dict(
            [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                [link.split(';') for link in
                    r.headers['link'].split(',')]])
    csvout.writerow(['Total', issues])
    file_close()


def write_issues_label(r):
    #output a list of issues to csv
    if not r.status_code == 200:
        raise Exception(r.status_code)

    json.dump(r.json(), txtout, sort_keys=True, indent=4)

    for issue in r.json():
        global issues
        issues = 0
        labels = issue['labels']
        for label in labels:
            label_name = input('Enter name of Label: ')
            if label['name'] == label_name:
                issues += 1
                csvout.writerow([label['name'], issue['number'], issue['title'].encode('utf-8'), issue['body'].encode('utf-8'),issue['state'].encode('utf-8'), issue['created_at'], issue['updated_at'], issue['user']['login']])
    if 'link' in r.headers:
        pages = dict(
            [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                [link.split(';') for link in
                    r.headers['link'].split(',')]])
        print("***")
        print(pages)
        while 'last' in pages and 'next' in pages:
            print(pages['next'])
            r = requests.get(pages['next'], auth=authorization)
            write_issues_all(r)
            if pages['next'] == pages['last']:
                break
            pages = dict(
            [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                [link.split(';') for link in
                    r.headers['link'].split(',')]])
    csvout.writerow(['Total', issues])
    file_close()


def help_about():
    print('\n\nWelcome to the Help/ About section')
    print('Please select a topic from the menu')
    print('1) Error Codes')
    print('2) How to input repository information')
    print('3) About this program')
    print('4) Exit Help')
    ans = input('Your selection: ')

    if ans == '1':
        print('Error Codes: ')
        print('Some common error codes that you may receive are 404 and 401: these codes indicate that there may be an'
              'error in the user name, password, or repository you provided. Please check these and try again.')
        print('To learn more about error codes go to https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html')
        help_about()
    elif ans == '2':
        print('How to input repository information: ')
        help_about()
    elif ans == '3':
        print('About this program')
        help_about()
    elif ans == '4':
        menu(0)
    else:
        print ("Please try again.")
        help_about()


def file_close():
    csvfile.close()
    txtout.close()
    exit()

menu(0)

#kick off the event loop
#root.mainloop()

