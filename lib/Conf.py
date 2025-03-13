import configparser

class conf:
    def __init__(self,configfile):
        self.parser = configparser.ConfigParser()
        self.parser.read(configfile)

        # Parse Out IMC Server Options
        self.httpport =       self.parser['DJINN']['HTTPS_PORT']
        self.httpip =         self.parser['DJINN']['HTTPS_IP']
        self.httpdomain =         self.parser['DJINN']['HTTPS_DOMAIN']
        self.httpendpoint =   self.parser['DJINN']['HTTPS_ENDPOINT']
        self.httppage =       self.parser['DJINN']['HTTPS_PAGE']
        self.httptokenparam = self.parser['DJINN']['HTTPS_TOKENPARAM']
        self.httptokenval = self.parser['DJINN']['HTTPS_TOKENVALUE']

        self.httpserverversion = self.parser['DJINN']['HTTPS_SERVERVERSION']
        self.httpsystemversion = self.parser['DJINN']['HTTPS_SYSTEMVERSION']


	    # File name located in ./resources/
        self.httpcert =         self.parser['DJINN']['HTTPCERT']
        self.httpkey =          self.parser['DJINN']['HTTPKEY']