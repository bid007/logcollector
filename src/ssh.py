#Author : Bidhya Nandan Sharma
#Date 12/18/2017
from paramiko import client 
class SSH:
    """
    Takes username, ip, password and port as input to connect to server
    Takes command to execute using send_command function
    Takes file to transfer using send_file function 
    """
    def __init__(self, ip, uname, pas, port):
        print('Connecting to server')
        self.client = client.SSHClient()
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())
        self.client.connect(ip, username=uname, password=pas, port=port, look_for_keys=False)

    def send_command(self, command):
        if self.client:
            stdin, stdout, stderr = self.client.exec_command(command)
            while not stdout.channel.exit_status_ready():
                if stdout.channel.recv_ready():
                    alldata = stdout.channel.recv(1024)
                    prevdata = b"1"
                    while prevdata:
                        prevdata = stdout.channel.recv(1024)
                        alldata += prevdata
                    if 'Log' in str(alldata):
                        self.log_msg = alldata
        else:
            print("No open connection found")
    
    def send_file(self, local_file, remotefilepath):
        ftp_client = self.client.open_sftp()
        ftp_client.put(local_file, remotefilepath)
        ftp_client.close()

    def copy_log_file(self, remotefile, localfile):
        ftp_client = self.client.open_sftp()
        ftp_client.get(remotefile, localfile)
        ftp_client.close()
