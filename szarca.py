import os
import cx_Oracle
from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
os.environ['NLS_DATE_FORMAT'] = 'YYYY-MM-DD HH24:MI:SS'
import nti

#read vars from array params
class Lparam():
    def __init__(self, p, n):
        self.p = p
        self.n = n
        
    def Lpa(self):
        y = 0
        for y in range(len(self.p)):
            if self.n in self.p[y]:
                rtn = (self.p[y][self.n])
                return rtn
            
class conn():
    def __init__(self, p):
        self.p = p
        
    def db(self):
        if self.p == "oracle":
            tns = cx_Oracle.makedsn('IP-SERVER', 'PORT-SERVER', service_name='SERVICENAME')
            param = cx_Oracle.connect(user=r'USER-DB', password='PASSWORD-USER-DB', dsn=tns)

        return param
            
class sdx(BaseHTTPRequestHandler):

    def resp(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/xml')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
    def do_GET(self):  
        self.resp()
        vG = ((((self.path).replace("/","")).replace("?","")).split("&"))

        #default message - introduction
        output = str('<szarca middleware="szarca.com">'+
                        '<ownership>'+
                        '<app str="br.sdx.szarca" scode="py"/>'+
                        '<version>1.0</version>'+
                        '<copyright str="SZARCA - 2010/2021"/>'+
                        '</ownership>'+
                        '<functions>'+
                        '<return str="Unauthorized user to execute function library"/>'+
                        '<return str="this application runs from an artificial intelligence developed with the purpose of collecting, '+
                            'processing and making available information from the ERP system. To access requests, contact technical support."/>'+
                        '</functions>'+
                    '</szarca>')

        #check if it has more than 1 parameter
        if len(vG) > 1 :

            #array - params
            p = []

            #make params array
            for x in vG:
                vL = x.split("=")
                p.append(dict({''+vL[0]+'' : ''+vL[1]+''}))

            #read module
            module = Lparam(p, 'md')
            if module.Lpa() == "nti":
                db = nti.dba(p)

            if module.Lpa() == "sales":
                db = sales.dba(p)
            
            output = "<szarca><return>"+str(db.conn())+"</return><param>"+str(p)+"</param></szarca>"

        #output XML response        
        self.wfile.write(output.encode('utf-8'))

def run_sdx(server_class=HTTPServer, handler_class=sdx):
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    
if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run_sdx(port=int(argv[1]))
    else:
     run_sdx()
