class GuiaModel:
    def __init__(self,  guia_numero = None,
                        guia_prest_id = None,
                        guia_valor_total = None,
                        guia_conv_id = None,
                        guia_beneficiario_id = None,
                        guia_data_cadastro = None,
                        guia_data_pagamento = None,
                        guia_valor_pago = None
                        ):
            self.guia_numero = guia_numero
            self.guia_prest_id = guia_prest_id
            self.guia_valor_total = guia_valor_total
            self.guia_conv_id = guia_conv_id
            self.guia_beneficiario_id = guia_beneficiario_id
            self.guia_data_cadastro = guia_data_cadastro
            self.guia_data_pagamento = guia_data_pagamento
            self.guia_valor_pago = guia_valor_pago