# 配音狀態（更新時一併改這裡）

| 範圍 | 聲音 | 說明 |
|---|---|---|
| 免費層 id < 2000 | 既有 | 未動 |
| 付費層 **id 2000–7348** 的 `w_` 與 `e_` | **VocalLab `Lore`**（Dutch Calm Female Narration, v-flash） | 2026-09-18 完成 |
| 付費層 **id 7349–8999** 的 `w_` 與 `e_` | macOS `Xander` | **待補**，VocalLab 點數用盡 |
| 付費層全部 `e2_`–`e5_`（6,990 段） | macOS `Xander` | 待補 |

## 續跑（下個月儲值後）
```bash
cd ~/telegram-dutch
python3 multilang/gen_audio_nl_vocallab.py --fields nl,ex --dry-run   # 先看還差多少點
python3 multilang/gen_audio_nl_vocallab.py --fields nl,ex
```
manifest 在 `~/telegram-dutch/multilang/nl_audio_vocallab_manifest.json`，
**已生成的不會重花點數**，直接接著跑。

## 成本：用實測值，不要用字元換算
2026-09-18 實測：**3.39 點／段**（36,241 點 ÷ 10,696 段）。

當初用「字元 ÷ 15 × 0.75」估成 1.34 點／段，**低估 2.5 倍**，跑到 76% 就沒點數。
原因是單價不只看內容長度，**每次請求還有約 1.1 點的固定開銷**——
對單字特別致命（一個字才 1.2 秒，開銷比內容還貴）。10,696 次請求光開銷就吃掉約 11,000 點。

剩下的量與估價：
- `nl,ex` 未完成 3,299 段 → 約 **11,200 點**
- `e2..e5` 全部 6,990 段（句子較長，單價會高一些）→ 約 **24,000 點**
