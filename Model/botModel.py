
#https://glosamax.zeroglosa.com.br
import abc, os, re, shutil
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium import  webdriver
import  time

class RootModel:

    def __init__(self, site, mode_execute,pasta=""):
        
        self.path_download_prov = os.path.abspath('../Downloads/' + pasta) # nome para criar uma pasta provisoria para o robo
        self.criar_pasta(str(self.path_download_prov)) # criar a pasta
        self.site = site # site que fará a busca
        self.chrome_options = webdriver.ChromeOptions() # preferencias do googlecrome
        #'safebrowsing'
        self.chrome_options.add_experimental_option("prefs",
                                                    {"download.default_directory": r"" + str(self.path_download_prov),
                                                     "download.prompt_for_download": False,
                                                     "download.directory_upgrade": True,
                                                     "safebrowsing.enabled": True,
                                                     "safebrowsing_for_trusted_sources_enabled": False,
                                                     'download.extensions_to_open': 'xml',
                                                     "plugins.always_open_pdf_externally": True,
                                                     "profile.default_content_setting_values.automatic_downloads":True,
                                                     "profile.content_settings.exceptions.automatic_downloads.*.setting":True,
                                                    })
        #self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--safebrowsing-disable-download-protection")
        self.chrome_options.add_argument("--safebrowsing-disable-extension-blacklist")

        self.visivel = mode_execute
        self.chrome_options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
        self.init_browser() # iniciar o browser

    def criar_pasta(self,nome_pasta):
        try:
            os.makedirs(nome_pasta, 0o777, False)
            return True
        except Exception:
            return False

    def init_browser(self):

            print("INICIANDO BROWSER")
            local = str( os.path.abspath('../WebDriver/chromedriver.exe'))
            self.browser = webdriver.Chrome(local, options=self.chrome_options)
            self.browser.maximize_window()
            self.browser.get(self.site)

            #if self.visivel:
                #self.browser.set_window_position(-10000, 0)

            return True

    def wait_download(self, n_files):
        temp_inicio = time.time()
        baixando = True

        # try:
        temp_inicio = time.time()
        baixando = True

        while baixando:

            if (time.time() - temp_inicio) >= 80:  # passou  um minto
                return True

            dir = os.listdir(self.path_download_prov)
            if n_files < len(dir):  # se tem mais um donwload

                for j in range(0, len(dir)):
                    if dir[j].endswith('.crdownload') or dir[j].endswith('.tmp'):
                        baixando = True
                        break
                    else:
                        baixando = False
        return False

