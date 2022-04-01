## Promotion Calculator
1. 請使用你熟悉的語言(我們使用 Ruby,但你可以選用你擅⻑的語言),實作一個結
帳金額計算機。其中會有各種商品優惠的折扣邏輯,並計算出最後的原始金額、折扣金額、實付金額。
至少需實作 Promotion, Order, Product, User, Calculator,等 5 個 class,可視需
要實做其他 Class, 不用定義太細的欄位(例如 User 只要定義有 user_id 即可),只需要定義足以完成規格的欄位。
需根據規格撰寫單元測試,保證以下的情境都可以正確計算。
* 訂單滿 X 元折 Z %
* 特定商品滿 X 件折 Y 元
* 訂單滿 X 元贈送特定商品
* 訂單滿 X 元折 Y 元,此折扣在全站總共只能套用 N 次
* (加分題)訂單滿 X 元折 Z %,折扣每人只能總共優惠 N 元
* (加分題)訂單滿 X 元折 Y 元,此折扣在全站每個月折扣上限為 N 元
### Directory Structure
```
├── models
    ├── promotion            
        ├── __init__.py      # Promotion class
        ├── action.py
        ├── rule.py
    ├── __init__.py
    ├── calculator.py        # Calculator class
    ├── order.py             # Order class
    ├── product.py           # Product class
    ├── user.py              # User class
└── main.py                  # main test file
```
### Test
`python test.py`
## Park lots payment system
2. 請以要向其他工程師說明架構的場合,畫出系統架構圖。設計一個能夠高可用、高併發,處理停車場結帳付款的系統。
可使用各種雲端服務搭建。
若覺得架構圖不易表達,可輔以文字說明。
```
舉例來說,付款可能發生各種異常:網路不順、金流方較慢或噴錯(例如回 5XX)、信用卡失效。
不能發生少收錢、多收錢的狀況,沒收到的必須要之後可以再次執行。
```
## Park lots backend system
3. 請以要向其他工程師說明架構的場合,畫出系統架構圖。設計一個提供停車場站資料
給全台灣大量用戶使用的系統架構。請以提供給使用者日常行車使用的情境去考慮。
可使用各種雲端服務搭建。
若覺得架構圖不易表達,可輔以文字說明。
```
停車場站可提供的資料有:名稱、地址、經緯度、目前空位。
請考慮空位資料變更頻率不固定且頻繁變更。
```