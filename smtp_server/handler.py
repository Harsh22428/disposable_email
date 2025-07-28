# aiosmtpd handler for recieving emails and saving them to db
from aiosmtpd.controller import Controller
from email.parser import BytesParser
from email import policy

from api.db import connect_to_db, close_db_connection, save_email

class DBHandler:
    async def handle_DATA(self, server, session, envelope):
        # Parse the incoming email
        msg = BytesParser(policy=policy.default).parsebytes(envelope.content)
        
        # Extract fields (you can expand this as needed)
        to_addr = envelope.rcpt_tos[0]
        from_addr = envelope.mail_from
        subject = msg['subject']
        date = msg['date']
        body = msg.get_body(preferencelist=('plain', 'html')).get_content() if msg.is_multipart() else msg.get_payload()
        
        # Connect to DB and save
        db = connect_to_db()
        save_email(db, to_addr, from_addr, subject, date, body)
        close_db_connection(db)
        
        return '250 Message accepted for delivery'

if __name__ == '__main__':
    handler = DBHandler()
    controller = Controller(handler, hostname='0.0.0.0', port=25)
    controller.start()