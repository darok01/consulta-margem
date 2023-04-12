import os
import cv2
import pickle
import numpy as np
from keras.models import load_model
from convert_preto_e_branco import tratar_imagens
import glob
import sklearn


def quebrar_captcha():
    # Carregando o arquivo com os rótulos
    with open("IA/rotulos_modelo.dat", "rb") as tradutor:
        lb = pickle.load(tradutor)

    # Carregando o modelo treinado
    modelo = load_model("IA/modelo_treinado.hdf5")
    
    # Carregando as imagens
    tratar_imagens("ler", pasta_destino='ler')

    def resolver_captcha(pasta_origem, pasta_destino):
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        arquivos = glob.glob(f'{pasta_origem}/*.png')
        for arquivo in arquivos:
            imagem = cv2.imread(arquivo)

            # converter a imagem para escala de cinza
            imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

            # aplicar o método cv2.THRESH_BINARY para transformar a imagem em preto e branco
            _, nova_imagem = cv2.threshold(imagem_cinza, 0, 255, cv2.THRESH_BINARY_INV)

            # encontrar os contornos de cada letra ou número
            contornos, _ = cv2.findContours(nova_imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            regiao_letras = []
            
            # filtrar os contornos que são realmente de letras ou números
            for contorno in contornos:
                (x, y, largura, altura) = cv2.boundingRect(contorno)
                area = cv2.contourArea(contorno)
                if area > 200:
                    regiao_letras.append((x, y, largura, altura))
            regiao_letras = sorted(regiao_letras, key=lambda x: x[0])

            # desenhar os contornos e separar as letras em arquivos individuais
            imagem_final = cv2.merge([imagem] * 3)
            previsao = []
            
            for retangulo in regiao_letras:
                x, y, largura, altura = retangulo
                imagem_letra = imagem_cinza[y:y+altura, x:x+largura]

                # pular letras ou números muito pequenos
                if imagem_letra.shape[0] < 10 or imagem_letra.shape[1] < 10:
                    continue
                # ajusta o tamanho da imagem para 20x20 pixels
                imagem_letra = cv2.resize(imagem_letra, (20, 20))
                imagem_letra =  np.expand_dims(imagem_letra, axis=2)
                imagem_letra = np.expand_dims(imagem_letra, axis=0)

                letra_prevista = modelo.predict(imagem_letra, verbose=0)
                letra_prevista = lb.inverse_transform(letra_prevista)[0]
                previsao.append(letra_prevista)

            texto_previsao = "".join(previsao)
            
            return texto_previsao
            
    return resolver_captcha("ler", "ler")


if __name__ == "__main__":
    quebrar_captcha()
