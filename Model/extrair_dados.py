import os
import untangle
import xmltodict
import datetime
from time import sleep
from Model.dados_planilhs import dados
from xml.etree import ElementTree as et

class Extracao_dados:
    def __init__(self):
        self.nome_arquivos = []
        self.caminho_ate_pasta_downloads = ''
        self.lista_num_prestes = []
        self.dicionario_chave_num_prestes = {}


    
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

    # MONTA O DICIONARIO, COM OS OBJETOS PREENCHIDOS, E CADA OBJETO EQUIVALE A UMA LINNHA DA PLANILHA EM XML
    def monta_diacionario_de_objetos(self,nome_arquivo):
        tupla_de_dados = self.retorna_tupla_dados(nome_arquivo)
        for tupla_dado in tupla_de_dados:
            objeto = dados(
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
            if objeto.ng_prest in self.dicionario_chave_num_prestes.keys():
                print("ng_prest: ",objeto.ng_prest)
                self.dicionario_chave_num_prestes[objeto.ng_prest].append(objeto)
            else:
                lista_aux = []
                lista_aux.append(objeto)
                self.dicionario_chave_num_prestes[objeto.ng_prest] = lista_aux


    # IMPRIMI A DADOS DE DADOS PARA TESTE DOS DADOS
    # def imprimir_tupla_dados(self):
    #     contador = 0
    #     for obj in self.lista_objetos:
    #         contador += 1
    #         print("\nPosição da lista: ",contador)
    #         print(obj.__dict__)
    #         print("")

    def imprimir_dicionario(self):
        lista_num_prestes = self.dicionario_chave_num_prestes.keys()
        print("\nInicio da lista de chaves: -->{}<-- final da lista!\n".format(lista_num_prestes))
        for pos in lista_num_prestes:
            print("Imprimindo a lista para a chave {}".format(pos))
            lista = self.dicionario_chave_num_prestes[pos]
            print("lista dessa chave: --->{")
            for x in lista:
                print(x.__dict__)
            print(")}<---")
            print("-----------------------------------")
        print("Final da impressão!!!!!")


    # PASSA POR TODOS OS ARQUIVOS
    def varre_todos_arquivos(self):
        for nome in self.nome_arquivos:
            self.monta_diacionario_de_objetos(nome)
            # self.imprimir_tupla_dados()


    def executar_extracao_dados(self):
        self.coleta_nome_arquivos()
        self.varre_todos_arquivos()
        self.imprimir_dicionario()


