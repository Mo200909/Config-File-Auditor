# Imports: sys gives access to the filename typed after the script name (sys.argv) and to sys.exit().
import sys


# PARSER: reads the config file line by line, skips blank lines and # comments,
# splits each remaining line into a name and a value, and returns them as a {name: value} dictionary.
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


# RULES: the checklist. Each rule is (setting name, test that returns True when the value is bad, severity, message).
# Most tests flag any value that is not "no"; MaxAuthTries converts the text to a number and flags anything above 4.
RULES = [
    ("PermitRootLogin", lambda v: v.lower() != "no", "HIGH", "Root login allowed over SSH"),
    ("PermitEmptyPasswords", lambda v: v.lower() != "no", "HIGH", "Empty passwords allowed"),
    ("PasswordAuthentication", lambda v: v.lower() != "no", "MEDIUM", "Password auth on; use keys"),
    ("MaxAuthTries", lambda v: int(v) > 4, "MEDIUM", "Too many login attempts allowed"),
    ("X11Forwarding", lambda v: v.lower() != "no", "LOW", "X11 forwarding enabled"),
]


# AUDIT: walks through every rule and, only when the setting exists in the file and its test says bad,
# saves a finding; returns the full list after all rules have been checked.
def audit(settings):
    findings = []
    for name, is_bad, severity, message in RULES:
        if name in settings and is_bad(settings[name]):
            findings.append((severity, name, settings[name], message))
    return findings


# MAIN: checks that a filename was given, prints the raw file, runs the parser and audit,
# then prints either "No findings found" or one line per finding plus a total count.
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


# ENTRY POINT: runs main() only when this file is run directly, not when it is imported by another file.
if __name__ == "__main__":
    main()
