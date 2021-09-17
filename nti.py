import szarca

class dba():
    def __init__(self, p):
        self.p = p
        self.a = ""
            
    def conn(self):

        lnX = ""
        lnX_users = ""
        
        inFN = szarca.Lparam(self.p, 'fn')

        #---------- Processos e Rotinas do ORACLE --------------------------
        if inFN.Lpa() == "oracle.process":

            connection = szarca.conn("oracle")
            database = connection.db()

            loggedUsers = database.cursor()

            #Usuarios em Uso no Oracle
            loggedUsers.execute(
                        'select '+
                            'USERNAME, '+
                            'OSUSER, '+
                            'MACHINE, '+
                            'PROGRAM, '+
                            'LOGON_TIME, '+
                            'USR_RAMAL '+
                        
                        'from v$session v '+
                            'LEFT JOIN usuario u ON u.usr_nome = v.USERNAME '+
                            'WHERE v.SCHEMANAME != \'SYS\''
                        )
            lnUsers = loggedUsers.fetchall()
            lnRec1 = 0                        
            for y in lnUsers:
                lnX_users += str('<process>'+
                        '<db_user>'+str(y[0])+'</db_user>'+
                       '<os_user>'+str(y[1])+'</os_user>'+
                        '<machine>'+str(y[2])+'</machine>'+
                        '<app>'+str(y[3])+'</app>'+
                        '<logonTime>'+str(y[4])+'</logonTime>'+
                        '<phone>'+str(y[5])+'</phone>'+
                    '</process>')

                lnRec1 +=1

            #Processos Travados
            qu = database.cursor()
            qu.execute(

                    'select '+
                        'c.owner as OWNER, '+ 
                        'c.object_name as TABELA, '+ 
                        'c.object_type as TIPO, '+
                        'b.sid as SID, '+
                        'b.serial# as SERIAL, '+ 
                        'b.status as STS, '+
                        'b.osuser as USUARIO, '+ 
                        'b.machine as MAQUINA '+
                                            
                            'from v$locked_object a , v$session b, dba_objects c '+

                             'where b.sid = a.session_id '+
                             'and a.object_id = c.object_id '

                           )
            ln = qu.fetchall()
            lnRec2 = 0
            
            for x in ln:
                
                lnX += str('<process> '+
                       '<owner>'+str(x[0])+'</owner>'+
                        '<table>'+str(x[1])+'</table>'+
                        '<type>'+str(x[2])+'</type>'+
                        '<sid>'+str(x[3])+'</sid>'+
                        '<serial>'+str(x[4])+'</serial>'+
                        '<status>'+str(x[5])+'</status>'+
                        '<user>'+str(x[6])+'</user>'+
                        '<machine>'+str(x[7])+'</machine>'+
            
                    '</process>')
                
                lnRec2 +=1

            outXML = str('<lockedProcesses count="'+str(lnRec2)+'">'+lnX+'</lockedProcesses>'+
                         '<activeUsersProcesses count="'+str(lnRec1)+'">'+lnX_users+'</activeUsersProcesses>')

            self.a = outXML
            database.close()

        return self.a
    
