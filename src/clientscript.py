#!/usr/bin/python3
import os 
import platform
import sys
#Author : Bidhya Nandan Sharma
#Date 12/18/2017
#System log generator for Linux
class Linux:
    """
    Prints out system log
    """
    def __init__(self):
        self.ram_info = self.get_ram_info()
        self.ram_usage = (float(self.ram_info[1])/float(self.ram_info[0]))
        self.cpu_usage = self.get_cpu_use()
        self.log = '# memory: {:.2f}%, cpu: {:.2f}% '.format(self.ram_usage, self.cpu_usage)

    # Return RAM information (unit=kb) in a list                                        
    # Index 0: total RAM                                                                
    # Index 1: used RAM                                                                 
    # Index 2: free RAM                                                                 
    def get_ram_info(self):
        p = os.popen('free')
        i = 0
        while 1:
            i = i + 1
            line = p.readline()
            if i==2:
                return(line.split()[1:4])

    # Return % of CPU used by user as a character string                                
    def get_cpu_use(self):
        last_idle = last_total = 0
        with open('/proc/stat') as f:
            fields = [float(column) for column in f.readline().strip().split()[1:]]
        idle, total = fields[3], sum(fields)
        idle_delta, total_delta = idle - last_idle, total - last_total
        last_idle, last_total = idle, total
        utilisation = 100.0 * (1.0 - idle_delta / total_delta)
        return utilisation

    def __str__(self):
        return self.log

def main():
    system = platform.system()
    my_ip = sys.argv[2]
    #Add other mappings here 
    sys_map = {'Linux':Linux}
    try:
        from Crypto.Cipher import ARC4
        import base64
        en_obj = ARC4.new(my_ip)
        cipher_text = base64.b64encode(en_obj.encrypt(str(sys_map[system]())))
        print("Log=>" + str(cipher_text))
    except Exception as e:
        # raise Exception("No logger defined for "+system+ " OS")
        print(e)
        print("ErrorLog=>No logger defined for "+system+ " OS")
    
if __name__ == '__main__':
    main()