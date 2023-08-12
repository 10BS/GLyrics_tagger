Genius Lyrics Tagger
======
Lyrics downloader and tagger for Genius

Requirements
---
* Python 3.11
* lyricsgenius
* mutagen

Before run
---
1. Copy music folder link
2. Get Genius API key:
  2.1. Goto https://docs.genius.com/
  2.2. Click "Authorize With Genius" in top section "These Docs are a Genius App"
  2.3. After logining, see next section "Resources". Your API key is text after "Authorization: Bearer". Copy it

Run
---
1. `pip install -r requirements.txt`
2. `python main.py`
3. Paste folder link into "Audio folder: "
4. Paste API key into "Genius API token: "
5. Wait
