# DJINN

Djinn is a quick and dirty attempt to integrate a customized web handler front end and [GraphSpy](https://github.com/RedByte1337/GraphSpy) 
This is intended for use in dynamic device code phishing and can be customized to spoof and present pages for any web server front end server.

# Installation & Usage

Installation is easy and recommended from a venv:

```
$ git clone https://github.com/H4rk3nz0/Djinn.git
$ cd Djinn
$ python3 -m venv djinn
$ source djinn/bin/activate
(djinn) $ pip install -r requirements.txt
```

Customize the the server config file **dyn.conf**, replace certs in **Djinn/resources/** and finally start:

```
# Default
$ python3 djinn.py

# Verbose output and custom engagement/db name
$ python3 djinn.py -d -n acme
```


If you encounter permission errors when port binding occurs then ensure the capabilities are set on your default python3 version.

```
python3 --version

sudo setcap 'cap_net_bind_service=+ep' /usr/bin/python3.12
```
