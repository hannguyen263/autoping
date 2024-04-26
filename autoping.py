import subprocess
import re
import platform
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body):
    sender_email = "#"
    receiver_email = "#"
    password = "#"  # Be cautious with password security

    # Create the email object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Connect to the server and send the email
    try:
        server = smtplib.SMTP('#', 25)  # Replace with your SMTP server details
       # server.starttls()
       # server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def ping(ip_address):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '20', ip_address]

    try:
        output = subprocess.run(command, stdout=subprocess.PIPE, text=True)
        output_text = output.stdout
        print(f"Output:\n{output_text}")

        average_time = None
        if platform.system().lower() == 'windows':
            match = re.search(r'Average = (\d+)ms', output_text)
            if match:
                average_time = float(match.group(1))
        else:
            times = re.findall(r'time=(\d+\.?\d*) ms', output_text)
            if times:
                average_time = sum(map(float, times)) / len(times)

        if average_time is not None:
            print(f"Average Ping time: {average_time:.2f} ms")
            if average_time > 400:
                subject = "High Ping Alert"
                body = f"The average ping time to {ip_address} exceeded 400 ms, measured at {average_time:.2f} ms."
                send_email(subject, body)
        else:
            print("Average ping time not found.")

    except subprocess.CalledProcessError as e:
        print(f"Failed to ping {ip_address}. Error: {e}")


if __name__ == '__main__':
    ip = "185.28.7.252"
    ping(ip)
