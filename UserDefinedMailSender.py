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
from getpass import getpass


def is_connected():
    try:
        url = 'http://www.google.com'
        response = urllib.request.urlopen(url, timeout=5)
        return True
    except urllib.error.URLError:
        return False

def MailSender(filename, log_time, fromaddr, toaddr):
    try:
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = f"Jay Infosystems Process log generated at: {log_time}"

        body = f"""
        Hello {toaddr},
        Welcome to my first Automated email,
        Please find the attached document which contains the log of running processes.
        Log file created at: {log_time}

        This is an auto-generated mail.

        Thanks & Regards,
        Jaywant Sandeep Adhau,
        Jay Infosystems
        """
        msg.attach(MIMEText(body, 'plain'))

        with open(filename, 'rb') as attachment:
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(attachment.read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', f"attachment; filename={os.path.basename(filename)}")
            msg.attach(p)

        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.set_debuglevel(1)
            server.starttls()
            server.login(fromaddr, "password") #stored in module or directly enter password   
            server.sendmail(fromaddr, toaddr, msg.as_string())

        print("Log file successfully sent through Mail")

    except smtplib.SMTPAuthenticationError:
        print("Failed to authenticate. Check your email and password.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def ProcessLog(log_dir="EmailLog"):
    listprocess = []

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    separator = "_" * 80
    log_time = time.ctime().replace(' ', '_').replace(':', '-')
    log_path = os.path.join(log_dir, f"MarvellousLog_{log_time}.log")

    with open(log_path, 'w') as f:
        f.write(separator + "\n")
        f.write(f"Jay Infosystems process Logger: {time.ctime()}\n")
        f.write(separator + "\n")
        f.write("\n")

        for proc in psutil.process_iter(attrs=['pid', 'name', 'username']):
            try:
                vms = proc.memory_info().vms / (1024 * 1024)
                pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
                pinfo['vms'] = vms
                listprocess.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        for element in listprocess:
            f.write(f"{element}\n")

    print(f"Log file is successfully generated at location {log_path}")

    if is_connected():
        fromaddr = input("From: ").strip()
        password = getpass("Password: ").strip()
        toaddr = input("To: ").strip()

        starttime = time.time()
        MailSender(log_path, time.ctime(), fromaddr, password, toaddr)
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
