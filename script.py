import os
import string
import shutil
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
import smtplib
from email.message import EmailMessage

# Carrega variáveis do .env
load_dotenv()

EBOOK_CONVERT = os.getenv("EBOOK_CONVERT_PATH")
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")
SMTP_SERVIDOR = os.getenv("SMTP_SERVIDOR")
SMTP_PORTA = int(os.getenv("SMTP_PORTA"))

def encontrar_kindle():
    for letra in string.ascii_uppercase:
        caminho = f"{letra}:\\documents"
        if os.path.isdir(caminho):
            return caminho
    return None

def enviar_usb(arquivo):
    kindle_path = encontrar_kindle()
    if kindle_path:
        try:
            shutil.copy2(arquivo, kindle_path)
            print("✅ Arquivo enviado com sucesso para o Kindle via USB!")
        except Exception as e:
            print(f"❌ Erro ao enviar para o Kindle: {e}")
    else:
        print("❌ Kindle não detectado via USB.")

def enviar_email(arquivo):
    if not arquivo.endswith(".epub"):
        print("❌ Apenas arquivos .epub podem ser enviados por e-mail para o Kindle.")
        return

    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_REMETENTE
        msg["To"] = EMAIL_DESTINO
        msg["Subject"] = "Envio para Kindle"
        msg.set_content("Segue em anexo o livro para leitura.")

        with open(arquivo, "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="epub+zip", filename=os.path.basename(arquivo))

        with smtplib.SMTP(SMTP_SERVIDOR, SMTP_PORTA) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_REMETENTE, EMAIL_SENHA)
            smtp.send_message(msg)

        print("✅ Arquivo enviado com sucesso para o Kindle via e-mail!")

    except Exception as e:
        print(f"❌ Falha ao enviar e-mail: {e}")

def converter_pdf(pdf, capa, titulo, autor, formato, pasta_saida):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    nome_saida = f"{titulo}.{formato}"
    caminho_saida = os.path.join(pasta_saida, nome_saida)

    comando = [
        EBOOK_CONVERT,
        pdf,
        caminho_saida,
        '--cover', capa,
        '--title', titulo,
        '--authors', autor
    ]

    print("\n🔄 Convertendo...")
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True)
        if resultado.returncode != 0:
            print(f"❌ Erro na conversão:\n{resultado.stderr}")
            return None

        print(f"✅ Conversão concluída: {caminho_saida}")
        with open("log_conversao.txt", "a", encoding="utf-8") as log:
            log.write(f"[{datetime.now()}] {titulo} de {autor} salvo em: {caminho_saida}\n")
        return caminho_saida
    except FileNotFoundError:
        print("❌ Caminho para ebook-convert não encontrado. Verifique o .env.")
        return None

def input_completado(msg):
    return prompt(msg, completer=PathCompleter()).strip()

def menu():
    print("""
=== Conversor Kindle Multifuncional ===
1. Converter PDF para AZW3 ou EPUB
2. Enviar arquivos para Kindle via USB
3. Enviar arquivos EPUB para Kindle via e-mail
0. Sair
""")
    return prompt("Escolha uma opção: ").strip()

def opcao_converter():
    qtd = int(prompt("📚 Quantos livros deseja converter? "))
    pasta = input_completado("📁 Pasta de saída: ") or "Livros_Convertidos"
    formato = prompt("📦 Formato desejado (azw3/epub): ").strip().lower()

    for i in range(1, qtd + 1):
        print(f"\n=== Livro {i} de {qtd} ===")
        pdf = input_completado("📄 PDF de entrada: ")
        capa = input_completado("🖼️  Capa (jpg/png): ")
        titulo = prompt("📘 Título: ").strip()
        autor = prompt("✍️  Autor: ").strip()

        converter_pdf(pdf, capa, titulo, autor, formato, pasta)

def opcao_usb():
    qtd = int(prompt("📤 Quantos arquivos deseja enviar ao Kindle via USB? "))
    for i in range(1, qtd + 1):
        caminho = input_completado(f"📄 Caminho do arquivo {i}: ")
        enviar_usb(caminho)

def opcao_email():
    qtd = int(prompt("📧 Quantos arquivos EPUB deseja enviar por e-mail ao Kindle? "))
    for i in range(1, qtd + 1):
        caminho = input_completado(f"📄 Caminho do arquivo .epub {i}: ")
        enviar_email(caminho)

def main():
    while True:
        opcao = menu()
        if opcao == '1':
            opcao_converter()
        elif opcao == '2':
            opcao_usb()
        elif opcao == '3':
            opcao_email()
        elif opcao == '0':
            print("👋 Encerrando.")
            break
        else:
            print("❌ Opção inválida.")

if __name__ == "__main__":
    main()
