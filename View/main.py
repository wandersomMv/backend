
from Controller.GlosaMax import GlosaMax
a = GlosaMax('https://glosamax.zeroglosa.com.br', True,'glosamin')
a.donwload_arquivos(convenio='glosamin')

# 'https://glosamax.zeroglosa.com.br/glosamax/arquivo/download?nome=glosamax_2018-02-15.xml&data=2018-02-15'
# 'href="../arquivo/download?nome=glosamax_2018-02-15.xml&data=2018-02-15"'