from datetime import date, datetime
import re
from typing import List, Optional
import pandas as pd
from pathlib import Path
from workalendar.america.brazil import BrazilBankCalendar

from case_loft.file import extrair_pdf_texto

REGEX_UNIT_ID = re.compile(
    r"(?P<unit_id>\d{6})(?=.*\n1\.)", flags=re.M | re.S | re.I)
REGEX_VALOR = re.compile(
    r"3\.1\. R\$ (?P<valor_total_da_venda>[\d.,]+).*?", flags=re.M | re.S | re.I)
REGEX_DIAS_ESCRITURA = re.compile(
    r"A Escritura deverá ser lavrada em até (?P<dias_de_escritura>\d+).*?", flags=re.M | re.S | re.I)
REGEX_DATA_ASSINATURA = re.compile(
    r"São Paulo, (?P<data_assinatura_do_contrato>\d{2}\/\d{2}\/\d{4})", flags=re.M | re.S | re.I)

CALENDARIO = BrazilBankCalendar()


def extrair_unit_id(texto: str) -> Optional[str]:
    unit_id = REGEX_UNIT_ID.search(texto)
    if unit_id:
        return unit_id.groupdict().get("unit_id")
    return None


def extrair_valor(texto: str) -> Optional[float]:
    valor = REGEX_VALOR.search(texto)
    if valor:
        valor = valor.groupdict().get("valor_total_da_venda")
        if valor is not None:
            if "," in valor:
                valor = valor.replace(".", "").replace(",", ".")
            return float(valor)
    return None


def extrair_data_escritura(texto: str, data_assinatura: date) -> Optional[date]:
    dias_escritura = REGEX_DIAS_ESCRITURA.search(texto)
    if dias_escritura:
        dias_escritura = dias_escritura.groupdict().get("dias_de_escritura")
        if dias_escritura is not None:
            return CALENDARIO.add_working_days(data_assinatura, int(dias_escritura))
    return None


def extrair_data_assinatura(texto: str) -> Optional[date]:
    data_assinatura = REGEX_DATA_ASSINATURA.search(texto)
    if data_assinatura:
        data_assinatura = data_assinatura.groupdict().get("data_assinatura_do_contrato")
        if data_assinatura is not None:
            return datetime.strptime(data_assinatura, "%d/%m/%Y").date()
    return None


def extrair_dados_arquivos(filepath_lista: List[Path]) -> pd.DataFrame:
    df = pd.DataFrame(columns=["unit_id", "valor",
                      "data_escritura", "data_assinatura"])

    for filepath in filepath_lista:
        texto = extrair_pdf_texto(filepath)
        data_assinatura = extrair_data_assinatura(texto)
        dados = {
            "unit_id": extrair_unit_id(texto),
            "valor": extrair_valor(texto),
            "data_escritura": extrair_data_escritura(texto, data_assinatura),
            "data_assinatura": data_assinatura
        }
        df = df.append(dados, ignore_index=True)
    return df
