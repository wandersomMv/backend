import os
import xlrd
import numpy as np
import datetime
import untangle
import xmltodict
import pandas as pd
from time import sleep
from Model.dados_planilhas import dados
from Model.dados_planilhas import guia
from Model.dados_planilhas import dados_item
from xml.etree import ElementTree as et
import xml.etree.ElementTree as ET

import requests
import xmltodict
import dicttoxml
from xml.etree import ElementTree as elements

class Extracao_dados:
    def __init__(self,nome_convenio):
        self.nome_convenio = nome_convenio
        self.nome_arquivos = []
        self.caminho_ate_pasta_downloads = ''
        self.lista_num_prestes = []
        self.dicionario_chave_num_prestes = {}
        self.caminho_pasta_dos_arquivos = ''
        self.dicionario_dados_site_orm = {}
    
    # COLETA O NOME DOS ARQUIVOS
    def coleta_nome_arquivos(self):
        caminhos_arquivos = os.getcwd()
        caminhos_arquivos = caminhos_arquivos.replace('Controller','')
        self.caminho_ate_pasta_downloads += caminhos_arquivos + "Downloads/"
        self.caminho_pasta_dos_arquivos = self.caminho_ate_pasta_downloads + self.nome_convenio
        self.nome_arquivos = os.listdir(self.caminho_pasta_dos_arquivos)

    # RETORNA UMA TUPLA COM OS DADOS DO ARQUIVOS XML
    def retorna_tupla_dados_dos_arquivos_xml(self,name):
        doc = ''
        # CRIA UM OBJETO DO TIPO DICIONARIO COM OS DADOS
        print("caminho para os arquivvos xml: ",self.caminho_pasta_dos_arquivos + "/" + name)
        with open(self.caminho_pasta_dos_arquivos + "/" + name) as fd:
            doc = xmltodict.parse(fd.read())
        # EXTRAI OS DADOS, E RETORNA A TUPLA COM ELES
        return tuple(doc['data']['row'])

    # RETORNA UMA TUPLA COM OS DADOS DO ARQUIVO HTML
    def retorna_tupla_dados_dos_arquivos_html(self,name):
        print("Nome do arquivo ",name)
        print("Caminho com o nome do arquivo: ",self.caminho_pasta_dos_arquivos + "/" + name)
        df_list = pd.read_html(self.caminho_pasta_dos_arquivos + "/" + name)
        planilha = pd.DataFrame(df_list[0])

        # EXTRAI OS DADOS DA PLANILHA HTML
        convenio = planilha['convenio']
        data_pagamento = planilha['data_pagamento']
        numero_protocolo = planilha['numero_protocolo']
        matricula = planilha['matricula']
        nome = planilha['nome']
        numero_guia = planilha['numero_guia']
        ng_prest = planilha['ng_prest']
        senha_guia = planilha['senha_guia']
        codigo_produto = planilha['codigo_produto']
        descricao_produto = planilha['descricao_produto']
        valor_apresentado = planilha['valor_apresentado']
        valor_pago = planilha['valor_pago']
        valor_glosa = planilha['valor_glosa']
        descricao_motivo = planilha['descricao_motivo']
        codigo_motivo = planilha['codigo_motivo']
        # -----------------------------------
        # TUPLA COM AS LISTAS DOS DADOS RETIRADOS DA PLANILHA EM HTML
        tupla_listas_dados = (convenio,data_pagamento,numero_protocolo,matricula,
                              nome,numero_guia,ng_prest,senha_guia,codigo_produto,
                              descricao_produto,valor_apresentado,valor_apresentado,
                              valor_pago,valor_glosa,descricao_motivo,codigo_motivo)
        print("tamanho da tupla de listas: ",len(tupla_listas_dados))
        return tupla_listas_dados


    # RETORNA UMA TUPLA COM OS DADOS DO ARQUIVO HTML
    def retorna_tupla_dados_dos_arquivos_csv(self,name):
        pass

    # MONTA O DICIONARIO, COM OS OBJETOS PREENCHIDOS, E CADA OBJETO EQUIVALE A UMA LINNHA DA PLANILHA EM XML
    def monta_diacionario_de_objetos_arquivos_xml(self,nome_arquivo):
        tupla_de_dados = self.retorna_tupla_dados_dos_arquivos_xml(nome_arquivo)
        print("tamanho tupla: ",len(tupla_de_dados))
        for tupla_dado in tupla_de_dados:
            objeto = dados(
                convenio = str(tupla_dado['convenio']),
                data_pagamento = str(tupla_dado['data_pagamento']),
                numero_protocolo = str(tupla_dado['numero_protocolo']),
                matricula = str(tupla_dado['matricula']),
                nome = str(tupla_dado['nome']),
                numero_guia = str(tupla_dado['numero_guia']),
                ng_prest = str(tupla_dado['ng_prest']),
                senha_guia = str(tupla_dado['senha_guia']),
                codigo_produto = str(tupla_dado['codigo_produto']),
                descricao_produto = str(tupla_dado['descricao_produto']),
                valor_apresentado = str(tupla_dado['valor_apresentado']),
                valor_pago = str(tupla_dado['valor_pago']),
                valor_glosa = str(tupla_dado['valor_glosa']),
                descricao_motivo = str(tupla_dado['descricao_motivo']),
                codigo_motivo = str(tupla_dado['codigo_motivo']),
            )
            tupla_chave_auxiliar = (objeto.ng_prest, objeto.numero_guia)
            # PEGA A LISTA DE CHAVES
            keys = list(self.dicionario_chave_num_prestes.keys())
            if len(keys) > 0 and tupla_chave_auxiliar in keys:
                self.dicionario_chave_num_prestes[tupla_chave_auxiliar].append(objeto)
            else:
                lista_aux = []
                lista_aux.append(objeto)
                self.dicionario_chave_num_prestes[tupla_chave_auxiliar] = lista_aux



    # MONTA O DICIONARIO, COM OS OBJETOS PREENCHIDOS, E CADA OBJETO EQUIVALE A UMA LINNHA DA PLANILHA EM HTML
    def monta_diacionario_de_objetos_arquivos_html(self, nome_arquivo):
        tupla_dados = self.retorna_tupla_dados_dos_arquivos_html(nome_arquivo)
        tam_lista_ng_prestes = len(tupla_dados[6])
        for i in range(tam_lista_ng_prestes):
            objeto = dados(
                convenio = str(tupla_dados[0][i]),
                data_pagamento = str(tupla_dados[1][i]),
                numero_protocolo = str(tupla_dados[2][i]),
                matricula = str(tupla_dados[3][i]),
                nome = str(tupla_dados[4][i]),
                numero_guia = str(tupla_dados[5][i]),
                ng_prest = str(tupla_dados[6][i]),
                senha_guia = str(tupla_dados[7][i]),
                codigo_produto = str(tupla_dados[8][i]),
                descricao_produto = str(tupla_dados[9][i]),
                valor_apresentado = str(tupla_dados[10][i]),
                valor_pago = str(tupla_dados[11][i]),
                valor_glosa = str(tupla_dados[12][i]),
                descricao_motivo = str(tupla_dados[13][i]),
                codigo_motivo = str(tupla_dados[14][i])
            )
            tupla_chave_auxiliar = (objeto.ng_prest,objeto.numero_guia)
            # PEGA A LISTA DE CHAVES
            keys = list(self.dicionario_chave_num_prestes.keys())
            if len(keys) > 0 and tupla_chave_auxiliar in keys:
                self.dicionario_chave_num_prestes[tupla_chave_auxiliar].append(objeto)
            else:
                lista_aux = []
                lista_aux.append(objeto)
                self.dicionario_chave_num_prestes[tupla_chave_auxiliar] = lista_aux


    # COLETA OS DADOS DO ARQUIVO XML BAIXADO NO SITE ORM
    def monta_dicionario_dados_orm(self,nome_arquivo):
        tree = ET.parse(self.caminho_pasta_dos_arquivos + "/" + nome_arquivo)
        root = tree.getroot()
        iterator = root.iter('guia')
        y = {}
        contador = 0
        for it in iterator:
            # MONTA A LISTA DE DICIONARIO COM OS ITENS DO XML COLETADO NO SITE DO ORM
            objeto = ''
            # MONTA A PARTE DOS DADOS DA GUIA
            for numeroGuia, nomeOperadora, nome_prestador, cnpj, nome_Beneficiario, matricula, dataAtendimento, valorTotalGuia in zip(it.iter('numeroGuia'),it.iter('nomeOperadora'),it.iter('nomePrestador'),it.iter('cnpj'),it.iter('nomeBeneficiario'),it.iter('matricula'),it.iter('dataAtendimento'),it.iter('valorTotalGuia')):
                objeto = guia(
                    numeroGuia = numeroGuia.text,
                    nomeOperadora = nomeOperadora.text,
                    nome_prestador = nome_prestador.text,
                    cnpj = cnpj.text,
                    nome_Beneficiario = nome_Beneficiario.text,
                    matricula = matricula.text,
                    dataAtendimento = dataAtendimento.text,
                    valorTotalGuia = valorTotalGuia.text
                )
            for numeroItem,codigo,nome_item,valorUnitario,quantidade,valorTotal in zip(it.iter('numeroItem'),it.iter('codigo'),it.iter('nome'),it.iter('valorUnitario'),it.iter('quantidade'),it.iter('valorTotal')):
                objeto_auxiliar = dados_item(
                    numeroItem = numeroItem.text,
                    codigo = codigo.text,
                    nome_item = nome_item.text,
                    valorUnitario = valorUnitario.text,
                    quantidade = quantidade.text,
                    valorTotal = valorTotal.text
                )
                objeto.lista_itens_da_guia.append(objeto_auxiliar)
            tupla_chave_auxiliar = (objeto.numeroGuia, objeto.matricula)
            # PEGA A LISTA DE CHAVES
            keys = list(self.dicionario_chave_num_prestes.keys())
            if len(keys) > 0 and tupla_chave_auxiliar in keys:
                print("repetido")
                self.dicionario_dados_site_orm[tupla_chave_auxiliar].append(objeto)
            else:
                lista_aux = []
                contador += 1
                print("objeto: ",objeto.__dict__,"\n")
                lista_aux.append(objeto)

                # print("chave dentro do else: ",tupla_chave_auxiliar)
                self.dicionario_dados_site_orm[tupla_chave_auxiliar] = lista_aux
                y[tupla_chave_auxiliar] = lista_aux
        print(contador)
        print("dicionario oficial: ",len(self.dicionario_dados_site_orm.keys()))
        print("dicionario auxiliar: ",len(y.keys()))


    # IMPRIMIR O DICIONARIO PARA TESTE
    def imprimir_dicionario(self):
        lista_chaves = self.dicionario_chave_num_prestes.keys()
        print("\nInicio da lista de chaves: -->{}<-- final da lista!\n".format(lista_chaves))
        for pos in lista_chaves:
            print("Imprimindo a lista para a chave {}".format(pos))
            lista = self.dicionario_chave_num_prestes[pos]
            print("lista dessa chave: --->{")
            for x in lista:
                print(x.__dict__)
            print(")}<---")
            print("-----------------------------------")
        print("Final da impressão!!!!!")


    # PASSA POR TODOS OS ARQUIVOS XML E PARA CADA ARQUIVO CHAMA A FUNÇÃO DE MONTAR DICIONARIO
    def varre_todos_arquivos_xml(self):
        for nome in self.nome_arquivos:
            self.monta_diacionario_de_objetos_arquivos_xml(nome)
            # self.imprimir_tupla_dados()

    # PASSA POR TODOS OS ARQUIVOS XML E PARA CADA ARQUIVO CHAMA A FUNÇÃO DE MONTAR DICIONARIO
    def varre_todos_arquivos_html(self):
        for nome in self.nome_arquivos:
            self.monta_diacionario_de_objetos_arquivos_html(nome)
            # self.imprimir_tupla_dados()

    # PEGA OS DADOS DOS ARQUIVOS XML QUE FORAM BAIXADOS NO SITE ORM
    def varre_todos_arquivos_orm(self):
        for nome_arquivo in self.nome_arquivos:
            self.monta_dicionario_dados_orm(nome_arquivo)

    # IMPRIMIR O DICIONARIO PARA TESTE
    def imprimir_dicionario_orm(self):
        lista_chaves = self.dicionario_dados_site_orm.keys()
        print("Quantidade de chaves do dicionario: ",len(lista_chaves))
        print("\nInicio da lista de chaves: -->{}<-- final da lista!\n".format(lista_chaves))
        cont = 0
        for pos in lista_chaves:
            cont += 1
            print("Imprimindo a lista para a chave {}".format(pos))
            lista = self.dicionario_dados_site_orm[pos]
            print(len(lista))
            # for k in lista:
            #     lista_auxiliar_itens = k.lista_itens_da_guia
            #     print("imprimindo os itens desta guia: ")
            #     for i in lista_auxiliar_itens:
            #         print(i.__dict__)
        print("cont: ",cont)
    def executar_extracao_dados(self):
        self.coleta_nome_arquivos()
        self.varre_todos_arquivos_orm()
        # self.imprimir_dicionario_orm()
        # self.varre_todos_arquivos_html()
        # self.imprimir_dicionario()
        # self.varre_todos_arquivos_xml()
        # self.imprimir_dicionario()


