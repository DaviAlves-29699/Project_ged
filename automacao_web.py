from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import logging
import requests
from captcha import tratar_captcha_e_salvar

class CadastroDeDados:
    def __init__(self):
        self.navegador = None
        self.date = None
        self.linha = None

    def cadastro_web(self):
        try:
            print("Iniciando cadastro no Ged")

            link = 'http://ged.inec.org.br:8181/index.jsp'
            site = requests.get(url=link)

            if site.status_code == 200:
                logging.info('Site On')
            else:
                logging.error('Site Off')
                return

            servico = Service(ChromeDriverManager().install())
            self.navegador = webdriver.Chrome(service=servico)
            self.navegador.maximize_window()
            self.navegador.get(url=link)

            self.date = datetime.now().strftime("%d/%m/%Y")

            # localiza o captcha na tela
            captcha_element = WebDriverWait(self.navegador, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/form/img")))

            # faz uma captura da tela no captcha
            captcha_element.screenshot("captcha.png")

            texto_captcha = tratar_captcha_e_salvar("captcha.png","captcha_tratado.png")

            logging.info(f'Captcha OCR: "{texto_captcha}"')

            if not texto_captcha:
                logging.error("Captcha vazio")
                self.navegador.close()
                return

            self.autenticacao_user(texto_captcha)

        except Exception as e:
            logging.error(f"Erro no cadastro_web: {e}")
            self.navegador.quit()

    def autenticacao_user(self, codigo_captcha):
        try:
            wait = WebDriverWait(self.navegador, 30)
            # credenciais de acesso
            Email = 'davi.rodrigues@inec.org.br'
            Key = 'Sk84ever*@'
            # espera os inputs da página carregarem para colocar os acessos.
            wait.until(EC.element_to_be_clickable((By.ID, "email"))).send_keys(Email)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmLogin"]/input[2]'))).send_keys(Key)

            capt = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/input[3]')))
            capt.send_keys(codigo_captcha + Keys.RETURN)

            logging.info('Login realizado')
            self.cadastro_ged()

        except Exception as e:
            logging.error(f'Erro no login: {e}')
            self.navegador.quit()

    def cadastro_ged(self):
        try:
            wait = WebDriverWait(self.navegador, 40)

            # Acessa a Tela de Recebimento Fiscal
            recebimento_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[1]/a[4]/div")))
            self.navegador.execute_script("arguments[0].click();", recebimento_btn)

            # Seleciona o Documento/Processo
            select_element = wait.until(EC.visibility_of_element_located((By.ID, "fluxoAssuntoList")))
            self.navegador.execute_script("arguments[0].removeAttribute('disabled');", select_element)

            select = Select(select_element)
            select.select_by_value("218")

            # Campo Número de Documento
            campo_doc = wait.until(EC.element_to_be_clickable((By.ID, "processoCheckAjax")))

            campo_doc.clear()
            campo_doc.send_keys(str(self.linha[25]) + " " + str(self.linha[1]))

            # Coloca a Data de recebimento
            data_rece = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/form/div[4]/div[1]/input')))
            data_rece.send_keys(str(self.date))
            
            # Coloca a Data de Emissão
            data_emi = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/form/div[4]/div[2]/input')))
            data_emi.send_keys(str(self.linha[14]))

            # Coloca a Data de Vencimento
            data_venc = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/form/div[4]/div[3]/input')))
            data_venc.send_keys(str(self.linha[15]))

            # Escolhe a Fonte de Recurso
            font_rec = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/form/div[7]/div[2]/select/option[" + str(self.linha[27]) + "]")))
            font_rec.click()
            
            # Termo de Parceria
            botao_parc = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/form/div[7]/div[" + str(self.linha[28]) + "]/select/option[2]")))
            botao_parc.click()

            # Coloca o Valor
            campo_valor = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/form/div[8]/div/input')))
            campo_valor.send_keys(str(self.linha[18]))

            avancar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/form/div[9]/div/a')))
            self.navegador.execute_script("arguments[0].click();", avancar_btn)

            # Campo de Dados de Fornecedor
            cnpj_input = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div[1]/div/input')))
            cnpj_input.send_keys(self.linha[3])

            # seleciona o fornecedor no campo de consulta
            sele_icon = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[2]/div[2]/table/tbody/tr/td[3]/i')))
            self.navegador.execute_script("arguments[0].click();", sele_icon)
            
            logging.info('Fornecedor selecionado')
            self.dados_forn()

        except Exception as e:
            logging.error(f'Erro no cadastro GED: {e}')
            self.navegador.quit()
      
    def dados_forn(self):
        try:
            wait = WebDriverWait(self.navegador, 40)

            # Dados de Pagamento (SELECT)
            select_pagina = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/form/div[12]/div/select')))
            Select(select_pagina).select_by_index(1)

            # Preenche Dados Bancários
            self.preencher_dados_bancarios()

            # Área de texto
            texto_area = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/form/div[16]/div/textarea')))

            texto_area.clear()
            texto_area.send_keys(f'Fatura de energia do posto {self.linha[4]} com vencimento em {self.linha[15]}')

            # Botão Cadastrar Documento
            botao_cadastrar = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/form/div[17]/button')))
            self.navegador.execute_script("arguments[0].click();", botao_cadastrar)

            # Botão Confirmar
            botao_confirm = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/form/div[18]/div/div/div[3]/button')))
            self.navegador.execute_script("arguments[0].click();", botao_confirm)

            logging.info('Processo cadastrado com sucesso')

        except Exception as e:
            logging.error(f'Erro ao finalizar processo: {e}')
            self.navegador.quit()


    def preencher_dados_bancarios(self):
        try:
            wait = WebDriverWait(self.navegador, 30)

            # CPF / CNPJ
            cnpj = wait.until(EC.element_to_be_clickable((By.ID, "cnpjCpfFavorecido")))
            self.navegador.execute_script("arguments[0].scrollIntoView(true);", cnpj)
            cnpj.clear()
            cnpj.send_keys(self.linha[3])

            # Favorecido
            favorecido = wait.until(EC.element_to_be_clickable((By.ID, "favorecido")))
            favorecido.clear()
            favorecido.send_keys(self.linha[4])

            # Banco
            banco = wait.until(EC.element_to_be_clickable((By.ID, "banco")))
            banco.clear()
            banco.send_keys(self.linha[6])

            # Agência
            agencia = wait.until(EC.element_to_be_clickable((By.ID, "agencia")))
            agencia.clear()
            agencia.send_keys(self.linha[7])

            # Conta
            conta = wait.until(EC.element_to_be_clickable((By.ID, "conta")))
            conta.clear()
            conta.send_keys(self.linha[8])

            # Tipo de Conta
            tipo_conta = wait.until(EC.element_to_be_clickable((By.ID, "tipoConta")))
            Select(tipo_conta).select_by_value("CORRENTE")

            logging.info("Dados bancários preenchidos com sucesso")

        except Exception as e:
            logging.error(f"Erro ao preencher dados bancários: {e}")
            self.navegador.quit()