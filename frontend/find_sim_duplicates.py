
import re
from collections import Counter

content = open(r'c:\Users\Lithi\OneDrive\Desktop\AgriNova-final\AgriNova-app\frontend\src\pages\FarmSimulation.jsx', 'r', encoding='utf-8').read()

# Only search within the TAMIL_SIM_STRINGS object to avoid confusion with other things
sim_strings_match = re.search(r'const TAMIL_SIM_STRINGS = {(.*?)};', content, re.DOTALL)
if sim_strings_match:
    sim_content = sim_strings_match.group(1)
    # Match 'Key': 'Value'
    matches = re.findall(r"['\"]([^'\"]+)['\"]\s*:", sim_content)
    counts = Counter(matches)
    duplicates = {k: v for k, v in counts.items() if v > 1}

    print(f"Found {len(duplicates)} duplicate keys in TAMIL_SIM_STRINGS:")
    for k, v in duplicates.items():
        print(f"Key: '{k}' used {v} times.")
else:
    print("Could not find TAMIL_SIM_STRINGS")
