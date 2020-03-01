
from Controller.GlosaMax import GlosaMax

from Controller.BuscaZeroGlosa import ZeroGlosa

for i in ['glosamin', 'glosamax', 'pagatudo']:
    a = GlosaMax(True, i)
    a.donwload_arquivos(convenio=i)
    a.browser.quit()




