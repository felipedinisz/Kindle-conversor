import os
import subprocess
import shutil
import smtplib
from email.message import EmailMessage
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from dotenv import load_dotenv

load_dotenv()

EBOOK_CONVERT = os.getenv("EBOOK_CONVERT_PATH")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

LOG_FILE = "conversion_log.txt"


def sanitize_pdf(input_pdf):
    print("\U0001F9FC Preprocessing PDF with Ghostscript...")
    output_pdf = os.path.splitext(input_pdf)[0] + "_cleaned.pdf"
    
    gs_path = os.getenv("GHOSTSCRIPT_PATH", "gswin64c" if os.name == 'nt' else "gs")

    gs_cmd = [
        gs_path,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/screen",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_pdf}",
        input_pdf
    ]

    try:
        subprocess.run(gs_cmd, check=True)
        return output_pdf
    except FileNotFoundError:
        print("\n❌ Ghostscript not found. Skipping cleaning step.")
        return input_pdf
    except subprocess.CalledProcessError:
        print("\n❌ Ghostscript preprocessing failed. Proceeding with original PDF.")
        return input_pdf


def convert_pdf(input_pdf, cover, title, author, output_dir, fmt):
    os.makedirs(output_dir, exist_ok=True)
    cleaned_pdf = sanitize_pdf(input_pdf)
    output_file = os.path.join(output_dir, f"{title}.{fmt}")

    cmd = [
        EBOOK_CONVERT,
        cleaned_pdf,
        output_file,
        "--title", title,
        "--authors", author,
        "--cover", cover,
    ]
    try:
        print("\n\U0001F504 Converting...")
        subprocess.run(cmd, check=True)
        print("\n✅ Conversion successful!")
        return output_file
    except subprocess.CalledProcessError as e:
        print("\n❌ Conversion failed:", e)
        return None


def send_to_kindle_usb(filepath):
    print("\n🔍 Looking for Kindle device...")
    possible_drives = [f"{chr(d)}:/" for d in range(65, 91) if os.path.exists(f"{chr(d)}:/documents")]
    if not possible_drives:
        print("❌ Kindle not detected.")
        return

    kindle_path = os.path.join(possible_drives[0], "documents")
    try:
        shutil.copy(filepath, kindle_path)
        print(f"✅ Sent to Kindle via USB: {filepath}")
    except Exception as e:
        print("❌ Error sending via USB:", e)


def send_to_kindle_email(filepath):
    if not filepath.lower().endswith(".epub"):
        print("❌ Only EPUB files can be sent via email.")
        return

    msg = EmailMessage()
    msg['Subject'] = 'Kindle Book Delivery'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECIPIENT

    with open(filepath, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(filepath)
        msg.add_attachment(file_data, maintype='application', subtype='epub+zip', filename=file_name)

    try:
        print("\n✉️ Sending email...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("✅ Sent to Kindle via email!")
    except Exception as e:
        print("❌ Email sending failed:", e)


def main():
    print("=== eBook Converter for Kindle (EPUB/AZW3) ===\n")
    print("Choose an option:")
    print("1 - Convert PDF")
    print("2 - Send ready file to Kindle (USB)")
    print("3 - Send ready file to Kindle (Email/EPUB only)")
    choice = input("> ")

    if choice == "1":
        n = int(input("How many books to convert? "))
        output_dir = prompt("\n📁 Output folder: ", completer=PathCompleter()) or "Converted_Books"

        with open(LOG_FILE, "a", encoding="utf-8") as log:
            for i in range(1, n + 1):
                print(f"\n=== Book {i} of {n} ===")
                pdf_path = prompt("📄 PDF file: ", completer=PathCompleter())
                cover_path = prompt("🖼️  Cover image: ", completer=PathCompleter())
                title = input("📘 Title: ")
                author = input("✍️  Author: ")
                fmt = input("Output format (azw3/epub): ").lower()

                result = convert_pdf(pdf_path, cover_path, title, author, output_dir, fmt)

                if result:
                    log.write(f"{title} | {author} | {result}\n")

    elif choice == "2":
        file_path = prompt("\n📄 File to send via USB: ", completer=PathCompleter())
        send_to_kindle_usb(file_path)

    elif choice == "3":
        file_path = prompt("\n📄 EPUB file to send via email: ", completer=PathCompleter())
        send_to_kindle_email(file_path)

    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()