# フォント

このディレクトリに日本語フォントを配置してください。

## 推奨フォント

### IPAex フォント（推奨）

1. https://moji.or.jp/ipafont/ipaex00401/ からダウンロード
2. 以下のファイルをこのディレクトリに配置:
   - `ipaexg.ttf` (IPAexゴシック - 見出し用)
   - `ipaexm.ttf` (IPAex明朝 - 本文用)

### Noto Sans JP / Noto Serif JP

1. https://fonts.google.com/noto/specimen/Noto+Sans+JP からダウンロード
2. 以下のファイルをこのディレクトリに配置:
   - `NotoSansJP-Regular.ttf`
   - `NotoSansJP-Bold.ttf`

## 使い方

```bash
python -m jpcv sample/data.yaml -o output.pdf --font-dir ./fonts
```
