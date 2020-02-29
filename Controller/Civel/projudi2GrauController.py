from Model.toolsModel import *
from Model.processoPlataformaModel import ProcessoPlataformaModel
from Controller.Civel.projudiController import projudiRoraimaController,projudiAmazonasController,projudiParaController,projudiMaranhaoController


class projudiRoraima2GrauController(projudiRoraimaController):
    def __init__(self, site, mode_execute, access, platform_id, platform_name, flag,num_thread):

        self.link_buscar_processo_2_grau = None
        super().__init__(site=site,mode_execute=mode_execute, access=access,platform_id= platform_id,
                         platform_name=platform_name,flag= flag,num_thread=num_thread,grau='2Grau')

    # SELECIONA PROCESSOS DO BANCO DE DADOS E PROCURA NA PLATAFORMA PARA UPDATE NO BANCO
    def search_process_to_update(self, user, password, row_database):
        # INICIA O BROWSER E A SESSÃO NA PLATAFORMA
        self.initializer(user, password)

        # VERIFICA CADA NUMERO DE PROCESSO DENTRO DA ESTRUTURA FORNECIDA
        i_n = 0
        for i_proc in row_database:
            # FRAGIMENTAR DADOS DO PROCESSO
            i_n += 1
            prc_numero, prc_id, prc_estado, plp_status, cadastro, plp_codigo, plp_data_update, plp_id, plp_numero, plp_localizado, \
            t0, bool_2_grau_numero, list_plp_2_grau = self.fragimentar_dados_dos_processo(dados_do_prosseco=i_proc)

            # VERIFICA SE O NAVEGADOR ESTÁ ABERTO
            if not self.verificar_se_o_navegador_esta_aberto():
                continue

            # EXIBIÇÃO DE INFORMAÇÕES PREVIAS E TRATAMENTO DO PRC_NUMERO
            self.print_info_previo_e_trata_prc_numero(prc_numero=prc_numero, prc_id=prc_id, plp_id=plp_id, i_n=i_n)

            # BUSCA PELO PROCESSO NA PLATAFORMA
            nao_achou = self.busca_processo_na_plataforma(prc_numero=prc_numero, tupla_processo=i_proc,
                                                          t0=t0, state=self.state,
                                                          log=self.log_error, row_database=row_database)
            if nao_achou:
                continue
            self.request_access()

            # COLETA OS ACOMPANHAMENTOS DO PROCESSO
            list_aud, list_acp_pra, list_name_urls, err1 \
                , not_refresh = self.acomp_down_aud(prc_id=prc_id, ult_mov=cadastro)


            if not err1 and (self.flag or not_refresh is not 1):
                # PEGA DADOS DO PROCESSO E ATUALIZA TABELA
                self.browser.find_element_by_xpath('//*[@id="tabItemprefix0"]/div[2]/a').click()
                try:
                    juizo = self.browser.find_element_by_xpath('//*[@id="includeContent"]/fieldset/'
                                                               'table/tbody/tr[2]/td[5]').text.upper()
                    juizo = Tools.remove_accents(juizo)
                except:
                    juizo = None
                try:
                    classe = self.browser.find_element_by_xpath('//*[@id="informacoesProcessuais"]/'
                                                                'tbody/tr[2]/td[2]/a').text.upper()
                    classe = Tools.remove_accents(classe)
                except:
                    classe = None
                try:
                    status = self.browser.find_element_by_xpath('//*[@id="includeContent"]/fieldset/'
                                                                'table/tbody/tr[6]/td[2]').text.upper()
                    if 'ARQUIVADO DEFINITIVAMENTE' in status or 'ARQUIVADO' in status or 'BAIXADO' in status:
                        status = 'ARQUIVADO'
                    else:
                        status = 'ATIVO'
                except:
                    status = None
                try:
                    assunto = self.browser.find_element_by_xpath('//*[@id="informacoesProcessuais"]/'
                                                                 'tbody/tr[2]/td[2]/a').text.upper()
                    assunto = Tools.remove_accents(assunto)
                except:
                    assunto = None
                try:
                    fase = self.browser.find_element_by_xpath('//*[@id="includeContent"]/'
                                                              'fieldset/table/tbody/tr[5]/td[5]').text.upper()
                    fase = Tools.remove_accents(fase)
                except:
                    fase = None
                try:
                    valor_causa = self.browser.find_element_by_xpath('//*[@id="includeContent"]/fieldset/'
                                                                     'table/tbody/tr[9]/td[2]').text.upper()
                    valor_causa = Tools.treat_value_cause(valor_causa)
                except:
                    valor_causa = None
                try:
                    dt_distribuicao = self.browser.find_element_by_xpath('//*[@id="includeContent"]/fieldset/'
                                                                         'table/tbody/tr[3]/td[2]').text.lower()
                    dt_distribuicao = Tools.remove_accents(dt_distribuicao)
                    dt_distribuicao = Tools.treat_date(dt_distribuicao)
                except:
                    dt_distribuicao = None

                print('\n----')
                print('dt_distribuicao', dt_distribuicao)
                print('valor_causa', valor_causa)
                print('fase', fase)
                print('classe', classe)
                print('assunto', assunto)
                print('status', status)
                print('juizo', juizo)
                print('\n----')

                # IDENTIFICA OS ENVOLVIDOS E RETORNA UMA LISTA COM AS PARTES E OS ADVOGADOS/JUIZ
                list_partes, list_advogs = self.envolvidos

                for i in list_partes: print(
                    " POLO:{} \t NOME:{} \t CPF_CNPJ:{}".format(i[-1], i[0].prt_nome, i[0].prt_cpf_cnpj))
                print('\n----')
                for i in list_advogs: print(
                    " POLO:{} \t NOME:{} \t TIPO:{}".format(i[-1], i[0].rsp_nome, i[0].rsp_tipo))
                print('\n----')

                # CRIA O OBJETO PROCESSO-PLATAFORMA QUE SERÁ INSERIDO NO BANCO DE DADOS
                process_platform = ProcessoPlataformaModel(plp_prc_id=prc_id, plp_plt_id=self.platform_id,
                                                           plp_numero=prc_numero, plp_status=status, plp_juizo=juizo,
                                                           plp_fase=fase, plp_valor_causa=valor_causa,
                                                           plp_classe=classe, plp_assunto=assunto,
                                                           plp_data_distribuicao=dt_distribuicao, plp_grau=2,
                                                           plp_segredo=False, plp_localizado=1)

                list_objects_process = [(process_platform, list_partes, list_advogs, list_aud,
                                         list_acp_pra, plp_id, [])]

                # INSERE A LISTA DE OBJETOS NO BANCO DE DADOS
                self.export_to_database(objects=list_objects_process, log=self.log_error, list_name_urls=list_name_urls,
                                        platform=self.platform_name, state=self.state, root=self)

                self.log_error.insert_info('Procedimento finalizado!')
            elif not err1:
                # CRIA O OBJETO PROCESSO-PLATAFORMA QUE SERÁ INSERIDO NO BANCO DE DADOS
                process_platform = ProcessoPlataformaModel(plp_prc_id=prc_id, plp_plt_id=self.platform_id,
                                                           plp_numero=prc_numero, plp_segredo=False,
                                                           plp_localizado=True)

                list_objects_process = [(process_platform, [], [], list_aud, list_acp_pra, plp_id, [])]

                # INSERE A LISTA DE OBJETOS NO BANCO DE DADOS
                self.export_to_database(objects=list_objects_process, log=self.log_error,
                                        list_name_urls=list_name_urls,
                                        platform=self.platform_name, state=self.state, root=self)

                self.log_error.insert_info('Procedimento finalizado!')
            else:  # SENÃO FAZ UMA NOVA BUSCA
                # LIMPA A PASTA PARA RECEBER OS NOVOS DOWNLOADS
                self.clear_path_download()

            print('###Tempo total da coleta de dados do processo: {} SECS'.format(time.time() - t0).upper())
            print('-' * 65)

        # VERIFICA SE O NAVEGADOR FECHOU, SENÃO O FECHA
        if self.browser is not None:
            self.browser.quit()

        # VERIFICA SE NÃO RETORNOU ALGUM PROCESSO DA BASE, SENÃO ATUALIZA A PLE_DATA
        # self.update_ple_data(ple_plt_id=self.platform_id, ple_uf=self.state)

        return i_n

    # BUSCA PROCESSO NO PROJUDI
    def find_process(self, prc_numero):

        try:
            if self.link_buscar_processo_2_grau is None:
                xphat_buscar_processo_2_grau='/html/body/div[9]/table/tbody/tr/td/table/tbody/tr[2]/td/a'
                wait = WebDriverWait(self.browser, 5)
                wait.until(EC.presence_of_element_located((
                    By.XPATH, xphat_buscar_processo_2_grau)))
                self.link_buscar_processo_1_grau=self.browser.find_element_by_xpath(xphat_buscar_processo_2_grau).get_attribute('href')
            self.browser.get(self.link_buscar_processo_2_grau)
            wait = WebDriverWait(self.browser, 5)
            wait.until(EC.presence_of_element_located((
                By.XPATH, xphat_buscar_processo_2_grau)))
            self.browser.find_element_by_xpath('//*[@id="numeroProcesso"]').send_keys(str(prc_numero))
            self.browser.find_element_by_xpath('//*[@id="pesquisar"]').click()
            self.browser.find_element_by_xpath(
                '//*[@id="buscaProcessosQualquerInstanciaForm"]/table[2]/tbody/tr/td[2]/a').click()
            return True
        except:
            try:
                self.browser.switch_to.default_content()
                self.browser.switch_to.frame(self.browser.find_element_by_css_selector("frame[name='mainFrame']"))
            except:
                pass

        return False


class projudiPara2GrauController(projudiParaController):
    def __init__(self, site, mode_execute, access, platform_id, platform_name, flag, num_thread):
        super().__init__(site=site, mode_execute=mode_execute, access=access, platform_id=platform_id,
                         platform_name=platform_name, flag=flag, num_thread=num_thread, grau='2Grau')

class projudiAmazonas2GrauController(projudiAmazonasController):
    def __init__(self, site, mode_execute, access, platform_id, platform_name, flag, num_thread):
        super().__init__(site=site, mode_execute=mode_execute, access=access, platform_id=platform_id,
                         platform_name=platform_name, flag=flag, num_thread=num_thread, grau='2Grau')

class projudiMaranhao2GrauController(projudiMaranhaoController):
    def __init__(self, site, mode_execute, access, platform_id, platform_name, flag, num_thread):
        super().__init__(site=site, mode_execute=mode_execute, access=access, platform_id=platform_id,
                         platform_name=platform_name, flag=flag, num_thread=num_thread, grau='2Grau')

