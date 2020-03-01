from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Model.botModel import RootModel
from datetime import *
import os
class GlosaMax(RootModel):

    def __init__(self,visivel,pasta): # para iniciar o browser
        super().__init__(visivel,pasta)


    def dowload_convenio_glosas(self,data_ultima_coleta,convenio): # todos os arquivo dos convenios glosas são baixados aqui
        # data_ultima_coleta é a data de até onde foi pego os donwloads da ultima vez que varreu, convennio sera onde ele sera buscado
        """função que baixa os arquvios dos convenios glosasmax, glosamin e pegatudo, esses arquivos são armazenados em uma pasta de donwload e dentro dessa pasta donwload tem a
        pasta dos determinados convenios"""

        link_base = 'https://{}.zeroglosa.com.br/{}/arquivo/download?nome={}_{}.{}&data={}'  # base do link para download
        extensao = ''
        if 'glosamin' in convenio:
            extensao = 'html'
        elif 'glosamax' in convenio:
            extensao = 'xml'
        else:
            extensao = 'csv'

        self.browser.get('https://{}.zeroglosa.com.br/{}/arquivo/index'.format(convenio,convenio))

        wait = WebDriverWait(self.browser, 10)  # será usado para esperar a tabela de download aparecer
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="list-arquivo"]/div/a')))  # esperar aparecer a tabela onde contém os download

        tabela_donwload = self.browser.find_elements_by_xpath('//*[@id="list-arquivo"]/div/a')  # pegar os elemetos da tabela

        lista_data = []
        for elementos in tabela_donwload:  # pegar as datas para fazer os donwloads

            data_elemento = str(elementos.text)  # pegar a data do elemento atual
            aux_data = datetime.strptime(data_elemento, "%Y-%m-%d")  # passar para o formato datatime
            lista_data.append(aux_data) # pegar a data


        lista_data.sort()
        lista_data.reverse()


        for elementos in lista_data:

            if data_ultima_coleta != None and data_ultima_coleta > elementos:
                break
            data_elemento =datetime.strftime(elementos, "%Y-%m-%d")
            link_donwload = link_base.format(convenio,convenio,convenio,data_elemento,extensao, data_elemento)  # montar a url para fazer o download

            n_files = len(os.listdir(self.path_download_prov))
            self.browser.execute_script('''window.open("{}","_blank");'''.format(link_donwload))  # Abrir nova aba e faz o donwload

            err_down = self.wait_download(n_files)  # esperar o download terminar, retorna verdadeiro se deu erro

        if len(lista_data) >0 and lista_data[0] > data_ultima_coleta: # ultima movimentação
            return lista_data[0]
        else:
            return data_ultima_coleta


    def donwload_arquivos(self,data_ultima_coleta = None, convenio=None):
        """Função faz o donwload de um convenio especifico, se não passar a data da ultima coleta, faz-se o donwload de todos os arquivos na plataforma
        """
        # data_ultima_coleta é a data de até onde foi pego os donwloads da ultima vez que varreu, convennio sera onde ele sera buscado

        glosas = ['glosamin','glosamax','pagatudo'] # lista de convenios
        if convenio!= None and convenio in glosas:
            return self.dowload_convenio_glosas(data_ultima_coleta,convenio)








