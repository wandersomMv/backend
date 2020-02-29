from Model.toolsModel import *
import logging

class LogErrorModelMutlThread:
    def __init__(self,  num_thread=None):
        self.num_tread = "" if num_thread is None else num_thread
        self.logger = logging.getLogger('tr{}'.format(num_thread))
        self.logger.setLevel(logging.INFO)
        self.Handler = None
        self.set_Handler()

    def insert_title(self, n_proc):

        self.logger.info('{}\n{}'.format('-' * 48, '#' * 76).upper())
        self.logger.info('Processo: {}'.format(n_proc).upper())

    def insert_log_erro(self, log):
        self.logger.error(log.upper())

    def insert_log_info(self, info):
        self.logger.info(info.upper())

    def set_Handler(self):

        directory = os.path.abspath('../Logs')
        Tools.new_path(directory)
        self.logger = logging.getLogger('tr_{}'.format(self.num_tread))
        self.logger.setLevel(logging.INFO)

        if self.Handler is not None:
            self.logger.handlers.clear()

        self.Handler = logging.FileHandler(directory + '/'  + '_logging_exec_{}.log'.format(self.num_tread),
                                           mode='a+')
        self.Handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'))
        self.logger.addHandler(self.Handler)
