# -*- coding: utf-8-*-
import imaplib

''' 
mailserver = imaplib.IMAP4_SSL('imap.gmail.com', 993)
username = 'user'
password = 'password@'
mailserver.login(username, password)
 
status, count = mailserver.select('Inbox')
status, data = mailserver.fetch(count[0], '(UID BODY[TEXT])')
 
print data[0][1]
 
mailserver.close()
mailserver.logout()
'''

""" GMail archiver 1.1

This program will download and archive all you emails from GMail.
Simply enter your login and password, and all your emails will 
be downloaded from GMail and stored in a standard mbox file.
This inclues inbox, archived and sent mails, whatever label you applied.
Spam is not downloaded.

This mbox files can later on be opened with almost any email client (eg. Evolution).

Author:
    Sébastien SAUVAGE - sebsauvage at sebsauvage dot net
    Webmaster for http://sebsauvage.net/

License:

    This program is distributed under the OSI-certified zlib/libpnglicense .
    http://www.opensource.org/licenses/zlib-license.php

    This software is provided 'as-is', without any express or implied warranty.
    In no event will the authors be held liable for any damages arising from
    the use of this software.

    Permission is granted to anyone to use this software for any purpose,
    including commercial applications, and to alter it and redistribute it freely,
    subject to the following restrictions:

        1. The origin of this software must not be misrepresented; you must not
           claim that you wrote the original software. If you use this software
           in a product, an acknowledgment in the product documentation would be
           appreciated but is not required.

        2. Altered source versions must be plainly marked as such, and must not
           be misrepresented as being the original software.

        3. This notice may not be removed or altered from any source distribution.

Requirements:

    - a GMail account with IMAP enabled in settings.
    - GMail settings in english
    - Python 2.5
"""
import imaplib,getpass,os

print "GMail archiver 1.0"
#user = raw_input("Enter your GMail username:")
#pwd = getpass.getpass("Enter your password: ")
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login("user","password@")
m.select("[Gmail]/All Mail")
resp, items = m.search(None, "ALL")
items = items[0].split()
print "Found %d emails." % len(items)
count = len(items)
for emailid in items:
    print "Downloading email %s (%d remaining)" % (emailid,count)
    resp, data = m.fetch(emailid, "(RFC822)")
    email_body = data[0][1]
    # We duplicate the From: line to the beginning of the email because mbox format requires it.
    from_line = "from:unknown@unknown"
    try:
        from_line = [line for line in email_body[:16384].split('\n') if line.lower().startswith('from:')][0].strip()
    except IndexError:
        print "  'from:' unreadable."
    email_body = "From %s\n%s" % (from_line[5:].strip(),email_body)
    print email_body
    '''
    file = open("%s.mbox"%user,"a")
    file.write(email_body)
    file.write("\n")
    file.close()
    '''
    count -= 1
print "All done."
