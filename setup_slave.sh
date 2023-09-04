apt-get update
apt-get -f install
apt-get upgrade -y
apt-get install python3-pip -y
/usr/bin/python3 -m pip uninstall pyparsing -y
/usr/bin/python3 -m pip uninstall cycler -y
/usr/bin/python3 -m pip uninstall happybase -y
/usr/bin/python3 -m pip uninstall numpy -y
/usr/bin/python3 -m pip uninstall matplotlib -y
/usr/bin/python3 -m pip uninstall pandas -y
/usr/bin/python3 -m pip uninstall typing -y
/usr/bin/python3 -m pip uninstall openpyxl -y
/usr/bin/python3 -m pip --no-cache-dir install cppy
/usr/bin/python3 -m pip --no-cache-dir install numpy==1.13.3
/usr/bin/python3 -m pip --no-cache-dir install happybase
/usr/bin/python3 -m pip --no-cache-dir install pyparsing==2.4.7
/usr/bin/python3 -m pip --no-cache-dir install cycler==0.10.0
/usr/bin/python3 -m pip --no-cache-dir install matplotlib==3.0.1
/usr/bin/python3 -m pip --no-cache-dir install openpyxl==3.0.0
/usr/bin/python3 -m pip --no-cache-dir install pandas==0.18.0
/usr/bin/python3 -m pip --no-cache-dir install typing==3.5.0


./service_slv.sh



