from pathlib import Path
import pytest


@pytest.fixture()
def lista_pdf_arquivos():
    devdata_pasta = Path(__file__).parent / "devdata"
    devdata_arquivos = devdata_pasta.glob("*.pdf")
    return list(devdata_arquivos)
