import smtplib
import os


class NotificationManager:
    def __init__(self, final_message):
        """ This class is responsible for sending notifications with the deal flight details"""

        self.my_email = "roxxxxxxxxxxxxxxcom"
        self.receiver_email = "xxxxxxxxxxxxgmail.com"
        self.my_pass = os.environ.get("SMTP_MAIL_PASS")

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(self.my_email, self.my_pass)
            connection.sendmail(
                from_addr=self.my_email,
                to_addrs=self.receiver_email,
                msg=f"subject: cheap flight details.\n\n{final_message}\n\n paste your flight detail here- https://jsonviewer.stack.hu/"
            )
            print("email send successfully")