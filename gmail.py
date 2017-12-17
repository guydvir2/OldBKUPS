import smtplib

# Specifying the from and to addresses
def sendmail(fromaddr,toaddrs,msg):
    fromaddr = 'guydvir.tech@gmail.com'
    toaddrs = 'guydvir2@gmail.com'

    # Writing the message (this message will appear in the email)

    msg = 'Enter you message here'

    # Gmail Login

    username = 'guydvir.tech@gmail.com'
    password = 'kupelu9e'

    # Sending the mail

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username , password)
    server.sendmail(fromaddr , toaddrs, msg)
    server.quit()