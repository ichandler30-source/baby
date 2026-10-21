import io
import re
import urllib.request
import zipfile

url = "https://www.ssa.gov/oact/babynames/names.zip"

# Use browser-like headers so the SSA server allows the download
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.ssa.gov/oact/babynames/limits.html",
}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as response:
    zip_bytes = response.read()

# Read each yearly file (yobYYYY.txt) from the zip archive and write to CSV
with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf, open("ssa-baby-names.csv", "w", encoding="utf-8") as out:
    out.write("year,name,sex,count\n")
    for filename in sorted(zf.namelist()):
        match = re.fullmatch(r"yob(\d{4})\.txt", filename)
        if match:
            year = match.group(1)
            with zf.open(filename) as f:
                for line in io.TextIOWrapper(f, encoding="utf-8"):
                    out.write(f"{year},{line.strip()}\n")
