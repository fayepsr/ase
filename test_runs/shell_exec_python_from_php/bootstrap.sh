#This is the bash script to be ran after the container is created

chmod 755 /home/python_example/test.py
apt update
apt install -y python2.7