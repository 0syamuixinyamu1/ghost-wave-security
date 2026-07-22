# Paper build

1. Download the official `neurips_2026.sty` file.
2. Place it in this directory.
3. Run the benchmark from the repository root so that
   `results_generated.tex` and the figures exist.
4. Compile:

```bash
cd paper
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The paper is a concept-and-feasibility draft, not a claim of production security.
