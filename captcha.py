import cv2
import pytesseract
import logging
import numpy as np


def tratar_captcha_e_salvar(caminho_original="captcha.png", caminho_saida="captcha_tratado.png"):
    try:
        imagem = cv2.imread(caminho_original)

        if imagem is None:
            logging.error("Imagem do captcha não encontrada.")
            return ""

        cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        cinza = cv2.bilateralFilter(cinza, 11, 17, 17)
        binario = cv2.adaptiveThreshold(
            cinza,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )
        kernel = np.ones((2, 2), np.uint8)
        binario = cv2.morphologyEx(binario, cv2.MORPH_OPEN, kernel)
        cv2.imwrite(caminho_saida, binario)

        logging.info("Captcha tratado e salvo com sucesso.")

        config = "--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

        texto = pytesseract.image_to_string(binario, config=config)

        return texto.strip()

    except Exception as e:
        logging.error(f"Erro ao tratar captcha: {e}")
        return ""
