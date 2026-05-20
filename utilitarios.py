import logging

def configurar_logging(arquivo_log="retornos.log"):
    logging.basicConfig(
        filename=arquivo_log,
        level=logging.INFO,
        format="%(asctime)s :: %(levelname)s :: %(filename)s :: %(lineno)d :: %(message)s"
    )

def mensagem_erro_padrao(erro, contexto=""):
    logging.error(f"Erro no contexto '{contexto}': {erro}")

def formatar_data_para_banco(data_string):
    return data_string.strip()





