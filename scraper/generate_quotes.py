import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# Sign mapping: Chinese → English filename
SIGN_MAP = {
    "牡羊座": "aries",
    "金牛座": "taurus",
    "雙子座": "gemini",
    "巨蟹座": "cancer",
    "獅子座": "leo",
    "處女座": "virgo",
    "天秤座": "libra",
    "天蠍座": "scorpio",
    "射手座": "sagittarius",
    "摩羯座": "capricorn",
    "水瓶座": "aquarius",
    "雙魚座": "pisces",
}

SIGNS_EN = {
    "牡羊座": "Aries",
    "金牛座": "Taurus",
    "雙子座": "Gemini",
    "巨蟹座": "Cancer",
    "獅子座": "Leo",
    "處女座": "Virgo",
    "天秤座": "Libra",
    "天蠍座": "Scorpio",
    "射手座": "Sagittarius",
    "摩羯座": "Capricorn",
    "水瓶座": "Aquarius",
    "雙魚座": "Pisces",
}


def generate_quote(sign_en, article_text):
    prompt = f"""
    Based on the following weekly horoscope content for {sign_en},
    write a single poetic and inspiring mood quote in English.
    
    Requirements:
    - 1 to 2 sentences only
    - Mystical, elegant and uplifting tone
    - Relevant to the week's energy described in the article
    - No quotation marks
    - Return only the quote, nothing else
    
    Horoscope content:
    {article_text[:3000]}
    """
    response = model.generate_content(prompt)
    return response.text.strip()


def extract_sign_content(text, sign_zh):
    """Try to extract content relevant to a specific sign from the full text."""
    # Look for the sign name or its English equivalent
    sign_en = SIGNS_EN[sign_zh]
    sign_file = SIGN_MAP[sign_zh]

    # Try to find a section for this sign
    patterns = [
        rf"{sign_zh}[^\n]*\n(.*?)(?=牡羊座|金牛座|雙子座|巨蟹座|獅子座|處女座|天秤座|天蠍座|射手座|摩羯座|水瓶座|雙魚座|：D|$)",
        rf"{sign_en}[^\n]*\n(.*?)(?=Aries|Taurus|Gemini|Cancer|Leo|Virgo|Libra|Scorpio|Sagittarius|Capricorn|Aquarius|Pisces|：D|$)",
        rf"{sign_file}[^\n]*\n(.*?)(?=aries|taurus|gemini|cancer|leo|virgo|libra|scorpio|sagittarius|capricorn|aquarius|pisces|：D|$)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()[:3000]

    # If no specific section found, return the full text (Gemini will extract relevant parts)
    return text[:3000]


def generate_all_quotes(input_file, output_dir):
    with open(input_file, "rt", encoding="utf-8") as f:
        full_text = f.read()

    os.makedirs(output_dir, exist_ok=True)

    for sign_zh, sign_file in SIGN_MAP.items():
        sign_en = SIGNS_EN[sign_zh]
        print(f"Generating quote for {sign_en}...")

        try:
            # Extract relevant content for this sign
            content = extract_sign_content(full_text, sign_zh)

            # Generate quote
            quote = generate_quote(sign_en, content)

            # Save to individual txt file
            output_path = os.path.join(output_dir, f"{sign_file}_quote.txt")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(quote)

            print(f"  {sign_en}: {quote}")

        except Exception as e:
            print(f"  {sign_en}: Error — {e}")


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base, "star_week_text.txt")
    output_dir = os.path.join(base, "quotes")

    print("=== Generating weekly mood quotes ===")
    generate_all_quotes(input_file, output_dir)
    print("=== Done ===")
