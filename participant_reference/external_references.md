# External References

These links are maintained by their publishers. Consult the current source when preparing a report or setting policy.

## OWASP

- [OWASP Top 10:2025](https://top10.owasp.org/) is the current awareness list for web application risks. Its categories are Broken Access Control, Security Misconfiguration, Software Supply Chain Failures, Cryptographic Failures, Injection, Insecure Design, Authentication Failures, Software or Data Integrity Failures, Security Logging and Alerting Failures, and Mishandling of Exceptional Conditions.
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) provides practical topic-focused guidance.
- [OWASP Secure Code Review Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html) supplies review-oriented prompts.
- [OWASP ASVS mapping index](https://cheatsheetseries.owasp.org/IndexASVS.html) connects detailed guidance to verification areas.

## CVE references

The [CVE Program](https://www.cve.org/) catalogs publicly disclosed issues. A CVE identifier is a reference, not by itself a severity decision or proof that a component is deployed.

Study examples:

- [CVE-2021-44228](https://www.cve.org/CVERecord?id=CVE-2021-44228)
- [CVE-2023-34362](https://www.cve.org/CVERecord?id=CVE-2023-34362)
- [CVE-2024-3094](https://www.cve.org/CVERecord?id=CVE-2024-3094)

For a dependency report, capture the component name, resolved version, advisory identifier, deployed context, available fixed version, and verification outcome. Do not treat a package-name match in source text or documentation as evidence that the component is installed.

## Additional baseline

- [NIST Secure Software Development Framework](https://csrc.nist.gov/Projects/ssdf) provides a broader secure-development practice framework.
- [CISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) is useful when prioritizing confirmed deployed components.
