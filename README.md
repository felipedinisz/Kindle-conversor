# 📚 Kindle Converter CLI Tool

A command-line tool designed to convert PDF files into Kindle-compatible formats (AZW3 or EPUB), and send them to your Kindle via USB or email. Perfect for users who want a smooth, customized document library on their Kindle devices.

---

## ❓ Why This Tool?

When I received my Kindle, I noticed many personal PDFs were poorly formatted, lacked metadata or covers, and some wouldn’t transfer properly via USB due to recent Kindle updates.

This tool solves that:

* Converts PDFs to EPUB or AZW3 with custom metadata and covers
* Automatically detects your Kindle for USB delivery
* Supports EPUB email delivery for seamless wireless transfer

---

## ⚙️ Features

* Convert PDFs to AZW3 or EPUB using Calibre’s `ebook-convert`
* Add custom title, author, and cover image
* Automatically logs all conversions
* Send files to Kindle:

  * 📤 USB (any supported format)
  * ✉️ Email (EPUB only)

---

## 📦 Requirements

* Python 3.7+
* [Calibre](https://calibre-ebook.com/download) installed (with `ebook-convert` accessible)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

**`requirements.txt`** should contain:

```text
prompt_toolkit
python-dotenv
```

---

## 🛠️ Setup

1. Install Calibre and find the path to `ebook-convert.exe` (typically: `C:\Program Files\Calibre2\ebook-convert.exe`)
2. Create a `.env` file in the project root with the following:

```ini
EBOOK_CONVERT_PATH=C:\Program Files\Calibre2\ebook-convert.exe
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECIPIENT=your_kindle_address@kindle.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

> ⚠️ Use a Gmail **App Password**, not your main account password. Make sure 2FA is enabled and generate an app password [here](https://myaccount.google.com/apppasswords).

---

## 🚀 Usage

Run the script:

```bash
python kindle_converter.py
```

Then choose one of the options:

1. Convert a PDF (add metadata, choose output format)
2. Send an already converted file via USB
3. Send an EPUB file to Kindle via email

---

## 📁 Output

* Converted files are saved to a user-specified folder
* All operations are logged in `conversion_log.txt`

---

## 🧠 AI Assistance

Some components were optimized using AI suggestions, including CLI improvements and this README.

---

## 🙌 Contributing / Feedback

Feel free to fork this project or open an issue with suggestions or bug reports. Contributions are welcome!

---

## 🔗 Repository

[https://github.com/felipedinisz/Kindle-conversor](https://github.com/felipedinisz/Kindle-conversor)
