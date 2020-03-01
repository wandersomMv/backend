from sqlalchemy import *
from Model.dados_planilhs import dados
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import ArgumentError, InterfaceError, OperationalError
Base = declarative_base()


class BeneficiaroTable(Base):
    __tablename__ = "beneficiario"
    bnfc_id =Column(BIGINT, primary_key=True, autoincrement=True)
    bnfc_matricula = Column(VARCHAR(255))
    bnfc_nome = Column(VARCHAR(255))

class ConvenioTable(Base):
    __tablename__ = "convenio"
    conv_id = Column(BIGINT, primary_key=True, autoincrement=True)
    conv_ans = Column(VARCHAR(255))
    conv_nome = Column( VARCHAR (255))
    con_data_update = Column( DATE) 

class GuiaTable(Base):
    __tablename__ = "guia"
    guia_id = Column(BIGINT, primary_key=True, autoincrement=True)
    guia_numero   = Column(VARCHAR(255),nullable=False)
    guia_prest_id = Column(BIGINT)
    guia_valor_total = Column(NUMERIC( precision=19,scale=2))
    guia_conv_id  = Column(BIGINT)
    guia_beneficiario_id  = Column(BIGINT)
    guia_data_cadastro = Column( DATE)
    guia_data_pagamento = Column( DATE)
    guia_valor_pago  = Column(NUMERIC( precision=19,scale=2))

class ItemGuiaTable(Base) :
    __tablename__ = "item_guia"
    itmg_id = Column(BIGINT, primary_key=True, autoincrement=True)
    itmg_quantidade = Column(BIGINT)
    itmg_guia_id  = Column(BIGINT)
    itmg_prdt_id =  Column(BIGINT)
    itmg_valor_total  =  Column(NUMERIC( precision=19,scale=2))
    itmg_numero   = Column(INTEGER,nullable=False)
    itmg_valor_pago = Column(INTEGER,nullable=False)
    itmg_motivo_glosa_descricao   = Column(VARCHAR(255))
    itmg_motivo_glosa_codigo    = Column(VARCHAR(255))
    itmg_status = Column(BIGINT)

class PrestadorTable(Base) :
    __tablename__ = "prestador"
    prest_id    = Column(BIGINT, primary_key=True, autoincrement=True)
    prest_cnpj  = Column(NVARCHAR(255))
    prest_nome  = Column(NVARCHAR(255))

class ProdutoTable(Base) :
    __tablename__ = "produtor"
    
    prdt__id = Column(BIGINT, primary_key=True, autoincrement=True)
    prdt__codigo   = Column(NVARCHAR(255))
    prdt__nome   = Column(NVARCHAR(255))
    prdt__valor_unitario  = Column(NUMERIC( precision=19,scale=2))



