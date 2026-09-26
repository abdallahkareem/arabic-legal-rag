import json
import re
import pymupdf
from src.helpers.config import get_settings

app_settings = get_settings()


# Regex
ARABIC_ARTICLE_RE = re.compile(
    r"مادة\s*\(?\s*([٠-٩0-9]+)\s*\)?"
)

ENGLISH_ARTICLE_RE = re.compile(
    r"Article\s+([0-9]+)"
)



# Arabic numbers → English
def arabic_to_english_number(number):
    table = str.maketrans(
        "٠١٢٣٤٥٦٧٨٩",
        "0123456789"
    )

    return number.translate(table)



# Get text blocks by columns
def extract_columns(page):

    blocks = page.get_text("blocks")

    page_width = page.rect.width
    middle = page_width / 2

    arabic_blocks = []
    english_blocks = []
    full_width_blocks = []

    for block in blocks:

        x0, y0, x1, y1, text = block[:5]

        text = text.strip()

        if not text:
            continue

        block_width = x1 - x0

        # Full width text
        if block_width > page_width * 0.75:

            full_width_blocks.append({
                "x": x0,
                "y": y0,
                "text": text
            })

        # Arabic = right column
        elif x0 >= middle:

            arabic_blocks.append({
                "x": x0,
                "y": y0,
                "text": text
            })

        # English = left column
        else:

            english_blocks.append({
                "x": x0,
                "y": y0,
                "text": text
            })

    # Sort top → bottom
    arabic_blocks.sort(key=lambda x: x["y"])
    english_blocks.sort(key=lambda x: x["y"])
    full_width_blocks.sort(key=lambda x: x["y"])

    return (
        full_width_blocks,
        arabic_blocks,
        english_blocks
    )



# Join blocks
def blocks_to_text(blocks):

    return "\n".join(
        block["text"]
        for block in blocks
    ).strip()



# Extract articles from column
def extract_articles(text, language):

    if language == "ar":

        pattern = ARABIC_ARTICLE_RE

    else:

        pattern = ENGLISH_ARTICLE_RE

    matches = list(pattern.finditer(text))

    articles = []

    for i, match in enumerate(matches):

        article_number = match.group(1)

        if language == "ar":
            article_number = arabic_to_english_number(
                article_number
            )

        start = match.start()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        article_text = text[start:end].strip()

        articles.append({
            "article": int(article_number),
            "text": article_text
        })

    return articles



# Main parser
def parse_pdf(pdf_path):

    doc = pymupdf.open(pdf_path)

    structured_data = []

    current_section = None
    current_topic = None

    for page_number, page in enumerate(doc, start=1):

        (
            full_width_blocks,
            arabic_blocks,
            english_blocks
        ) = extract_columns(page)

        arabic_text = blocks_to_text(arabic_blocks)
        english_text = blocks_to_text(english_blocks)

        # --------------------------------
        # Detect section / topic
        # --------------------------------

        for block in full_width_blocks:

            text = block["text"]

            # You can add more patterns here
            if "الفصل" in text:
                current_section = text

            elif "القسم" in text:
                current_section = text

            elif "أحكام عامة" in text:
                current_section = text

        # --------------------------------
        # Extract Arabic articles
        # --------------------------------

        arabic_articles = extract_articles(
            arabic_text,
            "ar"
        )

        # --------------------------------
        # Extract English articles
        # --------------------------------

        english_articles = extract_articles(
            english_text,
            "en"
        )

        # --------------------------------
        # Match Arabic + English
        # --------------------------------

        english_by_article = {
            item["article"]: item["text"]
            for item in english_articles
        }

        for arabic_article in arabic_articles:

            article_number = arabic_article["article"]

            record = {
                "page": page_number,
                "section": current_section,
                "topic": current_topic,
                "article": article_number,
                "arabic": arabic_article["text"],
                "english": english_by_article.get(
                    article_number,
                    ""
                )
            }

            structured_data.append(record)

    doc.close()

    return structured_data


# -----------------------------
# Save JSON
# -----------------------------

data = parse_pdf(app_settings.PDF_PATH)

with open(
    app_settings.JSON_PATH,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        data,
        file,
        ensure_ascii=False,
        indent=2
    )


print(f"Articles extracted: {len(data)}")
print(f"Saved to: {app_settings.JSON_PATH}")