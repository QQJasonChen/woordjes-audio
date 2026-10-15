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

## 正常語速規則（2026-10-15）

未來生成原音一律明確傳入 **`speed: 1.0`**，不得省略或要求「稍慢」。文字使用原始完整例句，不加 `[slowly]` 或任何語速／情緒標記。速度選擇交給 App 播放器，支援時保持音高。固定的生成條件見 `generation-contract.json`。

本次只重做曾用 0.85／0.9 的 A1／A2 例句：1,443 個 key、1,439 句不同文字，其中 1 句沿用 QQ 已聽過的 1.0 A／B 範例，新增生成 1,438 句。其餘 5,871 個正常例句 key、全部單字音檔與 B1 以上音檔保留。

驗證必須同時核對原生工具實際參數、實際模型、`alignment.characters` 與 `normalized_alignment.characters`，兩者逐字等於原句才可接受；只看請求或 `gen_config` 不足。保存的私人原生回應可用離線檢查器驗證：

```sh
python3 tools/check_generation.py --expected /private/path/expected.json --messages /private/path/messages.json
```

此檢查器不呼叫 API、不生成、不上傳；輸入不可放入公開 repo。發布前另驗 MP3 完整解碼、內容 SHA 與未修改範圍。提交結果未知時先找回原工作，成功的結果重用，不能直接重送付費請求。技術檢查不代表逐句真人發音驗收。
