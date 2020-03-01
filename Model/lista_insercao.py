class lista_insercao:
    def __init__(self,
                 convenio='',
                 data_pagamento='',
                 numero_protocolo='',
                 matricula='',
                 nome='',
                 numero_guia='',
                 ng_prest='',
                 senha_guia='',
                 codigo_produto='',
                 descricao_produto='',
                 valor_apresentado='',
                 valor_pago='',
                 valor_glosa='',
                 descricao_motivo='',
                 codigo_motivo='',
                 status = ''
                 ):
        self.convenio = convenio
        self.data_pagamento = data_pagamento
        self.numero_protocolo = numero_protocolo
        self.matricula = matricula
        self.nome = nome
        self.numero_guia = numero_guia
        self.ng_prest = ng_prest
        self.senha_guia = senha_guia
        self.codigo_produto = codigo_produto
        self.descricao_produto = descricao_produto
        self.valor_apresentado = valor_apresentado
        self.valor_pago = valor_pago
        self.valor_glosa = valor_glosa
        self.descricao_motivo = descricao_motivo
        self.codigo_motivo = codigo_motivo
        self.status = status