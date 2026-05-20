import pyodbc
import logging
from time import sleep

def conectar_bd():
    server = 'tcp:192.168.20.8'
    database = 'dbintegra'
    username = 'usr_rpa'
    password = 'Do^sqEEfQUTQOPmi'

    try:
        cnxn = pyodbc.connect('DRIVER={SQL SERVER Native Client 11.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
        logging.info('Conexão com o banco de dados realizada')
        return cnxn
    except Exception as ex:
        logging.error(f'Erro de conexão com o banco: {ex}')
        sleep(60)
        return None

def leitura_tabela():
    cnxn = conectar_bd()
    if not cnxn:
        return None
    cursor = cnxn.cursor()
    cursor.execute("SELECT numero_cliente, competencia, cnpj_inec, cnpj_fornecedor, localidade, filial, servico, projeto, fase, conta_financeira, conta_contabil, centro_custo, desc_centro_custo, tipo_titulo, data_emissao, data_vencimento, multa, juros, valor, codigo_barras, situacao_fatura, situacao_erp, situacao_ged, id_ged, nota_fiscal, tipo_titulo+'_'+localidade+'_'+CONVERT(varchar,numero_cliente)+'_'+competencia AS num_documento ,CASE WHEN centro_custo LIKE 'A%' THEN 3 WHEN centro_custo LIKE 'C%' THEN 4 ELSE '' END AS doc_processo ,CASE WHEN centro_custo LIKE 'A%' THEN 2 WHEN centro_custo LIKE 'C%' THEN 3 ELSE '' END AS fon_recurso ,CASE WHEN centro_custo LIKE 'A%' THEN 4 WHEN centro_custo LIKE 'C%' THEN 5 ELSE '' END AS ter_parceria ,datsit_ged ,id FROM dbintegra.dbo.tb_rpa_conta WHERE situacao_fatura = 1 AND situacao_ged = 0 ORDER BY data_vencimento")
    linha = cursor.fetchone()
    return linha

def update_no_bd(nu_id, datsit_ged):
    try:
        cnxn = conectar_bd()
        if not cnxn:
            return False

        cursor = cnxn.cursor()

        sql = """
            UPDATE dbintegra.dbo.tb_rpa_conta
            SET situacao_ged = 1,
                datsit_ged = ?
            WHERE id = ?
        """

        cursor.execute(sql, (datsit_ged, nu_id))
        cnxn.commit()

        logging.info(f'Registro atualizado com sucesso no banco: ID {nu_id}')
        return True

    except Exception as e:
        logging.error(f'Erro ao atualizar registro no banco: {e}')
        return False
