#!/usr/bin/env python3
import base64
import gzip
from pathlib import Path


def encode_file(path: Path) -> str:
    compressed = gzip.compress(path.read_bytes(), compresslevel=9)
    return base64.b64encode(compressed).decode('utf-8')


def build_script():
    to_encode = list(Path('kaggle_petfinder').glob('*.py')) + [Path('setup.py')]
    file_data = {str(path.as_posix()): encode_file(path) for path in to_encode}
    template = Path('script_template.py').read_text('utf8')
    build_dir = Path("build")
    if not build_dir.exists():
        build_dir.mkdir(parents=True, exist_ok=True)
    script_path = build_dir / "script.py"
    script_path.write_text(
        template.replace('{file_data}', str(file_data)),
        encoding='utf8')


if __name__ == '__main__':
    build_script()
