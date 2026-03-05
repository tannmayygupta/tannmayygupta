"""
update_readme.py  –  auto-updates the <!-- STREAK --> block in README.md
"""

import re
from datetime import datetime, timezone

README_PATH    = "README.md"
COUNTER_PATH   = ".streak-count.txt"

# ── Load / increment day counter ───────────────────────────────────────────────
try:
    with open(COUNTER_PATH, "r") as f:
        day_count = int(f.read().strip()) + 1
except (FileNotFoundError, ValueError):
    day_count = 1

with open(COUNTER_PATH, "w") as f:
    f.write(str(day_count))

# ── Build new streak block ──────────────────────────────────────────────────────
now   = datetime.now(timezone.utc)
today = now.strftime("%B %d, %Y")   # e.g. March 05, 2026
time  = now.strftime("%I:%M %p UTC") # e.g. 12:00 PM UTC

new_block = (
    "<!-- STREAK:START -->\n"
    "<div align='center'>\n\n"
    "| 🔥 Streak Day | 📅 Last Updated | ⏰ Time |\n"
    "|:---:|:---:|:---:|\n"
    f"| **{day_count}** | {today} | {time} |\n\n"
    "</div>\n"
    "<!-- STREAK:END -->"
)

# ── Patch README ────────────────────────────────────────────────────────────────
with open(README_PATH, "r", encoding="utf-8") as f:
    content = f.read()

pattern = r"<!-- STREAK:START -->.*?<!-- STREAK:END -->"
if re.search(pattern, content, flags=re.DOTALL):
    content = re.sub(pattern, new_block, content, flags=re.DOTALL)
else:
    content += f"\n\n## 🔥 Daily Activity\n{new_block}\n"

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print(f"✅  README updated — Day {day_count} — {today} {time}")
