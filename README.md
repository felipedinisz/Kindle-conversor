# 📚 Conversor de Livros para Kindle (PDF → EPUB/AZW3)

Este projeto é um utilitário de linha de comando (CLI) em Python que permite converter arquivos PDF para os formatos **EPUB** (recomendado para envio por e-mail ao Kindle) ou **AZW3** (ideal para uso local ou envio por USB). Ele também permite o envio direto dos arquivos convertidos para o Kindle via **USB** ou **e-mail**, de acordo com os padrões da Amazon.

## ✨ Funcionalidades

- Conversão de arquivos PDF para **EPUB** ou **AZW3**, com capa, título e autor personalizados.
- Envio automático para o Kindle via **conexão USB** (qualquer formato).
- Envio automático para o Kindle via **e-mail** (formato EPUB apenas).
- Interface interativa e completadores de caminho via terminal.
- Registro automático de conversões no `log_conversao.txt`.

---

## 🧰 Pré-requisitos

- Python 3.10 ou superior.
- [Calibre](https://calibre-ebook.com/download) instalado (para usar o `ebook-convert`).
- Conta Amazon com endereço Kindle configurado e autorizado a receber e-mails.
- Acesso ao seu e-mail com senha de app (Gmail, Outlook, etc.).

---

## 🔧 Instalação

1. Clone este repositório:

```bash
git clone https://github.com/seunome/conversor-kindle.git
cd conversor-kindle
```

2. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuração do `.env`

Crie um arquivo `.env` na raiz com as seguintes variáveis:

```env
EBOOK_CONVERT_PATH=C:\Program Files\Calibre2\ebook-convert.exe
EMAIL_REMETENTE=seuemail@gmail.com
EMAIL_SENHA=sua_senha_de_app
EMAIL_DESTINO=seudestino@kindle.com
SMTP_SERVIDOR=smtp.gmail.com
SMTP_PORTA=587
```

> ⚠️ Use [senhas de app](https://support.google.com/mail/answer/185833?hl=pt-BR) se estiver usando Gmail com autenticação de dois fatores. A senha comum **não funcionará**.

---

## 🚀 Uso

Execute o script principal:

```bash
python script.py
```

Você verá um menu com três opções:

### 1. 📘 Converter PDF para EPUB ou AZW3

Você poderá inserir os dados do livro (PDF, capa, título, autor), escolher o formato de saída e salvá-lo em uma pasta definida. Não é necessário conectar o Kindle nesta etapa.

### 2. 📤 Enviar arquivos para o Kindle via USB

Se o Kindle estiver conectado como unidade USB, o script detecta automaticamente e permite o envio dos arquivos **AZW3, EPUB, MOBI ou PDF** diretamente.

### 3. ✉️ Enviar arquivos EPUB para o Kindle via e-mail

O script enviará os arquivos para o endereço Kindle informado no `.env`. Apenas o formato **EPUB** é aceito por e-mail.

> Os envios por e-mail são feitos com autenticação SMTP segura e exibem mensagens claras em caso de erro.

---

## 📓 Log de Conversões

Todas as conversões são registradas em `log_conversao.txt` com:

- Título do livro
- Autor
- Caminho do arquivo
- Data e hora

---


### Posso enviar AZW3 por e-mail ao Kindle?

**Não.** A Amazon atualmente só aceita os seguintes formatos por e-mail:  
✔️ EPUB, PDF, DOCX  
❌ MOBI, AZW3

### O Kindle precisa estar conectado via cabo?

Apenas para a opção 2 (envio por USB). As demais funcionam com o dispositivo offline.

---





