from sqlalchemy import *
from Model.dados_planilhs import dados
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import ArgumentError, InterfaceError, OperationalError

class SQL :
    # CONSTRUTOR DA CLASSE SQL
    def __init__(self,user= None,password = None ,host = None ,port = None , database =None ) :
        self.user = user
        self.password = password 
        self.host = host
        self.port = port
        self.database = database
        self.cont = 0

        str_bd = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(self.user,self.password,self.host,self.port,self.database)

        s = 'Reconectando'.upper()
        c = 'Conectando'.upper()
        while self.cont < 100 :
            try :
                print(c, sep=' ', end='.', flush=True)
                c = ''
                self.conn = create_engine(str_bd).connect()
                self.metadata = MetaData(bind=self.conn)
                self.session = Session(bind=self.conn)
                break
            except :
                raise
                self.cont += 1
                print(s, sep=' ', end='.', flush=True)
                s = ''
                sleep(0.6)


    # DESTRUTOR DA CLASSE SQL
    def __del__(self) :
        try :
            self.conn.close()
        except :
            raise
            print("\nNenhuma conexão aberta!".upper())


    #
    def Select_dados_zero_glosa(self, dict_dados_modelados = {} ):
        dados_modelados_bd= []

        for key,dado_modelado in  dict_dados_modelados.items:
            i_dado=dados()
            query = "SELECT  convenio.nome ," \
                    "   data_pagamento = '',"\
                    "   numero_protocolo = '',"\
                    "   beneficiario.matricula = '',"\
                    "   beneficiario.nome = '',"\
                    "    guia.numero = '',"\
                    "    ng_prest = '',"\
                    "    senha_guia = '',"\
                    "    codigo_produto = '',"\
                    "    descricao_produto = '',"\
                    "    valor_apresentado = '',"\
                    "    valor_pago = '',"\
                    "    valor_glosa = '',"\
                    "    descricao_motivo = '',"\
                    "   codigo_motivo "\



