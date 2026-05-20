# Processo GED - Automação de Cadastro de Documentos

## Descrição

Projeto de automação desenvolvido em Python utilizando Selenium para realizar o cadastro automatizado de documentos no sistema GED.

A automação fazia:

* Acesso automático ao sistema web;
* Login utilizando credenciais;
* Captura e leitura de CAPTCHA com OCR;
* Consulta de dados em banco SQL Server;
* Preenchimento automático de formulários;
* Cadastro de processos/documentos no GED;
* Registro de logs da execução.

---

# Tecnologias Utilizadas

* Python
* Selenium
* ChromeDriver
* OpenCV
* Tesseract OCR
* PyODBC
* SQL Server
* WebDriver Manager

---

# Estrutura do Projeto

```bash
processo_ged/
│
├── automacao_web.py      # Fluxo principal da automação web
├── banco_dados.py        # Conexão e consultas ao banco SQL Server
├── captcha.py            # Tratamento e leitura de CAPTCHA
├── utilitarios.py        # Funções auxiliares e logging
├── main.py               # Arquivo principal de execução
├── captcha.png           # Captura original do CAPTCHA
├── captcha_tratado.png   # CAPTCHA tratado para OCR
├── retornos.log          # Logs da automação
```

---

# Funcionamento da Automação

## 1. Leitura de Dados

A automação inicia buscando registros pendentes no banco de dados SQL Server.

## 2. Acesso ao GED

O Selenium abre o navegador Google Chrome utilizando o ChromeDriver e acessa o sistema GED.

## 3. Leitura do CAPTCHA

O CAPTCHA da página é capturado por screenshot.

A imagem passa por tratamento utilizando OpenCV:

* Conversão para escala de cinza;
* Filtro bilateral;
* Threshold adaptativo;
* Remoção de ruídos.

Após o tratamento, o texto é lido utilizando Tesseract OCR.

## 4. Login Automático

Após a leitura do CAPTCHA, a automação realiza o login no sistema.

## 5. Cadastro do Documento

A automação:

* Navega até a tela de recebimento fiscal;
* Preenche campos do formulário;
* Seleciona fornecedor;
* Preenche dados bancários;
* Finaliza o cadastro do processo.

---

# Dependências

Instale as dependências utilizando:

```bash
pip install -r requirements.txt
```

Exemplo de bibliotecas utilizadas:

```txt
selenium
webdriver-manager
opencv-python
pytesseract
numpy
pyodbc
requests
```

---

# Como Executar

```bash
python main.py
```

---

# Observações

* O projeto foi desenvolvido para uso interno.
* Algumas informações sensíveis foram removidas/recomendadas para uso via variáveis de ambiente.
* O sistema automatizado depende da estrutura HTML original do GED.
* Alterações na interface do sistema podem quebrar a automação.

---

# Status do Projeto

Projeto pausado/descontinuado.

---

# Autor

Desenvolvido por Davi Alves.
