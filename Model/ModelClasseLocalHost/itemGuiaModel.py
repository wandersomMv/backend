class ItemGuiaModel:
    def __init__(self, itmg_quantidade = 0,
                    itmg_prdt_id = None,
                    itmg_valor_total = None,
                    itmg_numero = None,
                    itmg_valor_pago = None,
                    itmg_valor_glosa = None
                    itmg_motivo_glosa_descricao = None,
                    itmg_motivo_glosa_codigo = None,
                    itmg_status = None
                 ):
        self.itmg_quantidade = 0,
        self.itmg_prdt_id = itmg_prdt_id,
        self.itmg_valor_total = itmg_valor_total,
        self.itmg_numero = itmg_numero,
        self.itmg_valor_pago = itmg_valor_pago,
        self.itmg_motivo_glosa_descricao = itmg_motivo_glosa_descricao,
        self.itmg_motivo_glosa_codigo = itmg_motivo_glosa_codigo,
        self.itmg_valor_glosa = itmg_valor_glosa
        self.itmg_status = itmg_status