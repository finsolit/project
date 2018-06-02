import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def sendmail(name,email,phone,komment,tripid): 
    fromaddr = "fine2113@gmail.com"
    mypass = "13sd0909"
    toaddr = "fine2113@gmail.com"
 
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Новая регистрация на поездку"
 
    body = "Имя: "+name+"\nТелефон: "+phone+"\nПочта: "+email+"\ntripid: "+tripid+"\nS:"+"\nТвой уровень: "+"\nКомментарий: "+komment
    msg.attach(MIMEText(body, 'plain'))
 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, mypass)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()