# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# import qrcode
# import os
# from dotenv import load_dotenv
# from sqlmodel import Session, select
# from app.db import engine
# from app.models import Shop

# load_dotenv()
# BASE_URL = os.environ.get("PUBLIC_BASE_URL", "https://5fad-106-51-86-167.ngrok-free.app")

# def make_qrs():
#     with Session(engine) as session:
#         shops = session.exec(select(Shop)).all()
#         for shop in shops:
#             url = f"{BASE_URL}/shops/{shop.id}"
#             img = qrcode.make(url)
#             img.save(f"shop_{shop.id}.png")
#             print(f"QR for {shop.name}: {url}")

# if __name__ == "__main__":
#     make_qrs()
    

import sys
import os

# Ensure app/ and root directory are importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import qrcode
from dotenv import load_dotenv
from sqlmodel import Session, select
from app.db import engine
from app.models import Shop

# --- Robust .env loading (always from project root) ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
env_path = os.path.join(ROOT_DIR, ".env")
print(f"Loading .env from: {env_path}")

load_dotenv(dotenv_path=env_path, override=True)

# Print all envs for debug, you can remove below after confirming!
for key in ("PUBLIC_BASE_URL", "DATABASE_URL"):
    print(f"{key} = {os.environ.get(key)}")

BASE_URL = os.environ.get("PUBLIC_BASE_URL")
print(f"Using PUBLIC_BASE_URL: {BASE_URL}")

def make_qrs():
    with Session(engine) as session:
        shops = session.exec(select(Shop)).all()
        print(f"Found {len(shops)} shops in DB")
        if not shops:
            print("No shops found! Please create shop data first.")
        for shop in shops:
            url = f"{BASE_URL}/shops/{shop.id}"
            img = qrcode.make(url)
            img.save(f"shop_{shop.id}.png")
            print(f"QR for {shop.name}: {url}")

if __name__ == "__main__":
    make_qrs()