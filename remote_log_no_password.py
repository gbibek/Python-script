import os.path
import os
from subprocess import Popen, PIPE, STDOUT


HOME_PATH    = os.environ['HOME']
TARGET_DIR   = '/.ssh'
TARGET_FILE  = 'id_rsa.pub'
USER_NAME    = raw_input("user_name = ")
HOST         = raw_input("host_name = ")
USER_HOST    = USER_NAME + "@" + HOST 
PATH_SSH_DIR     = HOME_PATH + TARGET_DIR
PATH_TARGET_FILE = PATH_SSH_DIR +"/" + TARGET_FILE 
AUTHORIZE_FILE   = PATH_SSH_DIR + "/authorized_keys"

if not os.path.exists(PATH_SSH_DIR):
    os.makedirs(PATH_SSH_DIR)

os.chdir(PATH_SSH_DIR)


if not os.path.isfile(PATH_TARGET_FILE):
    print "Generating key.."
    os.popen("ssh-keygen -t rsa")


""" I used stderr=PIPE because I didnot want any error to be shown in the terminal to I piped it and ignored it"""

print "for loging into the server "
ret = Popen(["ssh","-o","StrictHostKeyChecking=no", USER_HOST, "mkdir", "-p", "~/.ssh"], stderr=PIPE)
ret.communicate()


print "for editing file"
ret1 = Popen(["cat", PATH_TARGET_FILE], stdout=PIPE)
ret2 = Popen(["ssh", USER_HOST,"cat > ~/.ssh/authorize_keys"],stdin=ret1.stdout)
ret2.communicate()
