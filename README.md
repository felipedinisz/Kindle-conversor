# Kindle Converter CLI

A command-line tool to convert PDF files into Kindle-friendly formats (AZW3 or EPUB), add cover images, and send them to your Kindle via USB or email. Ideal for users who want a personalized and organized experience reading documents on Kindle devices.

## Features

* Convert PDFs to **EPUB** (for email sending) or **AZW3** (for USB transfer).
* Add custom **title**, **author**, and **cover image**.
* Automatically **detects your Kindle** via USB.
* Supports sending **EPUB via email** using your own SMTP credentials.
* Keeps a **conversion log** (`conversion_log.txt`).

## Folder Structure

```
Kindle-conversor/
├── converter.py
├── .env
├── README.md
├── requirements.txt
├── Covers/
│   └── your_cover.jpg
├── Books/
│   └── your_book.pdf
└── Converted_Books/
```

## Requirements

* Python 3.8+
* Calibre installed and its `ebook-convert` path set in your `.env`
* Google/Gmail account with App Password enabled (for email sending)

## Installation

```bash
git clone https://github.com/felipedinisz/Kindle-conversor
cd Kindle-conversor
pip install -r requirements.txt
```

## Setting Up the `.env` File

Create a `.env` file in the root directory:

```ini
EBOOK_CONVERT_PATH=C:\Program Files\Calibre2\ebook-convert.exe
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECIPIENT=your_kindle_address@kindle.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

> ⚠️ Use [senhas de app](https://support.google.com/mail/answer/185833?hl=pt-BR) se estiver usando Gmail com autenticação de dois fatores. A senha comum **não funcionará**.

---

## 🚀 Uso

Execute o script principal:

```bash
python conversor.py
```

Você verá um menu com três opções:

### 1. 📘 Converter PDF para EPUB ou AZW3

Você poderá inserir os dados do livro (PDF, capa, título, autor), escolher o formato de saída e salvá-lo em uma pasta definida. Não é necessário conectar o Kindle nesta etapa.

### 2. Send to Kindle via USB

Choose option **2**, and if your Kindle is connected, the tool will send the file.

### 3. Send to Kindle via Email (EPUB only)

Choose option **3** and your EPUB file will be sent to your Kindle address.

## AI Contribution

Some parts of this project (especially the README, code optimization, and output formatting) were assisted by AI tools to accelerate development and documentation.

## License

MIT

---

Created by Felipe Diniz
