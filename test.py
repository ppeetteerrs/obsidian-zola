from pathlib import Path
from shutil import move

from utils import slugify_path

old_paths = list(Path("build/__docs").glob("**/*"))

for old_path in set(old_paths):
    if old_path.is_file():
        new_path = slugify_path(old_path)
        print(old_path, "===>", new_path)
        Path(new_path).parent.mkdir(parents=True, exist_ok=True)
        move(old_path, new_path)

print(old_paths)
