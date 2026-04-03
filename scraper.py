import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

# ──────────────────────────────────────────
# 設定區：改這裡就好
KEYWORD = "藍牙耳機"       # 你想搜尋的關鍵字
MAX_PAGES = 3              # 要抓幾頁（每頁約 20 筆）
OUTPUT_FILE = "prices.csv" # 存檔名稱
# ──────────────────────────────────────────

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def scrape_pchome(keyword, max_pages=3):
    """抓 PChome 搜尋結果的商品名稱與價格"""
    results = []
    today = datetime.now().strftime("%Y-%m-%d")

    for page in range(1, max_pages + 1):
        url = (
            f"https://ecshweb.pchome.com.tw/search/v3.3/all/results"
            f"?q={keyword}&page={page}&sort=sale/dc"
        )

        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"[錯誤] 第 {page} 頁抓取失敗：{e}")
            break

        prods = data.get("prods", [])
        if not prods:
            print(f"[資訊] 第 {page} 頁沒有資料，停止")
            break

        for item in prods:
            name  = item.get("name", "").strip()
            price = item.get("price", None)
            brand = item.get("brand", "")
            pid   = item.get("Id", "")

            if name and price:
                results.append({
                    "日期":   today,
                    "商品名稱": name,
                    "品牌":   brand,
                    "價格":   int(price),
                    "商品ID": pid,
                    "關鍵字": keyword,
                })

        print(f"[完成] 第 {page} 頁，共抓到 {len(prods)} 筆")
        time.sleep(1)  # 每頁間隔 1 秒，避免被封鎖

    return results


def save_to_csv(data, filename):
    """將資料存成 CSV，如果檔案已存在就 append（不重複寫標題）"""
    df_new = pd.DataFrame(data)

    try:
        df_exist = pd.read_csv(filename, encoding="utf-8-sig")
        df_all = pd.concat([df_exist, df_new], ignore_index=True)
        # 去除同一天同商品的重複資料
        df_all = df_all.drop_duplicates(subset=["日期", "商品ID"])
        print(f"[資訊] 合併後共 {len(df_all)} 筆資料")
    except FileNotFoundError:
        df_all = df_new
        print(f"[資訊] 建立新檔案，共 {len(df_all)} 筆資料")

    df_all.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"[儲存] 已存至 {filename}")
    return df_all


def show_summary(df):
    """印出簡單的統計摘要"""
    print("\n──────────────────────────────")
    print(f"  關鍵字：{KEYWORD}")
    print(f"  總商品數：{len(df)}")
    print(f"  最低價：NT$ {df['價格'].min():,}")
    print(f"  最高價：NT$ {df['價格'].max():,}")
    print(f"  平均價：NT$ {df['價格'].mean():,.0f}")
    print("──────────────────────────────")
    print("\n最便宜 5 筆：")
    cheap = df.nsmallest(5, "價格")[["商品名稱", "價格"]]
    for _, row in cheap.iterrows():
        name = row["商品名稱"][:30] + "…" if len(row["商品名稱"]) > 30 else row["商品名稱"]
        print(f"  NT$ {row['價格']:>6,}  {name}")


if __name__ == "__main__":
    print(f"開始抓取「{KEYWORD}」的價格資料...\n")

    data = scrape_pchome(KEYWORD, MAX_PAGES)

    if not data:
        print("沒有抓到任何資料，請檢查網路或關鍵字")
    else:
        df = save_to_csv(data, OUTPUT_FILE)
        show_summary(df)
        print(f"\n完成！開啟 {OUTPUT_FILE} 查看完整資料")
