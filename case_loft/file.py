import re
import fitz
from pathlib import Path


# Abri e lê o pdf
def extrair_pdf_texto(filepath: Path) -> str:
    """Using PyMuPDF do extract PDF text - https://pypi.org/project/PyMuPDF/
    Arguments:
        filepath {str} -- document path 
    """

    texto_completo = ""
    with fitz.open(filepath.absolute().as_posix()) as doc:
        for page in doc:
            texto = page.get_text()
            texto_completo += " " + texto
    texto_completo = re.sub(r" {2,}", " ", texto_completo).strip()
    return texto_completo
