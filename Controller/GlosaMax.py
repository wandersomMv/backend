from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Model.botModel import RootModel
from datetime import *
import os
class GlosaMax(RootModel):

    def __init__(self,site,visivel,pasta): # para iniciar o browser
        super().__init__(site,visivel,pasta)


    def dowload_convenio_glosas(self,data_ultima_coleta,convenio): # todos os arquivo dos convenios glosas são baixados aqui
        # data_ultima_coleta é a data de até onde foi pego os donwloads da ultima vez que varreu, convennio sera onde ele sera buscado

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
        wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//*[@id="list-arquivo"]/div/a')))  # esperar aparecer a tabela onde contém os download

        tabela_donwload = self.browser.find_elements_by_xpath(
            '//*[@id="list-arquivo"]/div/a')  # pegar os elemetos da tabela

        for elementos in tabela_donwload:  # pegar as datas para fazer os donwloads

            data_elemento = str(elementos.text)  # pegar a data do elemento atual
            aux_data = datetime.strptime(data_elemento, "%Y-%m-%d")  # passar para o formato datatime

            if data_ultima_coleta != None and data_ultima_coleta >= aux_data:
                break

            link_donwload = link_base.format(convenio,convenio,convenio,data_elemento,extensao, data_elemento)  # montar a url para fazer o download
            self.browser.execute_script(
                '''window.open("{}","_blank");'''.format(link_donwload))  # Abrir nova aba e faz o donwload
            n_files = len(os.listdir(self.path_download_prov))
            err_down = self.wait_download(n_files)  # esperar o download terminar, retorna verdadeiro se deu erro



    def donwload_arquivos(self,data_ultima_coleta = None, convenio=None):

        # data_ultima_coleta é a data de até onde foi pego os donwloads da ultima vez que varreu, convennio sera onde ele sera buscado

        glosas = ['glosamin','glosamax','pagatudo'] # lista de convenios
        if convenio!= None and convenio in glosas:
            self.dowload_convenio_glosas(data_ultima_coleta,convenio)


