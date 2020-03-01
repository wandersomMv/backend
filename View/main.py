
from Controller.GlosaMax import GlosaMax

from Controller.BuscaZeroGlosa import ZeroGlosa
a = ZeroGlosa('', True,"teste")
a.donwload_planilhas_xml_orm('42852','1179648',4)


#42852,655360 ->> Gosa_MAX

#42852,1179648 -> Paga Tudo

#42852, 2 -> Glosa_min





# a = GlosaMax('https://glosamax.zeroglosa.com.br', True,'glosamin')
# a.donwload_arquivos(convenio='glosamin')

# 'https://glosamax.zeroglosa.com.br/glosamax/arquivo/download?nome=glosamax_2018-02-15.xml&data=2018-02-15'
# 'href="../arquivo/download?nome=glosamax_2018-02-15.xml&data=2018-02-15"'

