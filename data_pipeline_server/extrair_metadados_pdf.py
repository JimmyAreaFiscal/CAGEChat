import os
import json
from PyPDF2 import PdfReader

# Caminhos das pastas com PDFs
pdf_dirs = [
    "arquivos/manuais",
    "arquivos/instrucoes_normativas"
]

# Função para extrair texto da primeira página do PDF
def extract_first_page_text(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        if reader.pages:
            return reader.pages[0].extract_text() or ""
        return ""
    except Exception as e:
        print(f"Erro ao ler {pdf_path}: {e}")
        return ""

# Função para tentar extrair informações do texto
def extract_metadata_from_text(text):
    # Aqui você pode melhorar as heurísticas conforme o padrão dos seus documentos
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    metadata = {
        "file_name": lines[0] if lines else "",
        "tipo_documento": "",
        "assunto": "",
        "edição": "",
        "ano_publicação": "",
    }
    # Tentativas básicas de extração
    for line in lines:
        if "edição" in line.lower():
            metadata["edição"] = ''.join(filter(str.isdigit, line))
        if "ano" in line.lower() or "publicação" in line.lower():
            for word in line.split():
                if word.isdigit() and len(word) == 4:
                    metadata["ano_publicação"] = word
        if "manual" in line.lower():
            metadata["tipo_documento"] = "manual"
        elif "guia" in line.lower():
            metadata["tipo_documento"] = "guia"
        elif "instrução normativa" in line.lower():
            metadata["tipo_documento"] = "instrução normativa"
        # Adicione mais regras conforme necessário
    return metadata

# Lista para armazenar os metadados
metadados = []

for pdf_dir in pdf_dirs:
    for file in os.listdir(pdf_dir):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, file)
            text = extract_first_page_text(pdf_path)
            meta = extract_metadata_from_text(text)
            meta["file_path"] = os.path.relpath(pdf_path, "upload_docs")
            metadados.append(meta)

# Salvar resultado em JSON
with open("metadados_extraidos.json", "w", encoding="utf-8") as f:
    json.dump(metadados, f, ensure_ascii=False, indent=4)

print("Extração concluída! Veja o arquivo metadados_extraidos.json.")