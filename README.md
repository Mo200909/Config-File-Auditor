# Config-File-Auditor
Python CLI that audits sshd_config-style files for 5 insecure settings and reports findings by severity. Beginner project; known limitations are documented in the README.

Python script that audits an `sshd_config`-style file and flags insecure settings.

## What it checks

| Setting | Flagged when | Severity |
|---|---|---|
| `PermitRootLogin` | value is not `no` | HIGH |
| `PermitEmptyPasswords` | value is not `no` | HIGH |
| `PasswordAuthentication` | value is not `no` | MEDIUM |
| `MaxAuthTries` | value is greater than 4 | MEDIUM |
| `X11Forwarding` | value is not `no` | LOW |

## Usage

```
python auditor.py <config_file>
```

Requires Python 3. No third-party packages.

## Project files

- `auditor.py`: parser, rules, audit logic, report
- `bad_sample.conf`: intentionally insecure config (should produce 5 findings)
- `good_sample.conf`: hardened config (should produce no findings)
- `edgetest.conf`: non-numeric `MaxAuthTries` (should crash; documents a known limitation)

## Sample output

```
$ python auditor.py bad_sample.conf
# sshd_config (intentionally insecure)
Port 22
PermitRootLogin yes
PasswordAuthentication yes
PermitEmptyPasswords yes
X11Forwarding yes
MaxAuthTries 10
[HIGH] PermitRootLogin: yes -> Root login allowed over SSH
[HIGH] PermitEmptyPasswords: yes -> Empty passwords allowed
[MEDIUM] PasswordAuthentication: yes -> Password auth on; use keys
[MEDIUM] MaxAuthTries: 10 -> Too many login attempts allowed
[LOW] X11Forwarding: yes -> X11 forwarding enabled
5 findings found
```

```
$ python auditor.py good_sample.conf
# sshd_config (hardened)
Port 2222
PermitRootLogin no
PasswordAuthentication no
PermitEmptyPasswords no
X11Forwarding no
MaxAuthTries 3
No findings found
```

## Known limitations

Tested:

- A non-numeric `MaxAuthTries` crashes the script:
  `ValueError: invalid literal for int() with base 10: 'abc'` (reproduced with `edgetest.conf`).

Found by reading the code, not yet tested:

- A setting missing from the file passes silently. OpenSSH may apply a default that is insecure.
- Setting names are matched case-sensitively, but OpenSSH keywords are case-insensitive.
- If a setting appears twice, the parser keeps the last value. OpenSSH uses the first.
- Inline comments (`PermitRootLogin no # note`) are read as part of the value and cause a false finding.
- `Match` blocks are not handled.

## Build note

Built following an AI-generated step-by-step walkthrough, then run and tested by me against the good, bad, and edge-case configs above. The rules and parser have not been extended beyond that walkthrough.
