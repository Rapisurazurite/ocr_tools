# OCR工具



## 文字OCR
使用百度OCR接口，需要申请，每天有一定免费额度。
```python
class BaiduOCR:
    def __init__(self):
        self.AppID = "******************"
        self.AK = "*******************"
        self.SK = "********************"
```
将tools\OCR.py里的***替换成自己的AppID,AK,SK

## 公式OCR
目前有两种，使用mathpix接口，以及使用必应的免费接口。

区别主要是mathpix接口的结果更加精确，但是每天有一定的免费额度，超出部分要购买。
bing的免费提供，但是准确率不如mathpix高，而且OCR的图片里面包含文字（中文），会导致bing的接口报错。

- 使用mathpix接口
  ```python
      def matpix_ocr(image_src: str, timeout=30) -> Tuple[int, Any]:
        url = 'https://api.mathpix.com/v1/snips'
        headers = {'Host': 'api.mathpix.com',
                   'Authorization': '*********************************************',
                   }
        payload = {
            "metadata": {
                "user_id": "******************************"},
            "src": image_src
        }
    ```

  将mathpix的API key替换成自己的Authorization, user_id替换成自己的。
- 使用bing的API
    无需修改，直接调用即可。
  
### 手写OCR
与百度接口一致,替换tools\OCR.py里的

```
```python
class BaiduHandWritingOCR:
    AppID = "******"
    AK = "******************"
    SK = "******************"
```

## Latex公式快捷输入
可选，如果不需要将main.py中的 `LaTexHelper.add_abbreviation()`注释掉即可。
替换的列表在replace_table.csv里。

## 翻译功能（去除）
由于此功能需要UI，写在了QT里面。现在删掉了，精简了代码。

# 使用
运行后选择使用的OCR引擎，alt+z进行文字OCR，alt+q进行公式（手写）OCR。
若开启Latex公式快捷输入，则输入 \frac 会替换为 \frac{}{}。