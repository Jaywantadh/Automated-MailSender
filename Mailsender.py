import os
import time
import urllib.error
import psutil
import urllib.request
import smtplib
import schedule
from sys import argv
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


def is_connected():
    try:
        # Check connection by opening a URL to a reliable site
        url = 'http://www.google.com'
        response = urllib.request.urlopen(url, timeout=5)
        return True
    except urllib.error.URLError as err:
        return False

def MailSender(filename, time):
    try:
        fromaddr = "---------" #Sender's Address
        toaddr = "-----------" #Reciever's Address
        
        msg = MIMEMultipart()
        
        msg['To'] = toaddr

        body = f"""
        Hello {toaddr},
        Welcome to my first Automated email,
        Please find the attached document which contains the log of running processes.
        Log file created at: {time}

        This is an auto-generated mail.

        Thanks & Regards,
        Jaywant Sandeep Adhau,
        Jay Infosystems
        """
        msg['Subject'] = f"Jay Infosystems Process log generated at: {time}"

        msg.attach(MIMEText(body, 'plain'))
        attachment = open(filename, 'rb')
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attachment.read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f"attachment; filename={os.path.basename(filename)}")

        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()

        # Use the app-specific password here
        s.login(fromaddr, 'password') #make module for password or enter the password(if you are using G-mail use app password)

        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()

        print("Log file successfully sent through Mail")

    except Exception as e:
        print("Error: Unable to send mail", e)


def ProcessLog(log_dir="EmailLog"):
    listprocess = []

    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass

    separator = "_" * 80
    log_path = os.path.join(log_dir, f"MarvellousLog{time.ctime().replace(' ', '_').replace(':', '-')}.log")
    with open(log_path, 'w') as f:
        f.write(separator + "\n")
        f.write(f"Jay Infosystems process Logger: {time.ctime()}\n")
        f.write(separator + "\n")
        f.write("\n")

        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
                vms = proc.memory_info().vms / (1024 * 1024)
                pinfo['vms'] = vms
                listprocess.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        for element in listprocess:
            f.write(f"{element}\n")

    print(f"Log file is successfully generated at location {log_path}")

    connected = is_connected()

    if connected:
        starttime = time.time()
        MailSender(log_path, time.ctime())
        endtime = time.time()
        print(f'Took {endtime - starttime} seconds to send mail')
    else:
        print("There is no internet connection")

def main():
    print("----Jay Inforsystems by Jaywant Adhau------")

    print(f"Application name: {argv[0]}")

    if len(argv) != 2:
        print("Error: Invalid number of arguments")
        print("Usage: python script.py <interval_in_minutes>")
        exit()

    if argv[1].lower() == '-h':
        print("This script is used to log records of running processes.")
        print("Usage: python script.py <interval_in_minutes>")
        exit()

    try:
        interval = int(argv[1])
        schedule.every(interval).seconds.do(ProcessLog)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except ValueError:
        print("Error: Invalid datatype of input. Please provide an integer for the interval.")
    except Exception as e:
        print("Error: Invalid inputs", e)

if __name__ == "__main__":
    main()
