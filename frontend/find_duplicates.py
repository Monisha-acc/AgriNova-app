
import re
from collections import Counter

content = open(r'c:\Users\Lithi\OneDrive\Desktop\AgriNova-final\AgriNova-app\frontend\src\context\LanguageContext.jsx', 'r', encoding='utf-8').read()

# Match something like "key: { en: '...', ta: '...' },"
# with potential newlines or different quotes.
matches = re.findall(r'(\w+):\s*{', content)

# Check for duplicates
counts = Counter(matches)
duplicates = {k: v for k, v in counts.items() if v > 1}

print(f"Found {len(duplicates)} duplicate keys in translations:")
for k, v in duplicates.items():
    print(f"Key: '{k}' used {v} times.")

