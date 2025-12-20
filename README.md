# A Neuro-Semantic Framework for Multi-Modal Narrative Immersion 

> **🎉 整合版本：** AI-Reader 與 ModernReader 已整合！現在前端 UI 和後端引擎都在同一個專案中。

## 專案願景 
故事的核心在於體驗，而非僅是文字。數百年來，我們透過視覺解碼符號來理解故事，但文字本身僅是通往故事世界的媒介。

Project H.O.L.O. 的使命，就是打破這個媒介的限制，提出一個大膽的問題：如果我們不僅能"閱讀"故事，而是能真正地"感受"它呢？ 

## 專案目標 
- 重新定義"閱讀"的體驗，讓讀者不僅僅是解讀文字，而是全方位感受故事中的情感與情境，成為故事的一部分。 

## 核心技術 
1. **深度語意分析**：
   - 使用自然語言處理 (NLP) 技術，將文本解構為語意單元。
   - 分析情感、語調、角色關係與故事背景。

2. **生成式 AI**：
   - 基於語意單元創建動態的聽覺體驗（例如角色對話、環境音效）。
   - 使用文本到聲音 (Text-to-Sound) 與文本到氣味 (Text-to-Scent) 的生成技術，模擬多感官回饋。

3. **多模態感知系統**：
   - 整合聽覺、觸覺與嗅覺回饋，打造沉浸式的敘事體驗。
   - 開發 API 供硬體設備（如觸覺反饋裝置）使用。

## 專案架構

```
AI-Reader/
├── web/
│   ├── frontend/          # React 前端應用 (整合 ModernReader UI)
│   │   ├── src/
│   │   │   ├── components/  # React 組件
│   │   │   │   ├── Header.jsx
│   │   │   │   ├── HeroSection.jsx
│   │   │   │   ├── VisionSection.jsx
│   │   │   │   ├── ScenariosSection.jsx
│   │   │   │   ├── InteractiveDemo.jsx
│   │   │   │   ├── EngineSection.jsx
│   │   │   │   ├── ProgressSection.jsx
│   │   │   │   ├── FutureSection.jsx
│   │   │   │   └── Footer.jsx
│   │   │   └── App.jsx
│   │   └── package.json
│   └── backend/           # FastAPI 後端
│       └── main.py
├── holo/                  # 核心 Python 模組
│   ├── ingestion/         # 文本分段處理
│   ├── auditory/          # TTS 語音合成
│   └── sensory/           # 觸覺回饋模擬
└── tests/                 # 測試檔案
```

## 快速開始

### 前端開發

```bash
cd web/frontend
npm install
npm run dev
```

### 後端開發

```bash
cd web/backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## 主要功能

### 🎨 現代化 UI (來自 ModernReader)
- **多輸入方式**：文字輸入、書籍封面/ISBN 掃描、臉部情緒辨識
- **互動式演示**：HSP 引擎可視化、感官回饋模擬
- **響應式設計**：支援桌面和移動設備

### 🔊 多模態輸出
- **聽覺輸出**：TTS 語音合成，支援多種語言
- **觸覺回饋**：觸覺模式生成（心跳、脈衝、震動等）
- **知識圖譜**：文本分段與語意分析

## 預期成果 
- 一個沉浸式敘事框架，能夠將任何文本轉化為多感官體驗。
- 支援多語言，應用於教育、娛樂與療癒場景。 

## 版權與貢獻 
歡迎對此專案感興趣的開發者提供意見並提交 PR.


---

## 🤖 開發說明

**本專案使用 AI 輔助開發工具**

本專案在開發過程中使用了以下 AI 輔助工具，以提升開發效率和代碼質量：

- **GitHub Copilot**: 用於代碼補全、函數生成和重構建議
- **Google Labs Jules**: 協助專案架構設計和技術文檔撰寫

這些工具在開發過程中提供了寶貴的輔助，但所有最終決策、架構設計和代碼審查均由開發者本人完成。使用 AI 工具是為了：

✨ 加速開發流程  
📚 學習最佳實踐  
🔍 提高代碼質量  
🚀 專注於創新功能實現  

我們相信透明地披露 AI 工具的使用，有助於推動學術界和工業界對 AI 輔助開發的理解與規範。
