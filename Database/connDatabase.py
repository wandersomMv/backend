from sqlalchemy import *
from Model.dados_planilhas import dados
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from Database import databaseLocalHost




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

    def Select_dados_zero_glosa(self, dados_modelado = dados() ):

        matricula = dados_modelado.matricula
        nome = dados_modelado.nome
        numero_da_guia  = dados_modelado.numero_guia if dados_modelado.numero_guia is not None else dados_modelado.ng_prest
        clausula_logica ="  guia.numero = '{}' ".format(numero_da_guia)
        if numero_da_guia is None:
            clausula_logica = "( beneficiario.matricula = '{}' and beneficiario.nome '{}' )".format(matricula,nome)

        query1 = "SELECT  convenio.nome," \
                "   quitacao_guia.data_pagamento ,"\
                "   NULL ,"\
                "   beneficiario.matricula ,"\
                "   beneficiario.nome ,"\
                "    guia.numero ,"\
                "    guia.numero ,"\
                "    guia.id  "\
                " FROM  guia inner join beneficiario  on {} and guia.beneficiario_id = beneficiario_id "\
                " inner join  convenio on  guia.convenio_id = convenio.id "\
                " left join  quitacao_guia on  quitacao_guia.guia_id = guia.id "

        query1= query1.format(clausula_logica)
        result_query1 = self.conn.execute(query1).fetchall()
        result_query1 = result_query1[0]
        guia_id = result_query1[-1]

        query2 = "SELECT   produto.codigo ,"\
                "    produto.nome ,"\
                "    item_guia.valor_total ,"\
                "    quitacao_item.valor ,"\
                "    NULL ,"\
                "    quitacao_item.motivo_glosa_descricao ,"\
                "   quitacao_item.motivo_glosa_codigo " \
                 " FROM  item_guia left join  produto on  item_guia.guia_id = {} and item_guia.produto_id = produto.id " \
                 " left join  quitacao_item on item_guia.id = quitacao_item.item_guia_id "
        query2=query2.format(guia_id)
        input(query2)
        result_query2 = self.conn.execute(query2).fetchall()
        gera_dados = []

        for i in result_query2:
            aux = dados(
                            convenio=result_query1[0],
                            data_pagamento=result_query1[1],
                            numero_protocolo=result_query1[2],
                            matricula=result_query1[3],
                            nome=result_query1[4],
                            numero_guia=result_query1[5],
                            ng_prest=result_query1[6],
                            senha_guia=result_query1[7],
                            codigo_produto=i[0],
                            descricao_produto=i[1],
                            valor_apresentado=i[2],
                            valor_pago=i[3],
                            valor_glosa= i[2] if i[3] is None else i[2]-i[3],
                            descricao_motivo=i[5],
                            codigo_motivo=i[6]
                        )
            gera_dados.append(aux)



        return gera_dados





    # ATUALIZAÇÃO DO ELEMENTO CONVENIUM NO BANCO DE DADOS
    def update_conv_db(self, conv_nome, obj):
        t = databaseLocalHost.ConvenioTable.conv_data_update
        list_item = {i: j for i, j in obj.__dict__.items() if j is not None}
        self.session.query(t).filter(t.conv_nome == conv_nome).update(list_item)
        self.session.commit()

    # BUSCA A CONVENIUM NO BANCO DE DADOS
    def select_aud_db(self, conv_nome):
        query = "SELECT conv_data_update  FROM convenio " \
                "WHERE conv_nome = '{}';".format(conv_nome)
        result = self.conn.execute(query)
        return result.fetchall()


    # INSERIR  GENERICO EM MASA
    def inseter(self,list_obj,gererica_table):
        list_item = []
        qtd = len(list_obj)
        for k in list_obj:
            list_item.append({i: j for i, j in k.__dict__.items() if j is not None})
        id_pk = self.conn.execute(gererica_table.__table__.insert(),list_item).inserted_primary_key[:qtd]
        return id_pk


