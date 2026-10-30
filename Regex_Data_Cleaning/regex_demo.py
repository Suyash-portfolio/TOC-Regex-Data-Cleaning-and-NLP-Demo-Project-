
import re
from datetime import datetime


# 1. Indian mobile numbers: optional +91 prefix and 10 digits
MOBILE_RE = re.compile(
    r"(?<!\d)(?:\+91[-\s]?)?[6-9][0-9]{9}(?!\d)"
)

# 2. Date candidates: DD/MM/YYYY or DD-MM-YYYY
DATE_RE = re.compile(
    r"(?<!\d)(?:0?[1-9]|[12][0-9]|3[01])"
    r"[-/](?:0?[1-9]|1[0-2])"
    r"[-/](?:19|20)[0-9]{2}(?!\d)"
)

# 3. HTTP and HTTPS URLs
URL_RE = re.compile(r"""https?://[^\s<>"']+""", re.IGNORECASE)

# 4. Basic email addresses
EMAIL_RE = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

# 5. Hashtags
HASHTAG_RE = re.compile(r"#[A-Za-z][A-Za-z0-9_]*")


def extract_valid_dates(text):
    """Extract date patterns and reject impossible calendar dates."""
    valid_dates = []

    for match in DATE_RE.finditer(text):
        candidate = match.group(0)

        # Reject mixed separators, such as 12/05-2026.
        if "/" in candidate and "-" in candidate:
            continue

        date_format = "%d/%m/%Y" if "/" in candidate else "%d-%m-%Y"

        try:
            datetime.strptime(candidate, date_format)
            valid_dates.append(candidate)
        except ValueError:
            # Reject dates such as 31/02/2026.
            continue

    return valid_dates


def extract_urls(text):
    """Remove common punctuation attached to URLs."""
    matches = URL_RE.findall(text)
    return [
        url.rstrip(".,;:!?)]}")
        for url in matches
        if url.rstrip(".,;:!?)]}")
    ]


def show_results(label, matches):
    print(f"\n{label}:")

    if matches:
        for item in matches:
            print(f"  - {item}")
    else:
        print("  No match found.")


def main():
    print("=" * 62)
    print(" REGEX-BASED DATA CLEANING AND INFORMATION EXTRACTION")
    print("=" * 62)

    print(
        "Enter text containing mobile numbers, dates, "
        "URLs, emails, or hashtags."
    )

    text = input("\nInput text: ").strip()

    if not text:
        print("No input entered. Please run the program again.")
        return

    show_results(
        "Indian mobile numbers",
        MOBILE_RE.findall(text)
    )

    show_results(
        "Valid dates (DD/MM/YYYY or DD-MM-YYYY)",
        extract_valid_dates(text)
    )

    show_results(
        "HTTP/HTTPS URLs",
        extract_urls(text)
    )

    show_results(
        "Email addresses",
        EMAIL_RE.findall(text)
    )

    show_results(
        "Hashtags",
        HASHTAG_RE.findall(text)
    )

    print("\nDone.")


if __name__ == "__main__":
    main()
