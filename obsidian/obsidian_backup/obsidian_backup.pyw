from datetime import datetime
import shutil
import os
from time import sleep
from win10toast import ToastNotifier

f = open(r"config.txt", "r") # Vault location, backup location, interval, last backup
lines = f.read().split('\n')

def backup(lines):
    ctime = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    os.makedirs(lines[1] + "\\" + ctime);
    dest = lines[0].split('\\')
    shutil.copytree(lines[0], lines[1] + "\\" + ctime + "\\" + dest[len(dest) - 1]);
    if (len(lines) > 3):
        lines[3] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    else:
        lines.append(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    f.close()
    os.remove("config.txt")
    with open('config.txt', 'w') as filehandle:
        for i in range(0, len(lines)):
            filehandle.write('%s' % lines[i])
            if (i < len(lines) - 1):
                filehandle.write('\n')

# Read config
while (True):
    if (len(lines) > 3):
        dt = datetime.strptime(lines[3], '%d-%m-%Y %H:%M:%S')
        delta = datetime.now() - dt 
        if (delta.total_seconds() >= int(lines[2])):
            backup(lines)
    else:
        backup(lines)
    if os.path.isfile('cmd.txt'):
        g = open(r"cmd.txt", "r")
        cmd = g.read().split('\n')
        for i in cmd:
            if (i == 'bkup'):
                backup(lines)
        toaster = ToastNotifier()
        toaster.show_toast("Obsidian Backup", "Commands are executed successfully.", duration=3)
        g.close()
        os.remove("cmd.txt")
    sleep(3)
