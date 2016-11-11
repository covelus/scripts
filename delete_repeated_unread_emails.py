'''
delete_repeated_unread_emails.py: script to get unread repeated e-mails
from a OWA folder and delete them.

Created initially to deal with the VMware Data Recovery e-mail bug:
this deprecated (but still running in some datacenters) system has to 
send a notification when it's configured to do it, i.e: once per week,
after the backup work.
But, from time to time (once per month), it just start sending e-mails
until it stops by itself and the servers enteres in error status.
That's another issue, but this script it done to clean the repeated 
e-mails
'''


'''
ISSUE-01: do some research about:
"imaplib.abort: socket error: [Errno 32] Broken pipe"
mail.expunge() should go just at the end, but due to the server crashes 
sometimes with a error I could not fix, nor find a solution or deal with
the error in a more civilized way. So, I had to put thisinstruction 
here.
When the script crashes, the output trio (num, i, subject) are something
like this:
  ('11500', 92, None)
  ('11501', 93, None)
    Repeated
  ('11502', 94, None)
    Repeated
  ('11503', 95, None)
    Repeated
  ('11504', 96, None)
    Repeated
  ('11505', 97, None)
    Repeated
  [..]
      raise self.abort('socket error: %s' % val)
  imaplib.abort: socket error: [Errno 32] Broken pipe

In this case, it has to be just relaunched.
Unconfortable, but when I have more time I will try to find out the 
solution.
'''

__author__    = "Breogan Costa"

import imaplib, email, re
import getpass
import sys, socket

# Configuration elements, fill with your own data
IMAP_SERVER   = 'imap.XXXXXXX.com'
OWA_DIR       = 'inbox'  # make sure this is your OWA folder
EMAIL_STATUS  = 'UNSEEN' # 'SEEN'

# End of configuration area

username = raw_input('Username: ')
password = getpass.getpass('Password: ')

mail = imaplib.IMAP4_SSL(IMAP_SERVER)
try:
  mail.login(username, password)
except:
  print(sys.exc_info()[1])
  sys.exit(1)

mail.select(OWA_DIR, readonly=False)

(result, mails) = mail.uid('search', None, EMAIL_STATUS)
if result == 'OK':

  print( "Number of unread e-mails:", len(mails[0].split()) )
  raw_input("press a key to continue")
  i = 0;
  prevSubject = ""
  for num in mails[0].split():
    try:
      typ, data = mail.fetch(num, '(RFC822)')
      raw_email = data[0][1]
      email_message = email.message_from_string(raw_email)
      i += 1
      subject = email_message.get('Subject') 
      print(num, i, subject )
      if prevSubject == subject:
        print("\tRepeated")
        mail.store(num, '+FLAGS', '\\Deleted')
      prevSubject = subject
      mail.expunge()  # TODO: fix this in other way. Check ISSUE-01
    except socket.error, ex:
      print("Error: ", ex)
      pass
      # it crashed sometimes due to sever issues & misses mail.expunge()

  mail.expunge()
 
mail.close()
mail.logout()


