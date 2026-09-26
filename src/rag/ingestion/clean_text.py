import json
import re


INPUT_PATH = "data/processed/cleaned_pdf.json"

ARABIC_PATH = "data/processed/arabic.json"
ENGLISH_PATH = "data/processed/english.json"


def split_languages(text):
    """
    Split Arabic and English text.
    English section starts at 'Article <number>'.
    """

    pattern = re.compile(
        r"(?m)^\s*Article\s+\d+"
    )

    match = pattern.search(text)

    if match:
        arabic_text = text[:match.start()].strip()
        english_text = text[match.start():].strip()
    else:
        arabic_text = text.strip()
        english_text = ""

    return arabic_text, english_text


def separate_languages(input_path):

    with open(input_path, "r", encoding="utf-8") as file:
        pages = json.load(file)

    arabic_pages = []
    english_pages = []

    for page in pages:

        arabic_text, english_text = split_languages(
            page["text"]
        )

        if arabic_text:
            arabic_pages.append({
                "page": page["page"],
                "text": arabic_text
            })

        if english_text:
            english_pages.append({
                "page": page["page"],
                "text": english_text
            })

    # Save Arabic JSON
    with open(ARABIC_PATH, "w", encoding="utf-8") as file:
        json.dump(
            arabic_pages,
            file,
            ensure_ascii=False,
            indent=2
        )

    # Save English JSON
    with open(ENGLISH_PATH, "w", encoding="utf-8") as file:
        json.dump(
            english_pages,
            file,
            ensure_ascii=False,
            indent=2
        )

    print(f"Arabic pages: {len(arabic_pages)}")
    print(f"English pages: {len(english_pages)}")

    print(f"Arabic saved to: {ARABIC_PATH}")
    print(f"English saved to: {ENGLISH_PATH}")


if __name__ == "__main__":
    separate_languages(INPUT_PATH)