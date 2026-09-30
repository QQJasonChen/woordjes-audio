# 配音狀態（更新時一併改這裡）

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
