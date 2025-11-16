# Security Policy

## 🔒 Security Commitment

The Reactive Multi-Monitor Light Show is committed to maintaining a secure codebase. We take security seriously and appreciate the community's help in identifying potential issues.

## 🛡️ Automated Security Scanning

This project uses multiple automated security tools:

### 1. **Bandit** - Python Security Linter
- Scans Python code for common security issues
- Checks for: SQL injection, hardcoded passwords, unsafe functions, etc.
- Runs on every commit and weekly

### 2. **Safety** - Dependency Vulnerability Scanner
- Checks all Python dependencies against known vulnerability databases
- Monitors: pygame, numpy, pyaudio
- Alerts on outdated packages with security fixes

### 3. **CodeQL** - Semantic Code Analysis
- GitHub's advanced code analysis engine
- Detects: injection flaws, path traversal, XSS, and more
- Deep semantic understanding of code flow

### 4. **ShellCheck** - Bash Script Analysis
- Lints all shell scripts for security issues
- Checks: command injection, unsafe expansions, quoting issues
- Validates: install.sh, start-light-show.sh

## ✅ Security Scan Status

All scans run automatically on:
- Every push to master/main
- Every pull request
- Weekly schedule (Mondays at 00:00 UTC)

View current scan results: [GitHub Actions](../../actions/workflows/security-scan.yml)

## 🔍 What We Scan For

### Python Code (Bandit)
- ✅ Command injection vulnerabilities
- ✅ SQL injection risks
- ✅ Hardcoded secrets/passwords
- ✅ Unsafe deserialization
- ✅ Weak cryptography
- ✅ Path traversal issues

### Dependencies (Safety)
- ✅ Known CVEs in packages
- ✅ Outdated vulnerable versions
- ✅ Security advisories

### Shell Scripts (ShellCheck)
- ✅ Command injection
- ✅ Unsafe variable expansion
- ✅ Quoting issues
- ✅ Path traversal

## 🚨 Reporting Security Issues

If you discover a security vulnerability, please report it responsibly:

### For Public Issues (Low Severity)
- Open a GitHub Issue with the `security` label
- Include: description, steps to reproduce, impact

### For Private Issues (High Severity)
- **DO NOT** open a public issue
- Email: [Your email or create GitHub Security Advisory]
- Include: full details, proof of concept, suggested fix

### What to Expect
- **Acknowledgment**: Within 48 hours
- **Assessment**: Within 1 week
- **Fix**: Within 2 weeks for critical issues
- **Disclosure**: Coordinated disclosure after fix is released

## 🔐 Security Best Practices

This project follows secure coding practices:

1. **No Hardcoded Credentials** - No API keys, passwords, or secrets in code
2. **Input Validation** - All user input is validated and sanitized
3. **Principle of Least Privilege** - Requests only necessary permissions
4. **Dependency Auditing** - Regular updates and vulnerability checks
5. **Secure Defaults** - Safe configurations out of the box

## 📦 Dependencies Security

### Python Packages
- `pygame` - Graphics library (regularly updated)
- `numpy` - Numerical computing (regularly updated)
- `pyaudio` - Audio interface (regularly updated)

### System Tools
- `xrandr` - Part of X11 (system-managed)
- `xdotool` - Window management (system-managed)
- `wmctrl` - Window control (system-managed)

All dependencies are:
- ✅ Open source and auditable
- ✅ Actively maintained
- ✅ Scanned for vulnerabilities
- ✅ Updated regularly

## 🔄 Update Policy

- **Critical Security Issues**: Patched immediately
- **High Severity**: Patched within 1 week
- **Medium Severity**: Patched within 1 month
- **Low Severity**: Addressed in next release

## 📋 Security Checklist for Contributors

When contributing code, ensure:

- [ ] No hardcoded secrets or credentials
- [ ] User input is validated
- [ ] No use of `eval()`, `exec()`, or similar dangerous functions
- [ ] Shell commands use proper escaping
- [ ] File paths are validated
- [ ] Dependencies are up-to-date
- [ ] Code passes Bandit security scan
- [ ] Shell scripts pass ShellCheck

## 🏆 Security Hall of Fame

We appreciate security researchers who help keep this project safe. Responsible disclosure will be acknowledged here.

*No security issues reported yet.*

## 📄 License

This security policy is part of the Reactive Multi-Monitor Light Show project and is subject to the same license as the project.

---

**Last Updated**: 2025-01-16
