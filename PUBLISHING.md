# Publish to GitHub

After downloading and unzipping the repository:

```bash
cd ghost-wave-security
git init
git add .
git commit -m "Initial Ghost Wave Security toy prototype"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ghost-wave-security.git
git push -u origin main
```

Then update the placeholder repository URL in `CITATION.cff`.

Recommended GitHub description:

> Benign toy simulator for sheaf-inspired, diversity-aware recovery in disposable infrastructures.

Recommended topics:

```text
cybersecurity moving-target-defense resilience recovery cellular-sheaves e8 simulation research
```

Before publishing, review the author name in `pyproject.toml`, `CITATION.cff`,
`LICENSE`, and `paper/main.tex`. No email address is included by default.
