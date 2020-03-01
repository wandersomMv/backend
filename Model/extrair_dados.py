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
from Database.connDatabase import SQL, dados
from Model.lista_insercao import lista_insercao

import requests
import xmltodict
import dicttoxml
from xml.etree import ElementTree as elements


class Extracao_dados:
    def __init__(self):
        self.nome_convenio = ""
        self.nome_arquivos = []
        self.caminho_ate_pasta_downloads = ''
        self.lista_num_prestes = []
        self.dicionario_chave_num_prestes = {}
        self.caminho_pasta_dos_arquivos = ''
        self.dicionario_dados_site_orm = {}
        self.caminhos_arquivos = ''
        self.lista_dados_errados = []

    # COLETA O NOME DOS ARQUIVOS
    def coleta_nome_arquivos(self):
        caminhos_arquivos = os.getcwd()
        caminhos_arquivos = caminhos_arquivos.replace('Controller', '')
        caminhos_arquivos = caminhos_arquivos.replace('View', '')
        self.caminho_ate_pasta_downloads = caminhos_arquivos + "Downloads/"
        self.caminho_pasta_dos_arquivos = self.caminho_ate_pasta_downloads + self.nome_convenio
        self.nome_arquivos = os.listdir(self.caminho_pasta_dos_arquivos)

    # RETORNA UMA TUPLA COM OS DADOS DO ARQUIVOS XML
    def retorna_tupla_dados_dos_arquivos_xml(self, name):
        doc = ''
        # CRIA UM OBJETO DO TIPO DICIONARIO COM OS DADOS
        print("caminho para os arquivvos xml: ", self.caminho_pasta_dos_arquivos + "/" + name)
        with open(self.caminho_pasta_dos_arquivos + "/" + name, encoding='utf-8') as fd:
            doc = xmltodict.parse(fd.read(), encoding='utf-8')
        # EXTRAI OS DADOS, E RETORNA A TUPLA COM ELES
        return tuple(doc['data']['row'])

    # RETORNA UMA TUPLA COM OS DADOS DO ARQUIVO HTML
    def retorna_tupla_dados_dos_arquivos_html(self, name):
        print("Nome do arquivo ", name)
        print("Caminho com o nome do arquivo: ", self.caminho_pasta_dos_arquivos + "/" + name)
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
        tupla_listas_dados = (convenio, data_pagamento, numero_protocolo, matricula,
                              nome, numero_guia, ng_prest, senha_guia, codigo_produto,
                              descricao_produto, valor_apresentado, valor_apresentado,
                              valor_pago, valor_glosa, descricao_motivo, codigo_motivo)
        print("tamanho da tupla de listas: ", len(tupla_listas_dados))
        return tupla_listas_dados

    # RETORNA UMA TUPLA COM OS DADOS DO ARQUIVO HTML
    def retorna_tupla_dados_dos_arquivos_csv(self, name):
        caminho_ate_arquivo = self.caminho_pasta_dos_arquivos + "/" + name
        print(caminho_ate_arquivo)
        train_dataset = pd.read_csv(caminho_ate_arquivo, sep='\t')
        convenio = train_dataset['convenio']
        data_pagamento = train_dataset['data_pagamento']
        numero_protocolo = train_dataset['numero_protocolo']
        matricula = train_dataset['matricula']
        nome = train_dataset['nome']
        numero_guia = train_dataset['numero_guia']
        ng_prest = train_dataset['numero_guia_prestador']
        senha_guia = train_dataset['senha']
        codigo_produto = train_dataset['codigo']
        descricao_produto = train_dataset['descricao']
        valor_apresentado = train_dataset['valor_apresentado']
        valor_pago = train_dataset['valor_pago']
        valor_glosa = train_dataset['valor_glosa']
        descricao_motivo = train_dataset['descricao_motivo']
        codigo_motivo = train_dataset['codigo_motivo']
        # -----------------------------------
        # TUPLA COM AS LISTAS DOS DADOS RETIRADOS DA train_dataset EM HTML
        tupla_listas_dados = (convenio, data_pagamento, numero_protocolo, matricula,
                              nome, numero_guia, ng_prest, senha_guia, codigo_produto,
                              descricao_produto, valor_apresentado, valor_apresentado,
                              valor_pago, valor_glosa, descricao_motivo, codigo_motivo)
        print("tamanho da tupla de listas: ", len(tupla_listas_dados))
        return tupla_listas_dados

    # MONTA O DICIONARIO, COM OS OBJETOS PREENCHIDOS, E CADA OBJETO EQUIVALE A UMA LINNHA DA PLANILHA EM XML
    def monta_diacionario_de_objetos_arquivos_xml(self, nome_arquivo):
        tupla_de_dados = self.retorna_tupla_dados_dos_arquivos_xml(nome_arquivo)
        print("tamanho tupla: ", len(tupla_de_dados))
        for tupla_dado in tupla_de_dados:
            objeto = dados(
                convenio=str(tupla_dado['convenio']),
                data_pagamento=str(tupla_dado['data_pagamento']),
                numero_protocolo=str(tupla_dado['numero_protocolo']),
                matricula=str(tupla_dado['matricula']),
                nome=str(tupla_dado['nome']),
                numero_guia=str(tupla_dado['numero_guia']),
                ng_prest=str(tupla_dado['ng_prest']),
                senha_guia=str(tupla_dado['senha_guia']),
                codigo_produto=str(tupla_dado['codigo_produto']),
                descricao_produto=str(tupla_dado['descricao_produto']),
                valor_apresentado=str(tupla_dado['valor_apresentado']),
                valor_pago=str(tupla_dado['valor_pago']),
                valor_glosa=str(tupla_dado['valor_glosa']),
                descricao_motivo=str(tupla_dado['descricao_motivo']),
                codigo_motivo=str(tupla_dado['codigo_motivo']),
            )
            tupla_chave_auxiliar = (objeto.ng_prest, objeto.numero_guia)
            # print("Conteudo da tupla: ",tupla_chave_auxiliar)
            # PEGA A LISTA DE CHAVES
            keys = list(self.dicionario_chave_num_prestes.keys())
            if len(keys) > 0 and tupla_chave_auxiliar in keys:
                self.dicionario_chave_num_prestes[tupla_chave_auxiliar].append(objeto)
            else:
                lista_aux = []
                lista_aux.append(objeto)
                self.dicionario_chave_num_prestes[tupla_chave_auxiliar] = lista_aux

    def monta_diacionario_de_objetos_do_banco(self):

        banco = SQL(user="time3", password="aFp5yEFVvGrfAu9c", host='servidor-maratona,zeroglossa.com.br', port='5432',
                    database="time3")

        nova_dict = {}
        for i, y in self.dicionario_chave_num_prestes.items():
            print("i ",i)
            try:
                resultado = banco.Select_dados_zero_glosa(dados(ng_prest=i[0], numero_guia=i[1]))
                nova_dict[i] = resultado
               # print("vo chora dms: ",resultado)
                break
            except:
                self.lista_dados_errados.append((i[0],i[1]))
            encontrou = False
            objeto_lista_final = ''
            lista_resultado_comparacao = []
            # FAZ A COMPARAÇÃO COM OS DADOS BUSCADOS NA BASE
            lista_objetos = self.dicionario_chave_num_prestes[i]
            lista_na_chave_dict_banco = resultado[i]
            for obj in lista_objetos:
                for obj_base in lista_na_chave_dict_banco:
                    if obj.codigo_produto == obj_base.codigo_produto:
                        encontrou = True
                        print("Encontrei o produto!")
                        if obj.valor_pago == obj_base.valor_apresentado:
                            objeto_lista_final = lista_insercao(
                                convenio= obj.convenio,
                                data_pagamento=obj.data_pagamento,
                                numero_protocolo=obj.numero_protocolo,
                                matricula=obj.matricula,
                                nome=obj.nome,
                                numero_guia=obj.numero_guia,
                                ng_prest=obj.ng_prest,
                                senha_guia=obj.senha_guia,
                                codigo_produto=obj.codigo_produto,
                                descricao_produto=obj.descricao_produto,
                                valor_apresentado=obj.valor_apresentado,
                                valor_pago=obj.valor_pago,
                                valor_glosa= '0',
                                descricao_motivo=obj.descricao_motivo,
                                codigo_motivo=obj.codigo_motivo,
                                status= 'pago'
                            )
                        else:
                            objeto_lista_final = lista_insercao(
                                convenio=obj.convenio,
                                data_pagamento=obj.data_pagamento,
                                numero_protocolo=obj.numero_protocolo,
                                matricula=obj.matricula,
                                nome=obj.nome,
                                numero_guia=obj.numero_guia,
                                ng_prest=obj.ng_prest,
                                senha_guia=obj.senha_guia,
                                codigo_produto=obj.codigo_produto,
                                descricao_produto=obj.descricao_produto,
                                valor_apresentado=obj.valor_apresentado,
                                valor_pago=obj.valor_pago,
                                valor_glosa= obj_base.valor_glosa - obj.valor_glosa,
                                descricao_motivo=obj.descricao_motivo,
                                codigo_motivo=obj.codigo_motivo,
                                status='não pago'
                            )
            if not encontrou:
                objeto_lista_final = lista_insercao(
                    convenio=obj.convenio,
                    data_pagamento=obj.data_pagamento,
                    numero_protocolo=obj.numero_protocolo,
                    matricula=obj.matricula,
                    nome=obj.nome,
                    numero_guia=obj.numero_guia,
                    ng_prest=obj.ng_prest,
                    senha_guia=obj.senha_guia,
                    codigo_produto=obj.codigo_produto,
                    descricao_produto=obj.descricao_produto,
                    valor_apresentado=obj.valor_apresentado,
                    valor_pago=obj.valor_pago,
                    valor_glosa=obj_base.valor_glosa - obj.valor_glosa,
                    descricao_motivo=obj.descricao_motivo,
                    codigo_motivo=obj.codigo_motivo,
                    status='não pago'
                )
            lista_resultado_comparacao.append(objeto_lista_final)
        return lista_resultado_comparacao





        banco.__del__()
        result = nova_dict


    # def gravar__dados(self):
    #
    #     self.dicionario_chave_num_banco=self.monta_diacionario_de_objetos_do_banco()
    #
    #     dict_dados_tratados=[]
    #
    #     for i in self.dicionario_chave_num_prestes.keys:
    #         lista_a= self.dicionario_chave_num_prestes[i]
    #         lista_b=  self.dicionario_chave_num_banco[i]
    #         key=[lista_a[0].convenio,lista_a[0].data_pagamento,
    #              lista_a[0].numero_protocolo,lista_a[0].matricula,
    #              lista_a[0].nome,lista_a[0].numero_guia,lista_a[0].ng_prest,
    #              lista_a[0].senha_guia,
    #              ]
    #         dict_dados_tratados.append([lista_a[0].convenio,lista_a[0].data_pagamento,
    #              lista_a[0].numero_protocolo,lista_a[0].matricula,
    #              lista_a[0].nome,lista_a[0].numero_guia,lista_a[0].ng_prest,
    #              lista_a[0].senha_guia,
    #              ])




    # MONTA O DICIONARIO, COM OS OBJETOS PREENCHIDOS, E CADA OBJETO EQUIVALE A UMA LINNHA DA PLANILHA EM HTML
    def monta_diacionario_de_objetos_arquivos_html(self, nome_arquivo):
        tupla_dados = self.retorna_tupla_dados_dos_arquivos_html(nome_arquivo)
        tam_lista_ng_prestes = len(tupla_dados[6])
        for i in range(tam_lista_ng_prestes):
            objeto = dados(
                convenio=str(tupla_dados[0][i]),
                data_pagamento=str(tupla_dados[1][i]),
                numero_protocolo=str(tupla_dados[2][i]),
                matricula=str(tupla_dados[3][i]),
                nome=str(tupla_dados[4][i]),
                numero_guia=str(tupla_dados[5][i]),
                ng_prest=str(tupla_dados[6][i]),
                senha_guia=str(tupla_dados[7][i]),
                codigo_produto=str(tupla_dados[8][i]),
                descricao_produto=str(tupla_dados[9][i]),
                valor_apresentado=str(tupla_dados[10][i]),
                valor_pago=str(tupla_dados[11][i]),
                valor_glosa=str(tupla_dados[12][i]),
                descricao_motivo=str(tupla_dados[13][i]),
                codigo_motivo=str(tupla_dados[14][i])
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

    # PEGA A TUPLA DE DADOS DOS ARQUIVOS CSV, E MONTA O DICIONARIO
    def monta_diacionario_de_objetos_arquivos_csv(self, nome_arquivo):
        tupla_dados = self.retorna_tupla_dados_dos_arquivos_csv(nome_arquivo)
        tam_lista_ng_prestes = len(tupla_dados[6])
        for i in range(tam_lista_ng_prestes):
            objeto = dados(
                convenio=str(tupla_dados[0][i]),
                data_pagamento=str(tupla_dados[1][i]),
                numero_protocolo=str(tupla_dados[2][i]),
                matricula=str(tupla_dados[3][i]),
                nome=str(tupla_dados[4][i]),
                numero_guia=str(tupla_dados[5][i]),
                ng_prest=str(tupla_dados[6][i]),
                senha_guia=str(tupla_dados[7][i]),
                codigo_produto=str(tupla_dados[8][i]),
                descricao_produto=str(tupla_dados[9][i]),
                valor_apresentado=str(tupla_dados[10][i]),
                valor_pago=str(tupla_dados[11][i]),
                valor_glosa=str(tupla_dados[12][i]),
                descricao_motivo=str(tupla_dados[13][i]),
                codigo_motivo=str(tupla_dados[14][i])
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

    # COLETA OS DADOS DO ARQUIVO XML BAIXADO NO SITE ORM
    def monta_dicionario_dados_orm(self, nome_arquivo):
        tree = ET.parse(self.caminho_pasta_dos_arquivos + "/" + nome_arquivo)
        root = tree.getroot()
        iterator = root.iter('guia')
        y = {}
        contador = 0
        for it in iterator:
            # MONTA A LISTA DE DICIONARIO COM OS ITENS DO XML COLETADO NO SITE DO ORM
            objeto = ''
            # MONTA A PARTE DOS DADOS DA GUIA
            for numeroGuia, nomeOperadora, nome_prestador, cnpj, nome_Beneficiario, matricula, dataAtendimento, valorTotalGuia in zip(
                    it.iter('numeroGuia'), it.iter('nomeOperadora'), it.iter('nomePrestador'), it.iter('cnpj'),
                    it.iter('nomeBeneficiario'), it.iter('matricula'), it.iter('dataAtendimento'),
                    it.iter('valorTotalGuia')):
                objeto = guia(
                    numeroGuia=numeroGuia.text,
                    nomeOperadora=nomeOperadora.text,
                    nome_prestador=nome_prestador.text,
                    cnpj=cnpj.text,
                    nome_Beneficiario=nome_Beneficiario.text,
                    matricula=matricula.text,
                    dataAtendimento=dataAtendimento.text,
                    valorTotalGuia=valorTotalGuia.text
                )
            for numeroItem, codigo, nome_item, valorUnitario, quantidade, valorTotal in zip(it.iter('numeroItem'),
                                                                                            it.iter('codigo'),
                                                                                            it.iter('nome'),
                                                                                            it.iter('valorUnitario'),
                                                                                            it.iter('quantidade'),
                                                                                            it.iter('valorTotal')):
                objeto_auxiliar = dados_item(
                    numeroItem=numeroItem.text,
                    codigo=codigo.text,
                    nome_item=nome_item.text,
                    valorUnitario=valorUnitario.text,
                    quantidade=quantidade.text,
                    valorTotal=valorTotal.text
                )
                objeto.lista_itens_da_guia.append(objeto_auxiliar)
            tupla_chave_auxiliar = (objeto.numeroGuia, objeto.numeroGuia)
            # PEGA A LISTA DE CHAVES
            keys = list(self.dicionario_chave_num_prestes.keys())
            if len(keys) > 0 and tupla_chave_auxiliar in keys:
                print("repetido")
                self.dicionario_dados_site_orm[tupla_chave_auxiliar].append(objeto)
            else:
                lista_aux = []
                contador += 1
                lista_aux.append(objeto)
                # print("chave dentro do else: ",tupla_chave_auxiliar)
                self.dicionario_dados_site_orm[tupla_chave_auxiliar] = lista_aux

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

    # PEGA OS DADOS DOS ARQUIVOS CSV QUE FORAM BAIXADOS DO SITE DO CONVENIO
    def varre_todos_arquivos_csv(self):
        for nome_arquivo in self.nome_arquivos:
            self.monta_diacionario_de_objetos_arquivos_csv(nome_arquivo)

    # IMPRIMIR O DICIONARIO PARA TESTE
    def imprimir_dicionario_orm(self):
        lista_chaves = self.dicionario_dados_site_orm.keys()
        print("Quantidade de chaves do dicionario: ", len(lista_chaves))
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
        print("cont: ", cont)

    def executar_extracao_dados_html(self):
        self.nome_convenio = 'glosamin'
        self.coleta_nome_arquivos()
        self.varre_todos_arquivos_html()

    # APAGA A PASTA DOWNLAOD DPS DE INSERIR OS DADOS NO BANCO DE DADOS
    def apaga_pasta_downlaod(self):
        os.chdir(self.caminhos_arquivos)
        os.system('rm -rf Downloads')

    def executar_extracao_dados(self):
        self.coleta_nome_arquivos()
        self.varre_todos_arquivos_csv()
        self.imprimir_dicionario()
        # self.apaga_pasta_downlaod()
        # self.varre_todos_arquivos_orm()
        # self.imprimir_dicionario_orm()
        self.varre_todos_arquivos_html()
        # self.imprimir_dicionario()
        # self.varre_todos_arquivos_xml()
        # self.imprimir_dicionario()

    def executar_extracao_dados_xml(self):

        self.nome_convenio = 'glosamax'
        self.coleta_nome_arquivos()
        # self.imprimir_dicionario_orm()
        self.varre_todos_arquivos_xml()

    def executar_extracao_dados_csv(self):
        self.nome_convenio = 'pagatudo'
        self.coleta_nome_arquivos()
        self.varre_todos_arquivos_csv()


