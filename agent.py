import feedparser
import anthropic
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

# ═══════════════════════════════════════
# কনফিগারেশন
# ═══════════════════════════════════════
ANTHROPIC_API_KEY = "your-api-key-here"  # তোমার Claude API key
FEED_URL = "https://www.aljazeera.com/xml/rss/all.xml"
MAX_NEWS = 5  # কতটা নিউজ দেখাবে

console = Console()

# ═══════════════════════════════════════
# ধাপ ১: RSS থেকে নিউজ আনো
# ═══════════════════════════════════════
def fetch_news(feed_url: str, limit: int = 5) -> list[dict]:
    console.print("\n[bold cyan]📡 Al Jazeera থেকে নিউজ আনা হচ্ছে...[/bold cyan]")
    
    feed = feedparser.parse(feed_url)
    news_list = []
    
    for entry in feed.entries[:limit]:
        news_list.append({
            "title": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
        })
    
    console.print(f"[green]✅ {len(news_list)}টি নিউজ পাওয়া গেছে[/green]")
    return news_list


# ═══════════════════════════════════════
# ধাপ ২: Claude দিয়ে বাংলায় Summary
# ═══════════════════════════════════════
def summarize_in_bangla(news: dict, client: anthropic.Anthropic) -> str:
    prompt = f"""তুমি একজন বাংলাদেশী সংবাদ সম্পাদক।

নিচের ইংরেজি নিউজটি পড়ো এবং বাংলায় সংক্ষিপ্ত summary লেখো।

নিউজ শিরোনাম: {news['title']}
নিউজ বিবরণ: {news['summary']}

তোমার কাজ:
১. বাংলায় একটি আকর্ষণীয় শিরোনাম লেখো (১ লাইন)
২. ৩-৪ বাক্যে সহজ বাংলায় summary লেখো
৩. একটি গুরুত্বপূর্ণ তথ্য বা বিশ্লেষণ যোগ করো

শুধু বাংলায় লেখো। কোনো ইংরেজি ব্যাখ্যা দিও না।"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text


# ═══════════════════════════════════════
# ধাপ ৩: সুন্দরভাবে দেখাও
# ═══════════════════════════════════════
def display_news(news: dict, bangla_summary: str, index: int):
    console.print()
    
    # Original title
    console.print(Panel(
        f"[bold yellow]🌐 মূল শিরোনাম:[/bold yellow]\n{news['title']}\n\n"
        f"[bold green]🇧🇩 বাংলা Summary:[/bold green]\n{bangla_summary}\n\n"
        f"[dim]🔗 {news['link']}[/dim]",
        title=f"[bold red]📰 নিউজ #{index}[/bold red]",
        border_style="blue",
        padding=(1, 2)
    ))


# ═══════════════════════════════════════
# মূল Agent
# ═══════════════════════════════════════
def run_agent():
    console.print(Panel(
        "[bold red]📡 News Summary Agent[/bold red]\n"
        "[dim]Al Jazeera → বাংলা Summary[/dim]",
        border_style="red",
        padding=(1, 4)
    ))

    # Claude client
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # নিউজ আনো
    news_list = fetch_news(FEED_URL, MAX_NEWS)

    # প্রতিটা নিউজ summary করো
    console.print(f"\n[bold cyan]🤖 Claude AI দিয়ে বাংলায় অনুবাদ হচ্ছে...[/bold cyan]")
    
    for i, news in enumerate(news_list, 1):
        console.print(f"\n[yellow]⏳ নিউজ {i}/{len(news_list)} প্রক্রিয়া হচ্ছে...[/yellow]")
        
        try:
            bangla_summary = summarize_in_bangla(news, client)
            display_news(news, bangla_summary, i)
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")

    console.print(Panel(
        "[bold green]✅ সব নিউজ summary সম্পন্ন![/bold green]",
        border_style="green"
    ))


# ═══════════════════════════════════════
# চালাও
# ═══════════════════════════════════════
if __name__ == "__main__":
    run_agent()
