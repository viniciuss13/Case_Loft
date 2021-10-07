from argparse import ArgumentParser
from case_loft import extractor
import logging
from pathlib import Path

if __name__ == "__main__":


    parser = ArgumentParser('Aceitar argumento de entrada da pasta com os arquivos e caminho do arquivo de saída, dica abaixo')
    parser.add_argument('-i', '--input', help='Caminho da pasta de entrada', type=str)
    parser.add_argument('-o', '--output', help='Caminho de saida do arquivo', type=str)
    argumentos = parser.parse_args()


    arquivos = list(Path(argumentos.input).glob("*.pdf"))
    dataframe = extractor.extrair_dados_arquivos(arquivos)
    dataframe.to_excel(argumentos.output,index=False)
