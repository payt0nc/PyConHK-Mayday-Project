# HK Mayday Ticket Bot

Current Version: 0.3.2

<img src="https://dcepcmzwvvlke.cloudfront.net/hkmaydaybot.JPG" width="400">

## Acknowledgements

#### [五谷 (五月天香港歌迷會)](https://www.facebook.com/hkmayday)

#### 懶人包作者：W.S. Ho

#### QA: F.WONG, B.CHAN

## Dependencies
Infra:

1. MongoDB
2. Redis
3. Python3.5

Python Lib:
> see requirements
## Updates

### Version 0.3.2
1. 增加Command
 - /start - 啟動程式
 - /help - 召喚懶人包
 - /menu - 回到主選單
 - /done - 結束程式

### Version 0.3.1
1. 重新修改Validator
 - 不再檢查入閘口
 - 新增段數(Section)取代閘口

### Version 0.3.0
1. 增加Redis
 - 存儲每個人錄入的Record

### Version 0.2.4
1. 修改個別中文字眼
2. 更新inline command
 - 增加/done 完結整個Bot
 - 增加/help 召喚懶人包

### Version 0.2.3
1. 增加'聯絡對方'的功能
 - 可以按照票據編號將信息通過Bot轉寄至對方
 - 對方收到消息 可以同過@直接發起雙方的對話 （前提：買方(即係搵飛的朋友)需要註冊telegram的username）
2. 座位號不再作詳細檢查 只保留檢查有沒有填寫
3. Typo修正

### Version 0.2.0
1. Main Panel: 新增‘搵門票’ 然後將原來的‘原價轉讓, 換票’放響搵門票後面
2. 票據狀態改為門票狀態
3. 門票紀錄回覆 改為 只回傳門票ID