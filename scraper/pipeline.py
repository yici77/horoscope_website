import json
import os
import re
import google.generativeai as genai
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from dotenv import load_dotenv

load_dotenv()

# ── Gemini setup ─────────────────────────────────────────
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# ── Constants ─────────────────────────────────────────────
STAR_SIGNS = [
    "牡羊座", "金牛座", "雙子座", "巨蟹座", "獅子座",
    "處女座", "天秤座", "天蠍座", "射手座", "摩羯座",
    "水瓶座", "雙魚座"
]

CATEGORIES = ["愛情", "事業", "財運", "健康", "綜合"]
VALID_VALUES = {"好", "一般", "差"}

# Sign name mapping: Chinese → English filename
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

# Category mapping: Chinese → English label
CATEGORY_MAP = {
    "愛情": "Love",
    "事業": "Career",
    "財運": "Wealth",
    "健康": "Health",
    "綜合": "Overall",
}

# Chart colors matching chart.py
COLORS = ["#B7927B", "#C9A96E", "#9B8A78", "#A67C5B", "#6B4A47"]

# ── Step 1: Analyse text with Gemini ─────────────────────
def analyse_with_gemini(post):
    prompt = f"""
    以下會附上星座運勢的文章，
    請將文章內容分析出十二星座的五種運勢:"愛情""事業""財運""健康""綜合"，
    並分析出運勢分別為"好""一般""差"，
    分析完用以下字典格式返回：
    {{
        "星座": {{
            "愛情": "好",
            "事業": "差",
            "財運": "差",
            "健康": "好",
            "綜合": "一般"
            }},
        ...
    }}
    其中"星座"替換成"摩羯座""金牛座"等12星座，
    字典的key只能出現"愛情""事業""財運""健康""綜合"，不能出現其他字，
    字典的value只能出現："好""一般""差"三個評級，
    只回傳 JSON，不要有其他文字或 markdown，
    以下是文章：
    {post}
    """
    response = model.generate_content(prompt)
    return response.text.strip()


def run_analysis(input_file, output_file):
    with open(input_file, "rt", encoding="utf-8") as f:
        text = f.read()

    posts = text.split("：D")
    results = []

    for i, post in enumerate(posts):
        if not post.strip():
            continue
        try:
            raw = analyse_with_gemini(post)
            # Strip markdown code fences if present
            raw = re.sub(r"```(?:json)?", "", raw).strip()
            raw = raw.replace("白羊座", "牡羊座").replace("魔羯座", "摩羯座").replace("天平座", "天秤座")
            dic_result = json.loads(raw)
            results.append(dic_result)
            print(f"  Analysed article {i + 1}")
        except json.JSONDecodeError:
            print(f"  Article {i + 1}: JSON parse error, skipping")
        except Exception as e:
            print(f"  Article {i + 1}: {e}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"Analysis saved to {output_file}")


# ── Step 2: Calculate statistics ─────────────────────────
def run_statistics(input_file, output_file):
    result = {
        sign: {cat: {"好": 0, "一般": 0, "差": 0} for cat in CATEGORIES}
        for sign in STAR_SIGNS
    }

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for article_data in data:
        for sign, evaluations in article_data.items():
            if sign not in STAR_SIGNS:
                continue
            for category in CATEGORIES:
                value = evaluations.get(category, "")
                if value in VALID_VALUES:
                    result[sign][category][value] += 1

    # Calculate proportions
    for sign in result:
        for category in result[sign]:
            counts = result[sign][category]
            total = sum(counts.values())
            result[sign][category]["proportion"] = {
                k: round((v / total) * 100, 2) if total > 0 else 0.0
                for k, v in counts.items()
            }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    print(f"Statistics saved to {output_file}")


# ── Step 3: Generate charts ───────────────────────────────
def generate_chart(sign_zh, category_data, output_path):
    labels = [CATEGORY_MAP[cat] for cat in CATEGORIES]
    values = [category_data[cat]["proportion"]["好"] for cat in CATEGORIES]

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')

    bar_width = 0.55

    for i, (value, color) in enumerate(zip(values, COLORS)):
        rounding = bar_width * 0.35
        rounded_bar = FancyBboxPatch(
            (i - bar_width / 2, 0),
            bar_width,
            value,
            boxstyle=f"round,pad=0,rounding_size={rounding}",
            linewidth=0,
            facecolor=color,
            edgecolor="none",
            clip_on=False,
            zorder=3,
            alpha=0.88
        )
        ax.add_patch(rounded_bar)

        ax.text(
            i,
            value + 1.5,
            f"{value:.0f}%",
            ha='center',
            va='bottom',
            fontsize=12,
            color="#4A312F",
            fontweight='bold',
            fontfamily='serif'
        )

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.tick_params(axis='x', colors="#4A312F", labelsize=15, length=0)

    for label in ax.get_xticklabels():
        label.set_fontfamily('serif')

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.yaxis.set_visible(False)
    ax.grid(False)
    ax.set_xlim(-0.7, len(labels) - 0.3)
    ax.set_ylim(0, 82)

    plt.tight_layout()
    plt.savefig(
        output_path,
        transparent=True,
        dpi=300,
        bbox_inches='tight',
        facecolor='none',
        edgecolor='none'
    )
    plt.close()
    print(f"  Chart saved: {output_path}")


def run_charts(statistic_file, media_dir):
    with open(statistic_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(media_dir, exist_ok=True)

    for sign_zh, category_data in data.items():
        sign_en = SIGN_MAP.get(sign_zh)
        if not sign_en:
            continue
        output_path = os.path.join(media_dir, f"{sign_en}.png")
        generate_chart(sign_zh, category_data, output_path)


# ── Main pipeline ─────────────────────────────────────────
def run_pipeline():
    base = os.path.dirname(os.path.abspath(__file__))

    # File paths
    text_file       = os.path.join(base, "star_week_text.txt")
    results_file    = os.path.join(base, "star_results_week.json")
    statistic_file  = os.path.join(base, "star_statistic_week.json")

    # Django media folder (two levels up from scraper/)
    media_dir = os.path.join(base, "..", "media")

    print("=== Step 1: Analysing articles with Gemini ===")
    run_analysis(text_file, results_file)

    print("=== Step 2: Calculating statistics ===")
    run_statistics(results_file, statistic_file)

    print("=== Step 3: Generating charts ===")
    run_charts(statistic_file, media_dir)

    print("=== Pipeline complete ===")


if __name__ == "__main__":
    run_pipeline()
