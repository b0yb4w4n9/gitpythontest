#!/bin/sh

#python -m pip install gitpython
#install https://git-scm.com/download
#environment variable: GIT_PYTHON_GIT_EXECUTABLE = git executable
#git remote set-url origin git@bitbucket.org:threattrack/avlabs-threat-research.git
#follow steps here: https://confluence.atlassian.com/bitbucket/set-up-an-ssh-key-728138079.html
#ssh and ssh-keygen tools are located in /usr/bin folder (in windows under programfiles\git\usr\bin)

import git
import datetime
from email.MIMEMultipart import MIMEMultipart
import os
from email.mime.text import MIMEText
import smtplib
from email.MIMEBase import MIMEBase
from email import Encoders

def notifybyemail(attachmentes):

    USERNAME = 'tts.maltrieve@threattrack.com'
    PASSWORD = 'S@mpl3s0urc!ng'
    SUBJECT = '[Test] Diff' + str(datetime.datetime.now())
    #EMAIL_SERVER = '10.139.102.30' #
    EMAIL_SERVER = 'smtp.threattrack.com'
    EMAIL_FROM = 'mister.pogi@threattrack.com'
    EMAIL_TO = ['reginald.wong@vipre.com','Nico.Yturriaga@vipre.com']

    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT 
    msg['From'] = EMAIL_FROM
    msg['To'] = ', '.join(EMAIL_TO)

    print "Sending this data via "+EMAIL_SERVER

    body = 'walang laman.' + "\n"
    if attachmentes != None:
        if os.path.getsize(attachmentes) != 0:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(attachmentes, "rb").read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="'+attachmentes+'"')
            msg.attach(part)
            body = 'The hills are alive with the sound of mucus.' + "\n"

    print msg
    print "\nSending... "

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(EMAIL_SERVER)
    server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

    print "Done sending\n"

def checkin_updates(path):
    git_repo = git.Repo(path, search_parent_directories=True)
    #git_repo.checkout('HEAD', b='master')
    git_root = git_repo.git.rev_parse("--show-toplevel")
    print git_root
    #print git_repo.git.status()
    status = git_repo.git.status()
    print status
    updates = False
    if "nothing to commit" not in status:
        #git_repo.git.add(update=True) #<-- does not add untracked
        git_repo.git.add(A=True) #<-- adds untracked
        git_repo.index.commit('[test] gitpython')
        git_repo.git.push("origin","master")
        print git_repo.git.status()
        updates = True
    return updates

def git_diff(path):
    git_repo = git.Repo(path)
    git_tree = git_repo.head.commit.tree
    #diff = git_repo.git.diff(git_tree)
    diff = git_repo.git.diff(r'HEAD^')
    return diff
    
if __name__ == "__main__":
    #checkin_updates(r'D:\VMHostShare\Projects\avlabs-threat-research')
    if checkin_updates(r'D:\Work\Projects\IDS\gitpython\gitpythontest'):
        updates = git_diff(r'D:\Work\Projects\IDS\gitpython\gitpythontest')
        open("updates_diff.txt", "wb").write(updates)
        notifybyemail("updates_diff.txt")
    else:
        notifybyemail(None)
