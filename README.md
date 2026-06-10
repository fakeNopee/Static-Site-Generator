# Static Site Generator

A simple, from-scratch **static site generator** written in pure Python. It converts Markdown files from a `content/` directory into a fully static HTML website using a custom Markdown parser and a lightweight templating system.

Perfect for learning how static site generators work under the hood or for small personal sites and documentation.

## Features

- Custom Markdown parser (no external dependencies like `markdown` or `mistune`)
- Recursive page generation (supports nested folders)
- Simple templating using `{{ Title }}` and `{{ Content }}` placeholders
- Automatic copying of static assets (`static/` → output)
- Custom base path support (great for GitHub Pages subdirectories)
- Pure Python stdlib only — no external packages required
- Well-tested core components

## Installation

```bash
# Clone the repository
git clone https://github.com/fakeNopee/Static-Site-Generator.git
cd Static-Site-Generator
```

## Quick Start 

```bash
# Generate the static site (outputs to docs/)
python src/main.py

# Or with a custom base path (useful for GitHub Pages)
python src/main.py "/Static-Site-Generator/"
```
After running, open docs/index.html in your browser to see the generated site.
You can also use the provided shell script:
```bash
./build.sh
```

## Usage

```bash
python src/main.py [basepath]
```
| Argument   | Description                                      | Default |
|------------|--------------------------------------------------|---------|
| basepath   | Base URL path for links (for subfolder deployment) | /       |

**Typical workflow:**
1. Write Markdown files in the content/ folder
2. Add CSS/JS/images to static/
3. Run the generator
4. Deploy the docs/ folder (or configure GitHub Pages to serve from docs/)

## Project Structure

```text
Static-Site-Generator/
├── content/              # Your Markdown source files
├── static/               # Static assets (CSS, images, JS)
├── src/                  # Python source code
│   ├── main.py           # Entry point
│   ├── markdown_to_html_node.py
│   ├── htmlnode.py
│   ├── textnode.py
│   └── ... (other modules)
├── template.html         # Base HTML template
├── docs/                 # Generated output (created automatically)
├── build.sh
└── README.md
```

## How It Works

1. main.py deletes and recreates the docs/ output directory.
2. It copies everything from static/ into docs/.
3. It recursively walks content/, converts each .md file to HTML using the custom parser, injects it into template.html, and writes the result to docs/.

## Examples 
**Input**:
![Generated Website Screenshot](assets/images/demo-screenshot1.png)
**Output**:
![Generated Website Screenshot](assets/images/demo-screenshot2.png)

## Testing

Run the test suite:
```bash
python -m pytest src/ -v
# or
./test.sh
```
