from sqlalchemy import *
from Model.dados_planilhas import dados
from sqlalchemy.orm import Session
from Database.connDatabase import Base

class BeneficiaroTable(Base) :
    __tablename__ = "beneficiario"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    version = Column(BIGINT)
    matricula = Column(VARCHAR(255))
    nome = Column(VARCHAR(255))

class ConvenioTable(Base) :
    __tablename__ = "convenio"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    version = Column(BIGINT)
    ans =  Column(VARCHAR(255))
    nome =  Column(VARCHAR(255))

class GuiaTable(Base) :
    __tablename__ = "guia"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    version = Column(BIGINT)
    numero = Column(VARCHAR(255),nullable=False)
    prestador_id = Column(BIGINT)
    valor_total  = Column(NUMERIC( precision=19,scale=2))
    convenio_id = Column(BIGINT)
    beneficiario_id = Column(BIGINT)
    data = Column(DATE)


class ItemGuiaTable(Base) :
    __tablename__ = "item_guia"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    version = Column(BIGINT)
    quantidade = Column(INTEGER)
    guia_id = Column(BIGINT)
    produto_id = Column(BIGINT)
    valor_total  = Column(NUMERIC( precision=19,scale=2))
    numero = Column(INTEGER,nullable=False)


class PrestadorTable(Base) :
    __tablename__ = "prestador"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    version = Column(BIGINT)
    cnpj = Column(NVARCHAR(255))
    nome = Column(NVARCHAR(255))


class ProdutoTable(Base) :
    __tablename__ = "produtor"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    version = Column(BIGINT)
    codigo = Column(NVARCHAR(255))
    nome = Column(NVARCHAR(255))
    valor_unitario = Column(NUMERIC( precision=19,scale=2))


class QuitacaoGuiaTable(Base) :
    __tablename__ = "quitacao_guia"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    version = Column(BIGINT)
    guia_id = Column(BIGINT)
    data_pagamento = Column(DATE)
    valor_pago = Column(NUMERIC( precision=19,scale=2))

class QuitacaoItemModel(Base) :
    __tablename__ = "quitacao_item"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    version = Column(BIGINT)
    valor = Column(NUMERIC( precision=19,scale=2))
    motivo_glosa_descricao = Column(VARCHAR(255))
    item_guia_id = Column(BIGINT)
    motivo_glosa_codigo = Column(VARCHAR(255))


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
    def Select_dados_(self, dict_dados_modelados = {} ):
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

