# 📡 News Summary Agent

Al Jazeera থেকে নিউজ এনে Claude AI দিয়ে বাংলায় summary দেয়।

## ইনস্টল করো

```bash
pip install -r requirements.txt
```

## Claude API Key পাবে কোথায়?

1. console.anthropic.com → Login
2. API Keys → Create Key
3. agent.py ফাইলে এই লাইনে key বসাও:
   ```python
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```

## চালাও

```bash
python agent.py
```

## কাস্টমাইজ করো

agent.py ফাইলে:
- `MAX_NEWS = 5` → কতটা নিউজ দেখাবে
- `FEED_URL` → অন্য RSS feed দিতে পারো
