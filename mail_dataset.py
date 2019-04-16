import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
email_user = "abhishek3485@gmail.com"
email_password = "kumar3485"
email_send = "1605231035@ietlucknow.ac.in"
subject ='dataset'
msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['Subject'] = subject
body = 'Hi there, sending this email from Python!'
msg.attach(MIMEText(body,'plain'))
filename= "/var/www/html/dht.csv"
attachment =open(filename,'rb')
part = MIMEBase('application','octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition',"attachment; filename= "+filename)
print('csv file sent')
msg.attach(part)
text = msg.as_string()
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_user,email_password)
server.sendmail(email_user,email_send,text)
server.quit()
