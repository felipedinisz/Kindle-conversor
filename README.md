# Kindle Converter CLI Tool

A command-line tool built to convert PDF files into Kindle-compatible formats (AZW3 or EPUB), and send them to your Kindle either via USB or email. Ideal for users who want a smooth and organized document library on their Kindle devices.

---

## 📚 Why This Tool?

After receiving a new Kindle, I noticed that many of my personal documents were unformatted, without covers, and in unsupported formats. Sending via USB was also problematic due to changes in how newer Kindle models mount drives.

This tool solves those problems:

* Converts PDFs to EPUB or AZW3 with custom metadata and cover.
* Automatically detects your Kindle for USB delivery.
* Supports sending EPUB files directly to your Kindle via email.

---

## 🔧 Features

* Convert PDFs to AZW3 or EPUB using Calibre's `ebook-convert`
* Add custom title, author, and cover image
* Automatically log all conversions
* Send files to Kindle:

  * 📤 via USB (any format)
  * ✉️ via Email (EPUB only)

---

## 📦 Requirements

* Python 3.7+
* [Calibre](https://calibre-ebook.com/download) installed (for `ebook-convert`)
* `pip install -r requirements.txt`

```bash
prompt_toolkit
python-dotenv
```

---

## 🛠️ Setup

1. Install Calibre and locate the path to `ebook-convert.exe` (usually `C:\Program Files\Calibre2\ebook-convert.exe`).
2. Create a `.env` file in the project root:

```
EBOOK_CONVERT_PATH=C:\Program Files\Calibre2\ebook-convert.exe
EMAIL_REMETENTE=your_email@gmail.com
EMAIL_SENHA=your_app_password
EMAIL_DESTINO=your_kindle_address@kindle.com
SMTP_SERVIDOR=smtp.gmail.com
SMTP_PORTA=587
```

> ⚠️ Use an **App Password** from Gmail, not your main password. Enable 2FA and generate a password [here](https://myaccount.google.com/apppasswords).

---

## 🚀 How to Use

```bash
python kindle_converter.py
```

You will be prompted to:

1. Convert a PDF (add title, author, cover, format)
2. Send already converted files via USB
3. Send EPUB files to your Kindle via email

---

## 📁 Output

* All converted files will be saved to a specified folder
* A `conversion_log.txt` is created to track your conversions

---

## 🧠 Built With Help From AI

This tool was built with some guidance from artificial intelligence for optimizing Python code, writing the README, and formatting output messages.

---

## 📢 Contributing / Feedback

Feel free to fork or open an issue. Feedback is welcome!

---

## 🔗 Repository

[https://github.com/felipedinisz/Kindle-conversor](https://github.com/felipedinisz/Kindle-conversor)
