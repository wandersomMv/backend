from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Model.botModel import RootModel
from datetime import *
import os
from Model.botModel import RootModel
class ZeroGlosa(RootModel):

    def __init__(self,site, mode_execute,pasta=""):
        super().__init__(site,mode_execute,'ZeroGlosa')



    def baixar_pagina(self,plataforma_id,convenioId,pagina):
        """baixa uma pagina em xml, o donwload de uma pagina contém 100 elementos"""

        base_link = "https://erp-time1.zeroglosa.com.br/erp-time1/guia/index?textoBusca=&prestadorId={}&convenioId={}&quitado=false&offset={}&max=100"

        link_da_pagina = base_link.format(plataforma_id,convenioId,str(int(pagina)*100)) # monta o link para ir para a página que será baixada

        self.browser.get(link_da_pagina) # ir para a pagina

        wait = WebDriverWait(self.browser ,10)
        wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/form/fieldset/input[2]'))) # esperar o botão do xml carregar

        n_files = len(os.listdir(self.path_download_prov))

        self.browser.find_element_by_xpath('/html/body/form/fieldset/input[2]').click()

        alert = self.browser.switch_to_alert()
        alert.accept()

        err_down = self.wait_download(n_files)  # esperar o download terminar, retorna verdadeiro se deu erro






    def donwload_planilhas_xml_orm(self,plataforma_id,convenioId,pagina):
        """função para baixar os arquivos no site da ZG, as planilhas"""

        for i in range(pagina):
            self.baixar_pagina(plataforma_id,convenioId,str(i))






