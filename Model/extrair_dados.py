import os
import untangle
import xmltodict
import datetime
from time import sleep
from xml.etree import ElementTree as et

class Extracao_dados:
    def __init__(self,
        convenio = '', 
        data_pagamento = '', 
        numero_protocolo = '', 
        matricula = '', 
        nome = '', 
        numero_guia = '', 
        ng_prest = '', 
        senha_guia = '', 
        codigo_produto = '', 
        descricao_produto = '', 
        valor_apresentado = '', 
        valor_pago = '', 
        valor_glosa = '', 
        descricao_motivo = '', 
        codigo_motivo = ''
    ):
        self.convenio = convenio
        self.data_pagamento = data_pagamento
        self.numero_protocolo = numero_protocolo
        self.matricula = matricula
        self.nome = nome
        self.numero_guia = numero_guia
        self.ng_prest = ng_prest
        self.senha_guia = senha_guia
        self.codigo_produto = codigo_produto
        self.descricao_produto = descricao_produto
        self.valor_apresentado = valor_apresentado
        self.valor_pago = valor_pago
        self.valor_glosa = valor_glosa
        self.descricao_motivo = descricao_motivo
        self.codigo_motivo = codigo_motivo
        self.nome_arquivos = []
        self.caminho_ate_pasta_downloads = ''
        self.lista_objetos = []


    
    # COLETA O NOME DOS ARQUIVOS XML
    def coleta_nome_arquivos(self):
        caminhos_arquivos = os.getcwd()
        caminhos_arquivos = caminhos_arquivos.replace('Controller','')
        self.caminho_ate_pasta_downloads += caminhos_arquivos + "/Downloads"
        print("Caminho para a psta downloads: ",self.caminho_ate_pasta_downloads)
        self.nome_arquivos = os.listdir(self.caminho_ate_pasta_downloads)

    # RETORNA UMA TUPLA COM OS DADOS DO XML
    def retorna_tupla_dados(self,name):
        doc = ''
        # CRIA UM OBJETO DO TIPO DICIONARIO COM OS DADOS
        with open(self.caminho_ate_pasta_downloads + "/" + name) as fd:
            doc = xmltodict.parse(fd.read())
        # EXTRAI OS DADOS, E RETORNA A TUPLA COM ELES
        return tuple(doc['data']['row'])

    # MONTA A TUPLA, COM OS OBJETOS PREENCHIDOS, E CADA OBJETO EQUIVALE A UMA LINNHA DA PLANILHA EM XML
    def monta_tupla_de_objetos(self,nome_arquivo):
        tupla_de_dados = self.retorna_tupla_dados(nome_arquivo)
        for tupla_dado in tupla_de_dados:
            objeto = Extracao_dados(
                convenio = tupla_dado['convenio'], 
                data_pagamento = tupla_dado['data_pagamento'], 
                numero_protocolo = tupla_dado['numero_protocolo'], 
                matricula = tupla_dado['matricula'], 
                nome = tupla_dado['nome'], 
                numero_guia = tupla_dado['numero_guia'], 
                ng_prest = tupla_dado['ng_prest'], 
                senha_guia = tupla_dado['senha_guia'], 
                codigo_produto = tupla_dado['codigo_produto'], 
                descricao_produto = tupla_dado['descricao_produto'], 
                valor_apresentado = tupla_dado['valor_apresentado'], 
                valor_pago = tupla_dado['valor_pago'], 
                valor_glosa = tupla_dado['valor_glosa'], 
                descricao_motivo = tupla_dado['descricao_motivo'], 
                codigo_motivo = tupla_dado['codigo_motivo'],
            )
            self.lista_objetos.append(objeto)

    # IMPRIMI A DADOS DE DADOS PARA TESTE DOS DADOS
    def imprimir_tupla_dados(self):
        contador = 0
        for obj in self.lista_objetos:
            contador += 1
            print("\nPosição da lista: ",contador)
            print(obj.__dict__)
            print("")

    # PASSA POR TODOS OS ARQUIVOS
    def varre_todos_arquivos(self):
        for nome in self.nome_arquivos:
            self.monta_tupla_de_objetos(nome)
            self.imprimir_tupla_dados()


    def executar_extracao_dados(self):
        self.coleta_nome_arquivos()
        self.varre_todos_arquivos()


a = Extracao_dados()
a.executar_extracao_dados()