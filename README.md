# 台灣電商價格追蹤器 | Taiwan E-commerce Price Tracker

自動抓取 PChome 商品價格並分析趨勢的 Python 工具。  
A Python tool that automatically scrapes PChome product prices and analyzes trends.

---

## 功能 | Features

- 自動爬取指定關鍵字的商品名稱與價格
- 每次執行自動 append 新資料，不會覆蓋舊紀錄
- 去除重複資料，保持資料乾淨
- 執行後顯示最低價、最高價、平均價摘要
- 輸出 CSV 方便後續用 Excel 或 Python 分析

---

## 使用技術 | Tech Stack

- Python 3.11
- `requests` + `BeautifulSoup4` — 網頁爬蟲
- `Pandas` — 資料清理與分析
- `SQLite`（開發中）— 資料儲存

---

## 如何使用 | Getting Started

**1. 安裝套件**
```bash
pip install requests beautifulsoup4 pandas
```

**2. 執行爬蟲**
```bash
python scraper.py
```

**3. 修改關鍵字**  
打開 `scraper.py`，修改最上方設定區：
```python
KEYWORD = "藍牙耳機"   # 換成你想追蹤的商品
MAX_PAGES = 3          # 抓幾頁（每頁約 20 筆）
```

---

## 輸出範例 | Sample Output

```
[完成] 第 1 頁，共抓到 20 筆
[完成] 第 2 頁，共抓到 20 筆

──────────────────────────────
  關鍵字：藍牙耳機
  總商品數：40
  最低價：NT$ 299
  最高價：NT$ 12,800
  平均價：NT$ 2,340
──────────────────────────────
```

---

## 開發計畫 | Roadmap

- [x] PChome 爬蟲基礎版
- [ ] 存入 SQLite 資料庫
- [ ] 價格趨勢視覺化（Plotly）
- [ ] 降價自動通知（Line Notify）
- [ ] Streamlit Dashboard 網頁版

---

## 作者 | Author

Jerry Chung — 歡迎合作接案，資料爬蟲、自動化、報表分析皆可承接。  
Open to freelance projects: web scraping, automation, data analysis.

📧 聯絡請至 GitHub Issues 或私訊或 email:jerrycnchung@gmail.com
