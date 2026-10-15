# woordjes-audio

荷蘭文單字 App「Woordjes」的發音音檔 CDN（GitHub Pages）。

- `audio/w_<id>.mp3`：單字發音。
- `audio/e_<id>.mp3`、`e2_`…`e5_`：例句發音。
- A1／A2 現有例句：共 7,314 個 MP3 音檔 key，經 YouMind 生成，實際模型為 `eleven_v4`，聲線為 `EkK5I93UQWFDigLMpZcX`，語言為 `nl-NL`。
- 單字發音及 B1 以上例句保留原檔；其聲線與編碼沿用既有內容。

App 端組法：`<AUDIO_BASE>audio/<kind>_<id>.mp3`。
`AUDIO_BASE = https://qqjasonchen.github.io/woordjes-audio/`，結尾需有斜線。

本次只替換 A1／A2 已存在的例句音檔，保留原本的檔名、卡片 ID、例句與中文。App 使用的音檔路徑不變。

公開的 `audio-refresh-manifest.json` 提供 key、文字 SHA、音檔 SHA、生成服務／模型／聲線與生成證據指紋，不包含例句全文、中文翻譯、帳號、chat ID 或原始 API 紀錄。完整來源與回復包保留於私人工作區。

既有 VocalLab 腳本與舊 manifest 仍是歷史生成紀錄，不能代表本次 A1／A2 音檔的生成狀態。後續重生需依明確 key 清單與最新 manifest 進行，避免全牌組腳本覆寫本次更新。配音範圍與歷史進度見 `VOICE_STATUS.md`。
