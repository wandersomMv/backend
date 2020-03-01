
from Controller.GlosaMax import GlosaMax
from datetime import *
from Controller.BuscaZeroGlosa import ZeroGlosa
from Model.extrair_dados import Extracao_dados


class execute:


     def pegar_dicionarios_dados(self):

         objeto = Extracao_dados()
         # objeto.executar_extracao_dados_csv()
         # objeto.imprimir_dicionario()
         objeto.executar_extracao_dados_xml()  # dados
         # objeto.executar_extracao_dados_html() # dados glosamin
         objeto.monta_diacionario_de_objetos_do_banco()


         # objeto.imprimir_dicionario()
         return objeto.dicionario_chave_num_prestes # dicionario com as chaves e dados
         #numero_prest, numero guia => [dados]

     def buscar_donwloads_convenios(self):

        lista_convenios =  ['glosamin', 'glosamax', 'pagatudo']
        for i in lista_convenios: # lista de convenios

            a = GlosaMax(True, i)

            data = a.donwload_arquivos(convenio=i,data_ultima_coleta=datetime.strptime("2017-11-29", "%Y-%m-%d"))

            print(datetime.strftime(data, "%Y-%m-%d"))

            a.browser.quit()

        dados_novos = self.pegar_dicionarios_dados()

objeto = execute()
# objeto.buscar_donwloads_convenios()
objeto.pegar_dicionarios_dados()

#objeto = Extracao_dados()
# objeto.executar_extracao_dados_html()
# numero_prest, numero guia => [dados]












