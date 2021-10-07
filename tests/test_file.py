from pathlib import Path
from typing import List

from case_loft.file import extrair_pdf_texto


def test_extrair_pdf_texto(lista_pdf_arquivos: List[Path]):
    for arquivo in lista_pdf_arquivos:
        texto = extrair_pdf_texto(arquivo)

        assert isinstance(texto, str)
        assert len(texto) > 0
