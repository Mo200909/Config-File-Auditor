import sys


# PARSER for auditor
def parse_config(path):
    settings = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(None, 1)
            if len(parts) == 2:
                settings[parts[0]] = parts[1]
    return settings


RULES = [
    ("PermitRootLogin", lambda v: v.lower() != "no", "HIGH", "Root login allowed over SSH"),
    ("PermitEmptyPasswords", lambda v: v.lower() != "no", "HIGH", "Empty passwords allowed"),
    ("PasswordAuthentication", lambda v: v.lower() != "no", "MEDIUM", "Password auth on; use keys"),
    ("MaxAuthTries", lambda v: int(v) > 4, "MEDIUM", "Too many login attempts allowed"),
    ("X11Forwarding", lambda v: v.lower() != "no", "LOW", "X11 forwarding enabled"),
]


def audit(settings):
    findings = []
    for name, is_bad, severity, message in RULES:
        if name in settings and is_bad(settings[name]):
            findings.append((severity, name, settings[name], message))
    return findings


def main():
    if len(sys.argv) != 2:
        print("Usage: auditor.py <config file>")
        sys.exit(1)

    # Print the raw config file first
    with open(sys.argv[1], 'r') as f:
        print(f.read())

    settings = parse_config(sys.argv[1])
    findings = audit(settings)

    if not findings:
        print("No findings found")
        return

    for severity, name, value, message in findings:
        print(f"[{severity}] {name}: {value} -> {message}")
    print(f"{len(findings)} findings found")


if __name__ == "__main__":
    main()