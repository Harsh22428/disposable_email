# Responsible for starting SMTP server
from aiosmtpd.controller import Controller
from handler import DBHandler

if __name__ == '__main__':
    handler = DBHandler()
    controller = Controller(handler, hostname='0.0.0.0', port=25)
    controller.start()