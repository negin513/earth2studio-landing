# Earth2Studio Landing Page

A single-page MkDocs Material landing site for NVIDIA Earth2Studio, using the
NVIDIA theme (green `#76b900`, NVIDIA Sans, light/dark schemes) from
[bionemo-recipes](https://nvidia-bionemo.github.io/bionemo-recipes/).

## Quick Start

```bash
pip install -r requirements.txt
mkdocs serve
```

Then open http://localhost:8000

## Structure

```
earth2studio-landing/
├── mkdocs.yml                  # Material theme, NVIDIA branding, external nav
├── requirements.txt
├── overrides/
│   └── .icons/nvidia/          # NVIDIA logo for the header
└── docs/
    ├── index.md                # The landing page
    └── assets/css/             # NVIDIA color schemes, fonts, component styles
```
