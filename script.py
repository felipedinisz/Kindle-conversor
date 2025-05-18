"""
CLI Tool for Converting and Sending eBooks to Kindle (AZW3/EPUB via USB or Email)
Author: Felipe Diniz
"""

import os
import string
import shutil
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

load_dotenv()

EBOOK_CONVERT_PATH = os.getenv("EBOOK_CONVERT_PATH")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

def find_kindle():
    for letter in string.ascii_uppercase:
        path = f"{letter}:\\documents"
        if os.path.isdir(path):
            return path
    return None

def send_to_kindle_usb(file_path):
    kindle_path = find_kindle()
    if kindle_path:
        response = prompt(f"\nKindle detected at {kindle_path}. Send file via USB? (y/n): ").strip().lower()
        if response == 'y':
            try:
                shutil.copy2(file_path, kindle_path)
                print("File sent successfully via USB!")
            except Exception as e:
                print(f"Error copying file: {e}")
        else:
            print("File not sent.")
    else:
        print("\nNo Kindle device detected via USB.")

def send_to_kindle_email(file_path):
    if not file_path.lower().endswith(".epub"):
        print("❌ Only EPUB files can be sent via email to Kindle.")
        return

    print("\n📤 Sending email...")
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECIPIENT
    msg['Subject'] = "Kindle Document"

    with open(file_path, 'rb') as f:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
        msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
            print("✅ File sent successfully to Kindle via email!")
    except Exception as e:
        print(f"❌ Email send failed: {e}")

def convert_pdf(input_pdf, cover_img, title, author, output_dir, output_format):
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{title}.{output_format}")

    command = [
        EBOOK_CONVERT_PATH,
        input_pdf,
        output_file,
        '--cover', cover_img,
        '--title', title,
        '--authors', author
    ]

    print("\n🔄 Converting...")
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Conversion error:\n{result.stderr}")
            return None
        else:
            print(f"✅ Converted to: {output_file}")
            with open("conversion_log.txt", "a", encoding="utf-8") as log:
                log.write(f"[{datetime.now()}] \"{title}\" by {author} -> {output_file}\n")
            return output_file
    except FileNotFoundError:
        print("❌ Calibre's ebook-convert not found. Check path.")
        return None

def input_path(msg):
    return prompt(msg, completer=PathCompleter()).strip()

def main():
    print("=== eBook Converter for Kindle (EPUB/AZW3) ===\n")
    choice = prompt("Choose an option:\n1 - Convert PDF\n2 - Send ready file to Kindle (USB)\n3 - Send ready file to Kindle (Email/EPUB only)\n> ").strip()

    if choice == '1':
        count = int(prompt("How many books to convert? "))
        output_dir = input_path("📁 Output folder: ") or "Converted_Books"

        for i in range(count):
            print(f"\n=== Book {i+1} of {count} ===")
            pdf = input_path("📄 PDF file: ")
            cover = input_path("🖼️  Cover image: ")
            title = prompt("📘 Title: ").strip()
            author = prompt("✍️  Author: ").strip()
            fmt = prompt("Output format (azw3/epub): ").strip().lower()
            result = convert_pdf(pdf, cover, title, author, output_dir, fmt)
            if result:
                send_to_kindle_usb(result)
                send_to_kindle_email(result)

    elif choice == '2':
        n = int(prompt("How many files to send via USB? "))
        for _ in range(n):
            file_path = input_path("Path to the file: ")
            send_to_kindle_usb(file_path)

    elif choice == '3':
        n = int(prompt("How many files to send via email? (EPUB only) "))
        for _ in range(n):
            file_path = input_path("Path to EPUB file: ")
            send_to_kindle_email(file_path)

    print("\n📓 Conversion and delivery log saved to: conversion_log.txt")

if __name__ == "__main__":
    main()