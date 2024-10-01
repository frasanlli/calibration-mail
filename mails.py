import autopywin32
import win32com
from log import Log

class Mail(Log):
    def __init__(self, user: str) -> None:
        super()
        self.outlook = win32com.client.Dispatch("Outlook.Application")

    def ask_y_n(self)->bool:
        user_input: str = ""
        while user_input!= "yes" or user_input!= "no":
            user_input = (input('Do you want to resend the mail? (yes/no): ')).lower()
            if user_input == 'yes':
                print('user typed yes')
                return True
            elif user_input == 'no':
                print('user typed no')
                return False

    def check_sent_mail(self, destiny: str, copy: str, subject: str, msg: str) -> bool:
        msg_or_subject: bool = False
        #Read mails sent today, if they already exist
        if mail_msg == msg:
            msg_or_subject = True
        if msg_or_subject:
            answer: bool = self.ask_y_n()
            if answer:
                self.send_mail(destiny, copy, subject, msg)
        else:
            self.send_mail(destiny, copy, subject, msg)

    def send_mail(self, destiny: str, copy: str, subject: str, msg: str) -> None:
        message = self.outlook.CreateItem(0)
        message.Subject = f"CALIBRATION DATE near to end: {tool} {expiration_date}"
        message.Body = "CALIBRATION about to expire"
        message.Body = "URGENT - CALIBRATION EXPIRED"