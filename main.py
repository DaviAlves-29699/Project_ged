import logging
from automacao_web import CadastroDeDados
from banco_dados import leitura_tabela

# Configuração do log
logging.basicConfig(
    filename="retornos.log",
    level=logging.INFO,
    format="%(asctime)s :: %(levelname)s :: %(filename)s :: %(lineno)d :: %(message)s"
)

# Busca um registro no banco
linha = leitura_tabela()

if not linha:
    print("Nenhum registro encontrado para processamento.")
else:
    print("Registro encontrado:", linha)

    # Inicia a automação
    bot = CadastroDeDados()
    bot.linha = linha
    bot.cadastro_web()
