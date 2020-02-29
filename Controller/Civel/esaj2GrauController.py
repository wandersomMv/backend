# coding=utf-8
from Model.toolsModel import *
from Model.processoPlataformaModel import ProcessoPlataformaModel
from Model.Civel.esajModel import esajModel2Grau



class esajAmazonas2GrauController(esajModel2Grau):
    def __init__(self, site, mode_execute, access, platform_id, platform_name, flag, num_thread):
        state = 'AM'
        link_consulta = "https://consultasaj.tjam.jus.br/cposgcr/"
        super().__init__(site=site, mode_execute=mode_execute, access=access, platform_id=platform_id,
                         platform_name=platform_name, flag=flag, num_thread=num_thread,state=state,link_consulta=link_consulta)

class esajMatoGrossoDoSul2GrauController(esajModel2Grau):
    def __init__(self, site, mode_execute, access, platform_id, platform_name, flag, num_thread):
        state = 'MS'
        link_consulta = "https://esaj.tjms.jus.br/cposg5/open.do"
        super().__init__(site=site, mode_execute=mode_execute, access=access, platform_id=platform_id,
                         platform_name=platform_name, flag=flag, num_thread=num_thread,state=state,link_consulta=link_consulta)

class esajAcre2GrauController(esajModel2Grau):

    def __init__(self, site, mode_execute, access, platform_id, platform_name, flag, num_thread):
        state = 'AC'
        link_consulta = "https://esaj.tjac.jus.br/cposg5/open.do"
        super().__init__(site=site, mode_execute=mode_execute, access=access, platform_id=platform_id,
                         platform_name=platform_name, flag=flag, num_thread=num_thread,state=state,link_consulta=link_consulta)

        # SELECIONA PROCESSOS DO BANCO DE DADOS E PROCURA NA PLATAFORMA PARA UPDATE NO BANCO

    def search_process_to_update(self, user, password, row_database) :

        # INICIA O BROWSER E A SESSÃO NA PLATAFORMA
        self.initializer(user, password)

        # VERIFICA CADA NUMERO DE PROCESSO DENTRO DA ESTRUTURA FORNECIDA
        i_n = 0
        for i_proc in row_database :
            t0 = time.time()
            i_n += 1

            # VERIFICA SE O NAVEGADOR ESTÁ ABERTO
            try :
                if len(self.browser.window_handles) > 1 :
                    if self.browser is not None :
                        self.browser.quit()
                        self.log_error.insert_log('Sessão encerrou!')
                        return -1
                else :
                    try :
                        wait = WebDriverWait(self.browser, 1)
                        wait.until(EC.alert_is_present())
                        self.browser.quit()
                        self.log_error.insert_log('Sessão encerrou!')
                        return -1
                    except :
                        pass
            except :
                self.log_error.insert_log('navegador fechou!')
                return -1

            n_proc = i_proc[0]
            n_proc = re.sub('[^0-9]', '', n_proc)
            self.log_error.insert_title(n_proc)
            print("\t{}ª: Coleta de dados do processo: {}".format(i_n, n_proc).upper())

            # BUSCA PELO PROCESSO NA PLATAFORMA
            if self.busca_processo_na_plataforma(n_proc, i_proc, t0, self.log_error, self.state):
                continue

            print('num_proc->')
            # VAlIDANDOS SE NUMERO DO PROCESSO CONTIDO NA PLATAFORMA E O MESMO CONTIDO NO SITE

            num_proc = self.browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div/span[1]').text
            num_proc = re.sub('[^0-9]', '', num_proc)

                # a=input('DEU RUIM MEU REI')
            print('num_proc->', num_proc)

            if num_proc != n_proc:
                self.log_error.insert_log('numero do processo diferente')
                print('###Tempo total da coleta de dados do processo: {} SECS'.format(time.time() - t0).upper())
                print('-' * 65)

                continue

            #  COLETA OS ACOMPANHAMENTOS DO PROCESSO
            list_aud, list_acp_pra, list_name_urls, err1, not_refresh = self.acomp_down_aud(i_proc[1], i_proc[4])
            # list_aud, list_acp_pra, list_name_urls, err1, not_refresh = [], [], [], False, True

            if not err1 and ( self.flag or not_refresh is not 1) :
                # PEGA DADOS DO PROCESSO E ATUALIZA TABELA
                try :
                    classe = self.browser.find_element_by_xpath(
                        '/html/body/div[1]/div[2]/div/div[2]/div[1]/div/span').text.upper()

                except :
                    classe = None
                try :
                    vara = self.browser.find_element_by_xpath('/html/body/div[2]/table[3]/tbody/tr/td[3]').text.upper()

                except :
                    vara = None
                try :
                    assunto = self.browser.find_element_by_xpath(
                        '/html/body/div[1]/div[2]/div/div[2]/div[2]/div/span').text.upper()
                except :
                    assunto = None
                try :
                    status = self.browser.find_element_by_xpath(
                        '/html/body/div[1]/div[2]/div/div[1]/div/span[2]').text.upper()
                    if 'ARQUIVADO DEFINITIVAMENTE' in status or 'ARQUIVADO' in status or 'BAIXADO' :
                        status = 'ARQUIVADO'
                    else :
                        status = 'ATIVO'
                except :
                    status = None
                try :
                    self.browser.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/a').click()
                    wait = WebDriverWait(self.browser, 3)
                    wait.until(EC.visibility_of_element_located((By.ID, 'maisDetalhes')))
                    try :
                        valor_causa = self.browser.find_element_by_xpath('//*[@id="maisDetalhes"]/div/div[1]/div/span').text
                        valor_causa = Tools.treat_value_cause(valor_causa)
                    except :
                        valor_causa = None

                except :
                    valor_causa = None
                    dt_distribuicao = None

                try :
                    comarca = self.browser.find_element_by_xpath(
                        '//*[@id="maisDetalhes"]/div/div[2]/div/span').text.upper()
                    comarca = comarca.split('/')[0]
                except :
                    comarca = None

                print('\n----')
                print('valor_causa->', valor_causa)
                print('comarca->', comarca)
                print('vara->', vara)
                print('classe->', classe)
                print('status->', status)
                print('\n----')

                # IDENTIFICA OS ENVOLVIDOS E RETORNA UMA LISTA COM AS PARTES, OS ADVOGADOS E O JUIZ
                list_partes, list_advogs = self.envolvidos

                # CRIA O OBJETO PROCESSO-PLATAFORMA QUE SERÁ INSERIDO NO BANCO DE DADOS
                process_platform = ProcessoPlataformaModel(plp_prc_id=i_proc[1], plp_plt_id=self.platform_id,
                                                           plp_comarca=comarca,
                                                           plp_numero=n_proc, plp_status=status, plp_classe=classe,
                                                           plp_vara=vara, plp_grau=2, plp_valor_causa=valor_causa,
                                                           plp_assunto=assunto, plp_segredo=False, plp_localizado=True)

                list_objects_process = [
                    (process_platform, list_partes, list_advogs, list_aud, list_acp_pra, i_proc[7], [])]

                # INSERE A LISTA DE OBJETOS NO BANCO DE DADOS
                self.export_to_database(objects=list_objects_process, log=self.log_error, list_name_urls=list_name_urls,
                                        platform=self.platform_name, state=self.state, root=self)

                self.log_error.insert_info('Procedimento finalizado!')
            elif not err1 :
                # CRIA O OBJETO PROCESSO-PLATAFORMA QUE SERÁ INSERIDO NO BANCO DE DADOS
                process_platform = ProcessoPlataformaModel(plp_prc_id=i_proc[1], plp_plt_id=self.platform_id,
                                                           plp_numero=n_proc, plp_segredo=False, plp_localizado=True)

                list_objects_process = [(process_platform, [], [], list_aud, list_acp_pra, i_proc[7], [])]

                # INSERE A LISTA DE OBJETOS NO BANCO DE DADOS
                self.export_to_database(objects=list_objects_process, log=self.log_error, list_name_urls=list_name_urls,
                                        platform=self.platform_name, state=self.state, root=self)

                self.log_error.insert_info('Procedimento finalizado!')
            else :  # SENÃO FAZ UMA NOVA BUSCA
                # LIMPA A PASTA PARA RECEBER OS NOVOS DOWNLOADS
                self.clear_path_download()

            print('###Tempo total da coleta de dados do processo: {} SECS'.format(time.time() - t0).upper())
            print('-' * 65)

        # VERIFICA SE O NAVEGADOR FECHOU, SENÃO O FECHA
        if self.browser is not None :
            self.browser.quit()

        # # VERIFICA SE NÃO RETORNOU ALGUM PROCESSO DA BASE, SENÃO ATUALIZA A PLE_DATA
        # if i_n is 0 :
        #     self.update_ple_data(ple_plt_id=self.platform_id, ple_uf=self.state)
        return i_n















