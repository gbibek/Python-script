import os.path
import os
from subprocess import Popen, PIPE, STDOUT

HOME_PATH    = os.environ['HOME']
TARGET_DIR   = '/.ssh'
TARGET_FILE  = 'id_rsa.pub'
USER_NAME    = 'bghimire'#raw_input("user_name = ")
HOST         = 'swat'#raw_input("host_name = ")
USER_HOST    = USER_NAME + "@" + HOST 
PATH_SSH_DIR     = HOME_PATH + TARGET_DIR
PATH_TARGET_FILE = PATH_SSH_DIR +"/" + TARGET_FILE 
AUTHORIZE_FILE   = PATH_SSH_DIR + "/authorized_keys"

def compare_lines(cmp_str, lines):
    for line in lines.splitlines():
        if cmp_str.split() == line.split(): 
	    return 1
    return 0

if not os.path.exists(PATH_SSH_DIR):
    os.makedirs(PATH_SSH_DIR)
os.chdir(PATH_SSH_DIR)

if not os.path.isfile(PATH_TARGET_FILE):
    print "Generating key.."
    os.popen("ssh-keygen -t rsa")

""" I used stderr=PIPE because I didnot want any error to be shown in the terminal to I piped it and ignored it"""

print "Starting ... "

ret = Popen(["ssh","-o","StrictHostKeyChecking=no", USER_HOST, "mkdir", "~/.ssh"], stderr=PIPE)
ret.communicate()
if ret.returncode:
   print "Directory .ssh already exists."
else:
   print "Creating .ssh directory"
 
local_ret  = Popen(["cat", PATH_TARGET_FILE], stdout=PIPE)
remote_ret = Popen(["ssh", USER_HOST,"cat ~/.ssh/authorized_keys"],stdout=PIPE,stderr=PIPE)

remote_lines = remote_ret.stdout.read()  
remote_ret.communicate()

local_line = local_ret.stdout.read()

if remote_ret.returncode:
    print "There is no authorized_key file in remote server."
else:
    print "There is already authorized_keys file in remote server."


if remote_ret.returncode == 0  and  compare_lines(local_line, remote_lines):
    print "The id_pub.rsa is already on the remote authorized_keys file."   
else:
    print "Appending id_rsa.pub file into authorized_keys file of remote server"
    ret = Popen(["ssh", USER_HOST,"cat >> ~/.ssh/authorized_keys"],stdin=PIPE)
    ret.communicate(input=local_line)
 
local_ret.communicate()
print "Done !!"
