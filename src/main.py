import os
import shutil
from markdown_blocks import generate_pages_recurvise
import sys



def copy_static(source: str, dest: str) -> None:
    if not os.path.exists(dest):
        os.mkdir(dest)

    for name in os.listdir(source):
        src_path = os.path.join(source, name)
        dest_path = os.path.join(dest, name)
        print(f"copying {src_path} -> {dest_path}")
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            copy_static(src_path, dest_path)
 
def main() -> None:
    basepath = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else "/"
    dest = "docs"
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    copy_static("static", dest)
    generate_pages_recurvise("content", "template.html", dest, basepath)


if __name__ == "__main__":
    main()
