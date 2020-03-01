class dados:
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
                 codigo_motivo=''
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




class guia:
    def __init__(self,
         numeroGuia='',
         nomeOperadora='',
         nome_prestador='',
         cnpj='',
         nome_Beneficiario='',
         matricula='',
         dataAtendimento='',
         valorTotalGuia='',
    ):
        self.numeroGuia = numeroGuia
        self.nomeOperadora = nomeOperadora
        self.nome_prestador = nome_prestador
        self.cnpj = cnpj
        self.nome_Beneficiario = nome_Beneficiario
        self.matricula = matricula
        self.dataAtendimento = dataAtendimento
        self.valorTotalGuia = valorTotalGuia
        self.lista_itens_da_guia = []


class dados_item:
    def __init__(self,
         numeroItem='',
         codigo='',
         nome_item='',
         valorUnitario='',
         quantidade='',
         valorTotal=''
    ):
        self.numeroItem = numeroItem
        self.codigo = codigo
        self.nome_item = nome_item
        self.valorUnitario = valorUnitario
        self.quantidade = quantidade
        self.valorTotal = valorTotal
