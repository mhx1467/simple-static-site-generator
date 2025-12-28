import shutil
import os
from pathlib import Path

def copy_dir(src: Path, dst: Path) -> None:
    if not src.exists() or not src.is_dir():
        raise FileNotFoundError(f"Source directory does not exist: {src}")

    for root, _, files in os.walk(src):
        root_path = Path(root)
        rel_path = root_path.relative_to(src)
        dst_dir = dst / rel_path
        dst_dir.mkdir(parents=True, exist_ok=True)

        for file in files:
            src_file = root_path / file
            dst_file = dst_dir / file
            shutil.copy2(src_file, dst_file)


def main() -> None:
    src_dir = Path("static")
    dst_dir = Path("public")

    if not src_dir.exists():
        raise FileNotFoundError(f"Source directory does not exist: {src_dir}")

    if dst_dir.exists():
        shutil.rmtree(dst_dir)

    dst_dir.mkdir(parents=True, exist_ok=True)
    copy_dir(src_dir, dst_dir)


if __name__ == "__main__":
    main()

