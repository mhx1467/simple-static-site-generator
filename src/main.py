import shutil
from pathlib import Path
from src.parsers.markdown import MarkdownParser
from string import Template

HTML_TEMPLATE = Template("""
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>$title</title>
    <link href="/index.css" rel="stylesheet" />
  </head>
  <body>
    <article>$content</article>
  </body>
</html>
""")

def generate_html_file(src_file: Path, dst_file: Path, parser: MarkdownParser) -> None:
    content = src_file.read_text()
    first_line = content.splitlines()[0]
    title = first_line.lstrip("#").strip()
    html_content = parser.markdown_to_html_code(content).to_html()
    
    dst_file.parent.mkdir(parents=True, exist_ok=True)
    dst_file.write_text(HTML_TEMPLATE.substitute(title=title, content=html_content))

def copy_static_files(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(f"Static directory not found: {src}")
    shutil.copytree(src, dst, dirs_exist_ok=True)


def build_content(src_dir: Path, dst_dir: Path, parser: MarkdownParser) -> None:
    for md_file in src_dir.rglob("*.md"):
        relative_path = md_file.relative_to(src_dir)
        output_file = (dst_dir / relative_path).with_suffix(".html")
        generate_html_file(md_file, output_file, parser)


def main() -> None:
    static_dir = Path("static")
    content_dir = Path("content")
    public_dir = Path("public")

    for path in (static_dir, content_dir):
        if not path.exists():
            raise FileNotFoundError(f"Required directory not found: {path}")

    if public_dir.exists():
        shutil.rmtree(public_dir)
    public_dir.mkdir()

    copy_static_files(static_dir, public_dir)

    parser = MarkdownParser()
    build_content(content_dir, public_dir, parser)


if __name__ == "__main__":
    main()

