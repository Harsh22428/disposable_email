from aiosmtpd.controller import Controller
from smtp_server.handler import DBHandler
from config import settings

if __name__ == '__main__':
    handler = DBHandler()
    controller = Controller(handler, hostname='0.0.0.0', port=settings.SMTP_PORT)
    controller.run()
