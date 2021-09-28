apt update
apt install -y software-properties-common
add-apt-repository ppa:deadsnakes/ppa
apt-get install -y python3.9
apt install -y python3.9-distutils
wget https://bootstrap.pypa.io/ez_setup.py -O - | python3.9
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.9 get-pip.py
pip3.9 install --upgrade setuptools
python3.9 -m pip install Pillow
python3.9 -m pip install behave
apt-get install -y python3-tk

useradd apps
mkdir -p /home/apps && chown apps:apps /home/apps

apt-get install -y xvfb x11-apps
apt-get install -y wget

apt-get install -y imagemagick

# debugging tools
apt-get install -y x11vnc fluxbox wmctrl
