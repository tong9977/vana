sudo mkdir /vanaramdisk
sudo mount -t tmpfs -o rw,size=2G tmpfs /vanaramdisk

sudo mkdir /tmpramdisk
sudo mount -t tmpfs -o rw,size=1G tmpfs /tmpramdisk

sudo umount /vanaramdisk
sudo umount /tmpramdisk


sudo sysctl -w net.core.rmem_default=31457280
sudo sysctl -w net.core.rmem_max=33554432

sudo ip link set dev enp8s0 mtu 9000
sudo ip link set dev enp9s0 mtu 9000  


pip3 install opencv-python
pip3 install opencv-contrib-python

pip3 install pycurl
pip3 install glob
pip3 install twisted[tls]

vscode 
"python.linting.pylintArgs": ["--extension-pkg-whitelist=cv2"],
"python.linting.pylintEnabled": false

sudo apt-get update
sudo apt-get install build-essential libssl-dev
curl -sL https://raw.githubusercontent.com/creationix/nvm/v0.31.0/install.sh -o install_nvm.sh
bash install_nvm.sh
source ~/.profile
nvm ls-remote 
nvm install v10.16.2
nvm use v10.16.2

npm install -g @feathersjs/cli
feathers generate app
sudo apt-get install gdebi
wget http://github.com/angryziber/ipscan/releases/download/3.3.3/ipscan_3.3.3_amd64.deb


ssh root@192.168.111.111
fa

//raspberry pi
sudo raspi-config
sudo apt-get install python-smbus i2c-tools
sudo i2cdetect -y 1


//NAS 192.168.111.3
Administrator
Monstermedia@vana