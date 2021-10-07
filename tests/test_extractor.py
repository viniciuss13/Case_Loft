from pathlib import Path
from typing import List

from case_loft.file import extrair_pdf_texto
from case_loft import extractor
from datetime import date
from datetime import datetime
import pandas as pd


def test_extrair_unit_id(lista_pdf_arquivos: List[Path]):
    for arquivo in lista_pdf_arquivos:
        texto = extrair_pdf_texto(arquivo)
        unit_id = extractor.extrair_unit_id(texto)

        assert unit_id is not None, f"Não encontrado no arquivo: {arquivo}"
        assert isinstance(unit_id, str)


def test_extrair_data_escritura(lista_pdf_arquivos: List[Path]):
    data_assinatura = datetime.today().date()
    for arquivo in lista_pdf_arquivos:
        texto = extrair_pdf_texto(arquivo)
        data_escritura = extractor.extrair_data_escritura(
            texto, data_assinatura
        )

        assert data_escritura is not None, f"Não encontrado no arquivo: {arquivo}"
        assert isinstance(data_escritura, date)
        assert data_escritura > data_assinatura


def test_extrair_data_assinatura(lista_pdf_arquivos: List[Path]):
    for arquivo in lista_pdf_arquivos:
        texto = extrair_pdf_texto(arquivo)
        data_assinatura = extractor.extrair_data_assinatura(texto)

        assert data_assinatura is not None, f"Não encontrado no arquivo: {arquivo}"
        assert isinstance(data_assinatura, date)


def test_extrair_dados_arquivos(lista_pdf_arquivos: List[Path]):
    df = extractor.extrair_dados_arquivos(lista_pdf_arquivos)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == len(lista_pdf_arquivos)
    assert df.columns.tolist() == [
        "unit_id", "valor", "data_escritura", "data_assinatura"]
    assert df[df.isnull().any(1)].empty


def test_extrair_valor(lista_pdf_arquivos: List[Path]):
    for arquivo in lista_pdf_arquivos:
        texto = extrair_pdf_texto(arquivo)
        extrair_valor = extractor.extrair_valor(texto)

        assert extrair_valor is not None, f"Não encontrado no arquivo: {arquivo}"
        assert isinstance(extrair_valor, float)
