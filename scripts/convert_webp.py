"""images/ 폴더에 새로 올라온 jpg/png를 같은 이름의 .webp로 변환한다.
이미 짝이 되는 .webp가 있으면 건너뛰므로 여러 번 실행해도 안전하다(idempotent).
"""
import os
from PIL import Image

IMG_DIR = os.path.join(os.path.dirname(__file__), "..", "images")
SOURCE_EXTS = (".jpg", ".jpeg", ".png")
QUALITY = 80


def main():
    converted = []
    for fname in sorted(os.listdir(IMG_DIR)):
        base, ext = os.path.splitext(fname)
        if ext.lower() not in SOURCE_EXTS:
            continue
        webp_path = os.path.join(IMG_DIR, base + ".webp")
        if os.path.exists(webp_path):
            continue
        src_path = os.path.join(IMG_DIR, fname)
        with Image.open(src_path) as img:
            img.convert("RGB").save(webp_path, "WEBP", quality=QUALITY)
        converted.append(base + ".webp")
        print(f"converted {fname} -> {base}.webp")

    if converted:
        with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as f:
            f.write("changed=true\n")
    else:
        print("no new images to convert")


if __name__ == "__main__":
    main()
