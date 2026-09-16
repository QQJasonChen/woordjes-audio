# woordjes-audio

荷蘭文單字 App「Woordjes」的發音音檔 CDN（GitHub Pages）。

- `audio/w_<id>.mp3`　單字發音（128 kbps）
- `audio/e_<id>.mp3`、`e2_`…`e5_`　例句發音（32 kbps）

App 端組法：`<AUDIO_BASE>audio/<kind>_<id>.mp3`，
`AUDIO_BASE = https://qqjasonchen.github.io/woordjes-audio/`（結尾要有斜線）。

跟 `tango-audio` 同一套做法：把音檔搬出 App，App 本體才不會幾百 MB。
重生音檔請用 `~/telegram-dutch/multilang/gen_audio_say_nl_paid.py`（付費層）
與 `gen_audio_*`（免費層），生完再整批複製進 `audio/`。
