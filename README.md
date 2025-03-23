# 📝 YouTube Transcript Extractor for NotebookLM 🧠

This application extracts transcripts from YouTube videos and playlists, optimized specifically for uploading to NotebookLM! 🚀

## ✨ Features

- 🎬 Extract transcripts from individual YouTube videos
- 📋 Extract transcripts from entire YouTube playlists
- 📊 Smart file splitting to meet NotebookLM's 500,000 word limit per file
- 💾 Clean, formatted output ready for direct upload

## 🔍 Why This Works Great with NotebookLM

- ✅ Automatically splits files at 500,000 words (NotebookLM's per-file limit)
- ✅ Removes unnecessary line breaks for better processing
- ✅ Creates clean, well-formatted text that NotebookLM can easily analyze
- ✅ Organizes content with clear video separators for better context

## 🛠️ Requirements

- Python 3.6+
- Required packages:
  - youtube_transcript_api
  - google-api-python-client
  - requests

## 🚀 Getting Started

1. Install required packages:
```bash
pip install youtube_transcript_api google-api-python-client requests