# 配音狀態

## A1／A2 例句更新

本次更新涵蓋 2,188 張 A1／A2 卡片原本就有的例句，共 7,314 個音檔 key：A1 2,290 段、A2 5,024 段。相同全文共用已驗證的生成結果，共 7,301 段不同的例句文字。

| 範圍 | 本次狀態 |
|---|---|
| A1／A2 的現有 `e_`、`e2_`–`e5_` | YouMind；實際模型 `eleven_v4`；聲線 `EkK5I93UQWFDigLMpZcX`；`nl-NL` |
| 全部 `w_` 單字音檔 | 保留原檔 |
| B1 以上例句 | 保留原檔 |
| 例句、中文與卡片 ID | 保留原內容 |

範圍以卡片 CEFR 及明確 key 清單判定，不能用免費／付費層或 ID 大小推斷。公開 `audio-refresh-manifest.json` 記錄各 key 的文字與音檔 SHA、模型／聲線及生成證據指紋；完整原生工具回應與回復包保留於私人工作區，不隨公開音檔發布。

技術驗證涵蓋全部 key、原生生成 metadata、SHA 及 MP3 完整解碼。這些檢查不代表全部例句皆經真人逐句聽審，也不代表使用者裝置已重新抓取最新音檔。人耳發音驗收與實機快取確認須分別記錄。

以下保留 2026-09-30 的歷史配音與成本紀錄。當中的全牌組 Lore 規則、待辦段數、聲線分布及 VocalLab 點數，只代表當時狀態；A1／A2 例句以本次 manifest 為準。

---

## 2026-09-30 歷史紀錄

**2026-09-30 起的規則（QQ）：VocalLab 一律用最高階 `v-studio`，全牌組統一 Lore。**
之前 id 2000–7348 用的是 `v-flash`，也要換掉。

| 範圍 | `w_` 單字 | `e_` 例句1 | `e2_`–`e5_` |
|---|---|---|---|
| 免費層 id < 2000 | ✅ Lore v-studio（1,992） | ✅ Lore v-studio（1,947） | e2 521 段已換；其餘 **OpenAI nova**（e2 1,463／e3 1,913／e4 1,837／e5 1,829） |
| 付費層 2000–7348 | ✅ Lore v-studio（5,349） | Lore **v-flash**（5,347）＋1 段 Xander | e2 **macOS Xander**（5,340） |
| 付費層 7349–8999 | ✅ Lore v-studio（1,651） | ✅ Lore v-studio（1,650） | e2 **macOS Xander**（1,650） |

2026-09-30 全量掃描（ffmpeg 時長＋音量）：32,575 個 App 會要求的檔案全部存在，0 個無聲/截斷檔。

## 還沒做完的（依優先序）
| 項目 | 段數 | 估點數（ceil(字元/15)） |
|---|---:|---:|
| 付費層 e_ 2000–7348（v-flash → v-studio） | 5,348 | ~18,000 |
| 免費層 e2–e5（nova → Lore） | 7,042 | ~22,400 |
| 付費層 e2 全部（Xander → Lore） | 6,990 | ~24,700 |
| **合計** | **19,380** | **~65,200** |

## 續跑
```bash
cd ~/telegram-dutch
python3 multilang/gen_audio_nl_vocallab.py --fields nl,ex,ex2,ex3,ex4,ex5 --dry-run
# 或照優先序給 key 清單（一行一個 key）：
python3 multilang/gen_audio_nl_vocallab.py --keys-file keys.txt --floor 5000
```
- manifest：`~/telegram-dutch/multilang/nl_audio_vocallab_manifest.json`，簽章＝md5(`Lore|v-studio|<文字>`)，
  已生成且文字沒變的不會重花點數；例句文字改過會自動重生。
- 每次請求實際扣點記在 `multilang/nl_audio_vocallab_points.jsonl`（API 回應的 `points_used`）。
  **同帳號有別的 agent 在花，別用餘額相減算成本。**
- `--floor`：帳號餘額低於此值就停（每 200 段檢查一次，一段最多約 4 點，留 ~800 點緩衝）。
- 生成後自動擋「太短或近乎無聲」的回傳（< 0.4 秒單字／< 0.8 秒例句、或 max_volume < -30 dB）會重試。

## 成本：以 API 回傳的 points_used 為準
2026-09-29/30 實測 v-studio：**每段就是 ceil(字元數/15) 點，沒有固定開銷**
（13,249 次請求共 22,316 點；單字幾乎都是 1 點，例句 3–4 點）。
09-18 記錄的「3.39 點／段、每請求 1.1 點固定開銷」是用餘額相減算的，
當時同帳號有其他工作在跑，數字被汙染了——別再用。