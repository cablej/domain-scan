import logging
import requests

###
# Check if a site has a security.txt file and parse it

# Required scan function. This is the meat of the scanner, where things
# that use the network or are otherwise expensive would go.
#
# Runs locally or in the cloud (Lambda).
def scan(domain: str, environment: dict, options: dict) -> dict:
    results = {}
    for header in headers:
        results[header] = ""

    # security.txt file should only be accessible via HTTPS
    base = 'https://' + domain
    # While the file should be in .well-known, it may be at the root, so try both
    urls = [base + '/.well-known/security.txt', base + '/security.txt']

    has_security_txt = False
    for url in urls:
        if has_security_txt:
            break
        # Try getting security.txt file
        try:
            response = requests.get(url, allow_redirects=True, timeout=4)
            # security.txt file must have text/plain content type
            if response.status_code == requests.codes.ok and 'text/plain' in response.headers['content-type']:
                has_security_txt = True
                contents = parse_security_txt(response.text)
                for name, contents in contents.items():
                    results[field_map[name]] = ','.join(contents)
        except Exception:
            logging.debug("could not get data from %s", url)

    has_vdp = results['policy_link'] != ''
    try:
        response = requests.get(base + '/vulnerability-disclosure-policy', allow_redirects=True, timeout=4)
        if response.status_code == requests.codes.ok and 'vulnerability' in response.text.lower():
            has_vdp = True
            if results['policy_link'] == '':
                results['policy_link'] = base + '/vulnerability-disclosure-policy'
    except Exception:
        logging.debug("could not get data from %s", url)

    results['has_security_txt'] = str(has_security_txt).lower()
    results['has_vdp'] = str(has_vdp).lower()

    logging.warning("security.txt for %s complete!", domain)
    return results

def parse_security_txt(file: str) -> dict:
    fields = {}
    lines = file.splitlines(False)
    for line in lines:
        # Line is a comment or invalid
        if line.startswith('#') or ':' not in line:
            continue
        name, contents = line.split(':', 1)
        name = name.lower()
        contents = contents.strip()
        if name in fields:
            fields[name].append(contents)
        else:
            fields[name] = [contents]
    return fields

# Required CSV row conversion function. Usually one row, can be more.
#
# Run locally.
def to_rows(data):
    row = []
    for page in headers:
        row.extend([data[page]])
    return [row]

field_map = {
    "policy": "policy_link",
    "contact": "contact",
    "acknowledgments": "acknowledgments",
    "canonical": "canonical",
    "encryption": "encryption",
    "expires": "expires",
    "hiring": "hiring",
    "preferred-languages": "preferred_languages"
}

headers = [
    "has_vdp", "has_security_txt", "policy_link", "contact", "is_non_html", "acknowledgments", "canonical", "encryption", "expires", "hiring", "preferred_languages"
]

