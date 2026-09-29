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
### Tested

The following limitations were reproduced through local testing with separate edge-case configuration files:

- A non-numeric `MaxAuthTries` crashes the script:
  `ValueError: invalid literal for int() with base 10: 'abc'` (reproduced with `edgetest.conf`).

- A setting missing from the file passes silently. For example, a file containing only `Port 22` produces no finding for the monitored settings.

- Setting names are matched case-sensitively. For example, `permitrootlogin yes` is not recognized as `PermitRootLogin`.

- If a setting appears twice, the parser keeps the last value encountered. For example, `PermitRootLogin no` followed by `PermitRootLogin yes` produces a finding for `yes`.

- Inline comments are treated as part of the value. For example, `PermitRootLogin no # keep off` is interpreted as the value `no # keep off` and produces a false finding.

- `Match` blocks are not handled separately. A setting inside a `Match` block is parsed and evaluated as though it were a global setting.

These tests document the current behavior of the parser and are not intended to represent a fully standards-compliant OpenSSH configuration parser.

## Build note

Built following an AI-generated step-by-step walkthrough, then run and tested by me against the good, bad, and edge-case configs above. The rules and parser have not been extended beyond that walkthrough.

## Build note

Built following an AI-generated step-by-step walkthrough, then run and tested by me against the good, bad, and edge-case configs above. The rules and parser have not been extended beyond that walkthrough.
