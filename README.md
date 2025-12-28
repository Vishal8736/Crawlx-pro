# Crawlx-pro

cat << 'EOF' > README.md
# 🛡️ CrawlX-Pro 
### **Developed by: Vishal ❤️ Subhi**

**CrawlX-Pro** is a high-performance automation suite designed for reconnaissance. It combines multi-source subdomain enumeration with deep archive crawling.

---

## ✨ Key Features
* **Multi-Engine Discovery:** Queries `crt.sh` (SSL Logs) and `AlienVault OTX` (Passive DNS) simultaneously.
* **Smart Concurrency:** Built with Python threads for rapid execution.
* **Auto-Sanitization:** Automatically strips wildcards (`*.`) and filters duplicate entries.
* **Seamless Integration:** Direct handoff to `wayback_urls_deep.sh` for immediate URL discovery after finding subdomains.
* **Professional UI:** Featuring the **Vishal ❤️ Subhi** signature and clean terminal output.

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3 and `requests` installed:
```bash
pip install requests


chmod +x crawlx-pro.py
chmod +x wayback_urls_deep.sh


python3 crawlx-pro.py -d example.com


python3 crawlx-pro.py -i list.txt
