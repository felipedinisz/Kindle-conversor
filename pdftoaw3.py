import os
import string
import shutil
import subprocess
from datetime import datetime

from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter

# Ajuste esse caminho para o seu calibre
ebook_convert = r"C:\Program Files\Calibre2\ebook-convert.exe"

def encontrar_kindle():
    for letra in string.ascii_uppercase:
        caminho = f"{letra}:\\documents"
        if os.path.isdir(caminho):
            return caminho
    return None

def enviar_para_kindle(caminho_arquivo_azw3):
    caminho_kindle = encontrar_kindle()
    if caminho_kindle:
        resposta = prompt(f"\nKindle detectado em {caminho_kindle}. Deseja enviar o arquivo para o Kindle? (s/n): ").strip().lower()
        if resposta == 's':
            try:
                shutil.copy2(caminho_arquivo_azw3, caminho_kindle)
                print("Arquivo enviado com sucesso!")
            except Exception as e:
                print(f"Erro ao enviar arquivo: {e}")
        else:
            print("Arquivo não foi enviado.")
    else:
        print("\nKindle não foi detectado com letra de unidade.")
        print(f"O arquivo foi salvo em: {caminho_arquivo_azw3}")

def converter_pdf_para_azw3(pdf_path, capa_path, titulo, autor, pasta_saida):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    nome_arquivo_azw3 = f"{titulo}.azw3"
    caminho_arquivo_azw3 = os.path.join(pasta_saida, nome_arquivo_azw3)

    comando = [
        ebook_convert,
        pdf_path,
        caminho_arquivo_azw3,
        '--cover', capa_path,
        '--title', titulo,
        '--authors', autor
    ]

    print("\n🔄 Convertendo...")
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True)
        if resultado.returncode != 0:
            print(f"❌ Erro na conversão:\n{resultado.stderr}")
            return None
        else:
            print(f"✅ Conversão concluída: {caminho_arquivo_azw3}")

            with open("log_conversao.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"[{datetime.now()}] \"{titulo}\" de {autor} salvo em: {caminho_arquivo_azw3}\n")

            return caminho_arquivo_azw3

    except FileNotFoundError:
        print("❌ Executável do calibre não encontrado. Verifique o caminho.")
        return None

def input_completado(msg):
    return prompt(msg, completer=PathCompleter())

def main():
    print("=== Conversor PDF para AZW3 com capa personalizada ===\n")
    qtd_livros = int(prompt("📚 Quantos livros deseja converter? "))
    pasta_saida = input_completado("📁 Pasta de saída: ").strip()
    if not pasta_saida:
        pasta_saida = "Livros_AZW3"

    for i in range(1, qtd_livros + 1):
        print(f"\n=== Livro {i} de {qtd_livros} ===")
        pdf_path = input_completado("📄 Caminho do PDF: ").strip()
        capa_path = input_completado("🖼️  Caminho da capa (JPG/PNG): ").strip()
        titulo = prompt("📘 Título do livro (define o nome do AZW3): ").strip()
        autor = prompt("✍️  Autor do livro: ").strip()

        arquivo_azw3 = converter_pdf_para_azw3(pdf_path, capa_path, titulo, autor, pasta_saida)
        if arquivo_azw3:
            enviar_para_kindle(arquivo_azw3)

    print("\n📓 Todas as conversões foram registradas em: log_conversao.txt")

if __name__ == "__main__":
    main()
