---

# Automated-MailSender

This project, named "Automated MailSender," is designed to log records of running processes on your system at specified intervals and send these logs via email automatically. It uses Python to accomplish this task and relies on several external libraries for process management, scheduling, and email sending.

## Table of Contents
1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [License](#license)

## Features
- Logs information about currently running processes.
- Automatically sends log files to a specified email address.
- Can be scheduled to run at user-defined intervals.
- Checks for internet connectivity before attempting to send emails.

## Requirements
- Python 3.6 or higher
- The following Python libraries:
  - os
  - time
  - urllib
  - psutil
  - smtplib
  - schedule
  - email
- An SMTP server (e.g., Gmail SMTP server for sending emails).

## Installation
To get started with the "Automated Mail-Sender," follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/Automated-MailSender.git
    cd Automated-MailSender
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required Python libraries:
    ```sh
    pip install -r requirements.txt
    ```

    If you don't have a `requirements.txt` file, create one with the following content:
    ```
    psutil
    schedule
    ```

4. Add your email password to `PasswordUtil.py`:
    ```python
    # PasswordUtil.py
    password = 'your-email-password'
    ```

## Usage
To use the "Automated Mail-Sender," you need to run the `EmailSender.py` script with a specified interval (in seconds) for logging and sending emails. 

1. Run the script:
    ```sh
    python EmailSender.py <interval>
    ```

    Replace `<interval>` with the number of seconds between each log and email. For example:
    ```sh
    python EmailSender.py 10
    ```

## Configuration
Before running the script, make sure to configure the following:

1. **Email Credentials:** Update the `MailSender` function in `EmailSender.py` with your email address and the recipient's email address.
    ```python
    fromaddr = "your-email@gmail.com"
    toaddr = "recipient-email@gmail.com"
    ```

2. **SMTP Settings:** The script uses Gmail's SMTP server. If you are using a different email provider, update the SMTP server settings accordingly:
    ```python
    s = smtplib.SMTP('smtp.gmail.com', 587)
    ```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
