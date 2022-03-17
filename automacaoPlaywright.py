# importando modo síncrono
import time

from playwright.sync_api import sync_playwright

from unzipFile import descompacta

url = "http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/mercado-a-vista/opcoes/series-autorizadas/" # noQa E501
navegadorOculto = True

print("\n\n\n\n\n\n\n\n####################################################################\nPrograma iniciado") # noQaE501
with sync_playwright() as p:
    carregamento_inicio = time.time()  # datetime.now().strftime('%Y-%m-%d %H:%M:%S') # noQa E501
    # por padrão ele abre o chrome de forma invisível
    # browser = p.chromium.launch()
    # headless=False abre browser
    browser = p.chromium.launch(headless=navegadorOculto)
    page = browser.new_page()
    # timeout default 30000 aumentado devido a demora site da B3
    print("Iniciado o carregamento de URL\nAguarde no máximo 1 minuto")
    page.goto(url, timeout=60000)
    # page.fill("input[name='q']",'paçoca')
    # page.click("input[name='btnK']")
    carregamento_fim = time.time()  # datetime.now().strftime('%Y-%m-%d %H:%M:%S') # noQa E501
    xpath_botao_download = '//*[@id="conteudo-principal"]/div[4]/div/div/div[3]/div[3]/div[1]/div[1]/div[2]/p/a' # noQa E501
    # Start waiting for the download
    print("Iniciado download de arquivo")
    with page.expect_download() as download_info:
        page.locator(xpath_botao_download).click()
    download = download_info.value
    filename = download.suggested_filename
    download.save_as("./temp/" + filename)
    print("\n\ndownloaded file: ", str(download.suggested_filename))

    browser.close()
    print("Inicio do carregamento", carregamento_inicio)
    print("Fim do carregamento", carregamento_fim)
    # print("datetime.strptime(carregamento_fim, '%M%S')", datetime.strptime(str(carregamento_fim), "%S")) # noQa E501

    carregamento_duracao = carregamento_fim - carregamento_inicio # noQa E501
    print("Tempo de carregamento", str(carregamento_duracao))

    tmp_folder = "./temp/"
    descompacta(tmp_folder, "SI_D_SEDE.zip")

#                       Fim do donload






print("Programa finalizado com sucesso\n#######\n######\n#####\n####\n###\n##\n#") # noQa E501
