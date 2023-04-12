import cv2
import os
import glob
import sklearn


def tratar_imagens(pasta_origem, pasta_destino='images'):
    # lista todos os arquivos da pasta_origem que possuem extensão .png
    arquivos = glob.glob(f"{pasta_origem}/*.png")
    
    for arquivo in arquivos:
        # leia a imagem
        imagem = cv2.imread(arquivo)
        
        # aplique o método cv2.THRESH_BINARY
        _, imagem_tratada = cv2.threshold(imagem, 127, 255, cv2.THRESH_BINARY)
        
        # obtenha o nome do arquivo (sem o caminho) e salve a imagem tratada na pasta_destino
        nome_arquivo = os.path.basename(arquivo)
        cv2.imwrite(f"{pasta_destino}/{nome_arquivo}", imagem_tratada)

if __name__ == "__main__":
    tratar_imagens('images')
