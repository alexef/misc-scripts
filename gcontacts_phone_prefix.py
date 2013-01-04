"""
    Add the country prefix to all contacts phone numbers.

    It asks for username and password interactively.
"""
import logging
import gdata.data
import gdata.contacts.data
import gdata.contacts.client
import getpass

logging.basicConfig(level=logging.INFO)

class ContactsApp:
    PREFIX = '+4'
    
    def __init__(self, email, password):
        self.gd_client = gdata.contacts.client.ContactsClient(source='GoogleInc-ContactsPythonSample-1')
        self.gd_client.ClientLogin(email, password, self.gd_client.source)

    def update_phone(self, entry):
        if entry.name and entry.name.full_name:
            print entry.name.full_name.text
        else:
            print '(none)'
        for i, n in enumerate(entry.phone_number):
            print " ", n.text,
            if not n.text.startswith('00') and not n.text.startswith('+'):
                new_text = self.PREFIX + n.text
                new_number = gdata.data.PhoneNumber(rel=n.rel, text=new_text)
                entry.phone_number[i] = new_number
                self.gd_client.Update(entry)
                print "DONE"
            else:
                print "OK"

    def update_phone_feed(self, feed):
        for e in feed.entry:
            if e.phone_number:
                try:
                    self.update_phone(e)
                except gdata.client.RequestError as error:
                    logging.exception(error)
                
    def do(self):
        feed = self.gd_client.GetContacts()
        while feed:
            self.update_phone_feed(feed)
            next = feed.GetNextLink()
            if next:
                feed = self.gd_client.GetContacts(uri=next.href)
            else:
                feed = None

                
if __name__ == '__main__':
    username = raw_input("Please enter your username:")
    pw = getpass.getpass()

    app = ContactsApp(username, pw)
    app.do()
