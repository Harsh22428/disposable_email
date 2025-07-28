# handles incoming emails --> Parse them -->Build email models and saves them to MongoDB
from email.parser import BytesParser
from email import policy

from ..api.models import EmailModel
from ..api.db import connect_to_mongo, save_email
import logging
logger = logging.getLogger("smtp_handler")
logging.basicConfig(level=logging.INFO)

db = connect_to_mongo()

class DBHandler:
    async def handle_DATA(self, server, session, envelope):
        try:
            # Parse the incoming email message
            msg = BytesParser(policy=policy.default).parsebytes(envelope.content)

            # Extract addresses
            to_addr = envelope.rcpt_tos[0]
            from_addr = envelope.mail_from
            inbox = to_addr.split("@")[0]

            # Extract subject and date
            subject = msg['subject']
            date = msg['date']

            # Parse the body 
            if msg.is_multipart():
                body = None
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_content()
                        break
                if body is None:
                    # fallback: first text/html part, or whole
                    for part in msg.walk():
                        if part.get_content_type() == "text/html":
                            body = part.get_content()
                            break
                if body is None:
                    body = "(No text content found)"
            else:
                body = msg.get_content()

            #  Extract attachments
            attachments = []
            if msg.is_multipart():
                for part in msg.iter_attachments():
                    attachment = {
                        "filename": part.get_filename(),
                        "content_type": part.get_content_type(),
                        "size": len(part.get_content()) if part.get_content() else 0,
                        # You can save the data or skip it for now to avoid bloat
                        # "data": base64.b64encode(part.get_content()).decode('utf-8')
                    }
                    attachments.append(attachment)

            #  Extract all headers
            headers = {k: v for k, v in msg.items()}

            # Build EmailModel
            email_obj = EmailModel(
                inbox=inbox,
                from_address=from_addr,
                to_address=to_addr,
                subject=subject,
                body=body,
                date=date,  # Let Pydantic parse this string to datetime
                attachments=attachments,
                headers=headers
            )

            # Save to DB
            save_email(db, email_obj.model_dump(by_alias=True, exclude_none=True))

            return '250 Message accepted for delivery'
        except Exception as e:
                logger.error(f"Error processing email: {e}", exc_info=True)
                return '451 Requested action aborted: local error in processing'


