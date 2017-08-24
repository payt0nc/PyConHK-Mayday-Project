'''
Created on 8 Mar 2017

@author: Comma
'''


class Conversations(object):
    '''
    classdocs
    '''
    TYPE_IN_CORRECT = 'Bingo! 全中'
    TYPE_IN_ERROR = '輸入錯誤，請重新輸入\n'
    TYPE_IN_WARNING = '瑪莎說：這樣不行哦\n%s'

    def __init__(self):
        '''
        To state every stage conversation
        '''

        self._keywords_mapping = {
            '類別': 'Collection',
            '日期': 'Date',
            '價錢': 'Price',
            '數量': 'Quantity',
            '門票狀態': 'Status',
            '段數': 'Section',
            '行數': 'Row',
            '座位號': 'Seat',
            '備註': 'Remarks'
        }

        self._ticket_type_mapping = {
            '原價轉讓': 'Sell',
            '換飛': 'Exchange'
        }

    def get_keywords(self, keyword):
        return self._keywords_mapping.get(keyword)

    def get_ticket_type(self, ticket_type):
        return self._ticket_type_mapping.get(ticket_type)


class AdminPanel(Conversations):
    BACK_TO_MAIN_PANEL = '現在返回主選單'
    CONFIRM = '確認送出?'
    SENT = '已經送出 {n} 個信息'
    MESSAGE = '你想傳達的信息:\n%s'
    NOTICE_CAPTION = '''
關於香港分公司的一些些小事，希望大家能share出去。另更多的同事知道。
'''

    DOKODEMO = '''
在「文字失效」的瞬間，只需一個動作勝過千言萬語。
雖然香港場沒有「北京鳥巢」10萬人的震撼、也沒有「高雄世運」懾人的舞台效果.....但香港永遠是五月天最溫暖的「另一個家」。

不管你是坐在接待處、辦公室、會議室還是茶水間的同事，邀請大家一起加入。讓我們再創造一個與五月天的「專屬語言」吧!❤
'''

    DOKODEMO_CAPTION = '''
請瘋狂 like & share & tag 所有將會上班的同事吧！(團結） — ￼覺得係時候喇。
'''


class MainPanel(Conversations):
    ADMIN_PANEL = '開啟Admin模式'
    START = 'Hello @%s 有咩可以幫到你?\n即時平臺統計: http://bit.ly/2q3JHn6'
    DONE = '五月之約 紅館見!\n之後你 /start 就可以再次召喚我\n'
    USERNAME_MISSING = '你未填Username喔...\n入Setting選擇Username就可以填\n否則對方就冇辦法搵到你'
    REMINDER = '''
除各認可單位收取的手續費(建議賣家提供收據或其他證明)外，只接受原價放售。
如發現黃牛，請盡公民義務舉報警方，及將證據Send到 @hk_mayday 舉報下架。
請各五迷小心交易，本telegram只提供平台(非官方)配對買賣雙方，買賣方的爭議或任何人士如遭受損失，本平台及開發者概不負責。
    '''
    YELLOWCOW = '根據記錄，你被舉報為黃牛。本平台不能再為你提供服務。bye～'
    SOS = '''
使用說明(懶人包)
－ 無票五迷搵門票:
http://bit.ly/maydaylazypkg1

－ 有票五迷換門票:
http://bit.ly/maydaylazypkg2

－ 有票五迷原價讓票:
http://bit.ly/maydaylazypkg3

－ 如果你發現本平台有黃牛：
請盡公民義務舉報警方，及將證據send到 @hk_mayday

－ 黃牛統計:
收集: https://goo.gl/P1RhKv
統計: https://goo.gl/v676c1

－ 即時平臺統計:
http://bit.ly/2q3JHn6

/start 開始使用'''


class PairUp(Conversations):
    CONFIRM = '確認送出?'
    MESSAGE = '你想傳達的信息:\n%s'
    MSG_FROM = ' 來自 @'
    NEW_MSG = '你有新信息%s'
    REMINDER = '溫馨提示：請註明你所想要的門票信息，並留下Telegram以外的聯絡方式自行聯絡交易。\n若發現對方為黃牛，請截圖保存並向 @hk_mayday 舉報。'
    RESET = '請重新輸入你想傳達的信息'
    SENT = '已經送出\n有咩可以幫到你?'
    START = '請輸入你想給對方的說話，例如：「Hi! 我想換/買你$xxx的門票」，我會幫你於telegram轉達，然後你們可私下聯絡了。'
    NAME_MISSING = '我都未知點稱呼你\n或者你在Telegram的Settings註冊咗你個username先啊?\n我會等你(不要走～請不要走~)'


class PostTickets(Conversations):
    START = '如果你想擺張票上來，記得填曬下面全部的項目'
    INFO = '%s係?'
    INTO_DB = '你張門票已經畀紀錄\n ID: %s\n哩個ID係證明張門票屬於你 小心保管'
    SECTION = '紅閘: 43-49\n藍閘: 50-59\n綠閘: 60-67\n段數係?'
    RECEVIED_INFO = '你手上張票係%s'
    RESET = '重置完成'
    EXISTED = '門票已經存在 請不要重複提交'
    ERROR = '系統錯誤 請稍後再試'


class SearchTickets(Conversations):
    AGAIN = '使唔使搵多次?'
    START = '門票的類型係?'
    CONDITION = '話畀我知你想要咩門票,介紹返'
    CHOICE = '按%s來搵'
    WITH_TICKETS = '我地搵到以下門票：\n%s'
    WITHOUT_TICKETS = '暫時冇喔～不如改一改你要搵嘅條件?'


class SupportEvents(Conversations):
    LIST_EVENTS = '''
目前所知的應援活動：
523上班餘興節目
《五月之約》尋回專屬HOME KONG場的感動
'''
    EVENTS_523 = '''
[轉發] 523 節目
https://www.facebook.com/523HKLifeTour/
'''
    EVENT_HOME_KONG = '''
[轉發] 《五月之約》尋回專屬HOME KONG場的感動
2006年的五月，
台上只有五月天，
台下只有熱愛他們的歌迷，
還有汗水、淚水、呼喊聲
交織著無數的感動與熱情。

讓我們一起找回最初的感動，
這是專屬香港的五月。

https://www.facebook.com/events/401155273603140/
'''
    EVENT_HOME_KONG_CREDIT = '圖片來源：《五月之約》尋回專屬Home Kong場的感動 (by May)'
    EVENT_BACK = '''
可選擇介紹其他應援活動
/menu 回主選單
/done 結束程式
'''


class UpdateTicket(Conversations):
    ERROR = '請重新輸入要更新的票據號碼'
    INFO = '你想將佢更新成為\n%s'
    FAIL = '票據出錯 請重新輸入'
    NO_TICKETS = '暫無紀錄'
    START = '選擇更新項目'
    SUCESS = '你張門票已經被紀錄'
    ITEM = '更新%s'
    YOURS = '你的門票:\n%s'
