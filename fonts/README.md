# フォント

このディレクトリに日本語フォントを配置してください。

## 推奨フォント

### IPAex フォント（同梱済み）

本ディレクトリに以下の IPAex フォントを同梱しています。追加のダウンロードは不要です。

- `ipaexg.ttf` (IPAexゴシック - 見出し用)
- `ipaexm.ttf` (IPAex明朝 - 本文用)

これらのフォントは [IPAフォントライセンス v1.0](https://moji.or.jp/ipafont/license/) に従って再配布しています。

### Noto Sans JP / Noto Serif JP

1. https://fonts.google.com/noto/specimen/Noto+Sans+JP からダウンロード
2. 以下のファイルをこのディレクトリに配置:
   - `NotoSansJP-Regular.ttf`
   - `NotoSansJP-Bold.ttf`

## 使い方

```bash
python -m jb_workhistory sample/data.yaml -o output.pdf --font-dir ./fonts
```
