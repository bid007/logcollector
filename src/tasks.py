#Author : Bidhya Nandan Sharma
#Date 12/18/2017

from celery import Celery 
from ssh import SSH
from rulematcher import RuleMatcher
app = Celery('tasks')
app.config_from_object('configs.celeryconfig')
from dbconn import conn

#The function extracts username, password, ip and port from client dict
#Uses those info to connect to clients
#move our client script there
#create temp directory and move the script inside it and execute it
#finally remove the directory
@app.task
def execute_client(client_info, econfig_dict):
    user = client_info['username']
    pas = client_info['password']
    ip = client_info['ip']
    port = client_info['port']
    email = client_info['mail']
    alerts = client_info['alerts']
    print(alerts)
    try:
        ssh_cli = SSH(ip, user, pas, port)
        ssh_cli.send_file("clientscript.py", "clientscript.py")
        ssh_cli.send_command('rm -rf .tmpPyScr*')
        ssh_cli.send_command("mktemp -d .tmpPyScr.XXXX")
        ssh_cli.send_command("mv clientscript.py .tmpPyScr*/")
        ssh_cli.send_command("chmod +x .tmpPyScr.*/clientscript.py")
        ssh_cli.send_command("python -V")
        ssh_cli.send_command("python .tmpPyScr*/clientscript.py -ip " + ip)
        ssh_cli.send_command('rm -rf .tmpPyScr*')
        log_processing.delay(str(ssh_cli.log_msg), ip, email, alerts, econfig_dict)
        ssh_cli.client.close()
    except Exception as e:
        print(e)
        print("Cannot connect to the clients")


#After retrieving the encrypted log, this function will handle
#decryption, matching against alert rule, sending email and saving to db
#Sending email may take time and thus seperate email seperate taks is created for that
@app.task
def log_processing(log, ip, email, alert_rules, econfig_dict):
    from Crypto.Cipher import ARC4
    import base64
    dec_obj = ARC4.new(ip)
    cipher = log.split('=>')[1]
    print("Encrypted & encoded log : " + cipher)
    actual_log = str(dec_obj.decrypt(base64.b64decode(cipher)))
    print("Log : "+ actual_log)
    #match against rule and store in db
    match_obj = RuleMatcher(actual_log, alert_rules)
    if match_obj.matched:
        send_email.delay(match_obj.msg, email, econfig_dict)
    # try:
    cur = conn.cursor()
    cur.execute("INSERT INTO logtable (IP, LOG) VALUES (%s, %s)", (ip, actual_log))
    cur.close()
    conn.commit()
    # except Exception as e:
        # print(e)

@app.task
def send_email(msg, email, econfig_dict):
    import smtplib
    #smtp mail server detail
    HOST = econfig_dict['HOST']
    PORT = econfig_dict['PORT']
    USER = econfig_dict['USER']
    PWD = econfig_dict['PWD']
    FROM = econfig_dict['FROM']
    SUBJECT = econfig_dict['SUBJECT']
    #using gmail and gmail email address
    TEXT = msg
    TO = email
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        server.login(USER, PWD)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except Exception as e:
        print(e)
        print("failed to send mail")