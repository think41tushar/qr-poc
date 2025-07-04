import sys
import os

# Ensure app/ and root directory are importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import qrcode
from dotenv import load_dotenv
from sqlmodel import Session, select
from app.db import engine
from app.models import Shop

# --- Always load .env from project root ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
env_path = os.path.join(ROOT_DIR, ".env")
print(f"[ENV] Loading .env from: {env_path}")

load_dotenv(dotenv_path=env_path, override=True)

# Debug: print the envs (remove/comment later)
for key in ("PUBLIC_BASE_URL", "DATABASE_URL"):
    print(f"[ENV] {key} = {os.environ.get(key)}")

BASE_URL = os.environ.get("PUBLIC_BASE_URL")
print(f"[INFO] Using PUBLIC_BASE_URL: {BASE_URL}")

# Optional: Save QR images in a subfolder
QR_FOLDER = os.path.join(ROOT_DIR, "qr_codes")
os.makedirs(QR_FOLDER, exist_ok=True)

def make_qrs():
    with Session(engine) as session:
        shops = session.exec(select(Shop)).all()
        print(f"[INFO] Found {len(shops)} shops in DB")
        if not shops:
            print("[WARN] No shops found! Please create shop data first.")
            return
        for shop in shops:
            url = f"{BASE_URL}/shops/{shop.id}"
            img = qrcode.make(url)
            qr_path = os.path.join(QR_FOLDER, f"shop_{shop.id}.png")
            img.save(qr_path)
            print(f"[OK] QR for {shop.name}: {url} (saved: {qr_path})")

if __name__ == "__main__":
    make_qrs()