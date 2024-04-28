VERIFICATION_EMAIL = """Thank you for registering an account on Study Chat. 
In order to complete setting up your account, you need to enter this verification code: {number}"""

import logging
import random
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union

from email_validator import EmailNotValidError, validate_email


class EmailManager:
    def __init__(self, smtp_port: int, smtp_server: str, sender_email: str, 
                 password: str, code_pool_size: int, valid_domain: str) -> None:
        
        # Initiate attributes
        self.smtp_port = smtp_port
        self.smtp_server = smtp_server
        self.sender_email = sender_email
        self.__password = password
        self.code_pool_size = code_pool_size
        self.valid_domain = valid_domain
        self.domain_length = len(valid_domain)

        self.pending_verifications = {}
        self.email_context = ssl.create_default_context()
        self.__connect()
    

    def validate_email(self, email: str) -> bool:
        try:
            domain = email[-self.domain_length:]
            if domain != self.valid_domain: return False
            validate_email(email)
            return True
        
        except EmailNotValidError:
            return False
        

    def init_verification_code(self, address: tuple[str]) -> Union[None, int]:
        if not address in self.pending_verifications.keys(): 
            code = random.randint(0, self.code_pool_size) # 3 digits code
            while code in self.pending_verifications.values():
                code = random.randint(0, self.code_pool_size) 
            self.pending_verifications[address] = code
            return code
        

    def check_verification_code(self, address: tuple[str], code: str) -> bool:
        if address in self.pending_verifications.keys():
            if int(code) == self.pending_verifications[address]:
                self.pending_verifications.pop(address)
                return True
        return False


    def send_verification_email(self, recipient: str, code: str) -> None:
        try:
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = recipient
            message['Subject'] = 'Study Chat Verification Code'
            body = VERIFICATION_EMAIL.format(number=str(code))
            message.attach(MIMEText(body, 'plain'))

            self.TIE_server.sendmail(
                self.sender_email,
                recipient,
                message.as_string()
            )

        except smtplib.SMTPResponseException as err:
            self.__debug(err)


    def __connect(self) -> None:
        try:
            self.TIE_server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.TIE_server.starttls(context=self.email_context)
            self.TIE_server.login(self.sender_email, self.__password)
            self.__debug('connected')

        except smtplib.SMTPResponseException as err:
            self.__debug(err)
            self.TIE_server.quit()


    def __debug(self, message) -> None:
        logging.debug(f'[email service]: {message}')
