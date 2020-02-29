class RootModel:

    # virtualização de atributo
    log_error=None
    user = None
    password = None

    def __init__(self, site, mode_execute, SQL_Long, platform_id, platform_name, estado='Default', grau='1'):
        self.path_download_prov = os.path.abspath('../../Downloads/' + estado + '/' + platform_name + '/' +str(grau)+'Grau/Download' + str(hex(id(self))))
        Tools.new_path(str(self.path_download_prov))
        self.site = site
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("prefs",
                                                    {"download.default_directory": r"" + str(self.path_download_prov),
                                                     "download.prompt_for_download": False,
                                                     "download.directory_upgrade": True,
                                                     "safebrowsing.enabled": False,
                                                     "safebrowsing_for_trusted_sources_enabled": False,
                                                     'download.extensions_to_open': 'msg',
                                                     "plugins.always_open_pdf_externally": True,
                                                     "profile.default_content_setting_values.automatic_downloads":True,
                                                     "profile.content_settings.exceptions.automatic_downloads.*.setting":True})
        # self.chrome_options.add_argument("--headless")


        self.visivel = mode_execute
        self.chrome_options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")


        # self.browser = None
        self.Access_AQL = SQL_Long
        self.platform_id = int(platform_id)
        self.platform_name = platform_name
        self.database = SQL(self.Access_AQL[0], self.Access_AQL[1], self.Access_AQL[2])
        self.montar_dicionario()
        # montar dicionario com o nome de todas as cidades do brasil para pegar a comarca
