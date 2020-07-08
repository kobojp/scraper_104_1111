# 使用flask call  執行檔
from flask import Flask
import email_find
import threading

app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     thread = threading.Thread(target=email_find.email, args=('金融', ))   # 增加定義線程
#     thread.start()  # 讓線程開始工作 
#     return 'Hello, World!,爬人力銀行'

@app.route('/user/<find_key>/<select_salary>/<select_area>/<related_key>/<related_content>')
def show_user_profile(find_key, select_salary, select_area, related_key, related_content):
    print(select_area) # input 11,22
    # print(type(select_area))
    print(select_area.split(','))
    select_area = select_area.split(',')
    print(type(select_area))
    thread = threading.Thread(target=email_find.email, args=(find_key, select_salary, select_area, related_key, related_content))   # 增加定義線程
    thread.start()  # 讓線程開始工作 
    # show the user profile for that user
    return '爬取資料 %s %s %s %s %s ' % (find_key, select_salary, select_area, related_key, related_content)

"""
爬取 工作關鍵字 find_key 
薪資 select_salary
市區 select_area
工作最相關關鍵字 related_key

使用方法：
例子 ：你的heroku網址/user/金融/30000/台北市,新北市,桃園市/分析/管理

/user/爬取關鍵字/篩選薪水多少以上/台北市,新北市,桃園市/最相關工作關鍵字


市區域只能選擇3個市/縣市，你也可以到email_find 新增更多的市/縣市

新增市/縣市
例如：
    mask1 = concat_104_1111.薪資 >= int(select_salary)
    mask2 = concat_104_1111.地區.str.contains(select_area[0])
    mask3 = concat_104_1111.地區.str.contains(select_area[1])
    mask4 = concat_104_1111.地區.str.contains(select_area[2])
    mask6 = concat_104_1111.地區.str.contains(select_area[3]) #新增 新增市/縣市
    mask5 = concat_104_1111.工作名稱.str.contains(related_key)
    mask6 = concat_104_1111.工作內容.str.contains(related_content) #工作內容簡介也許會有相關的工作
    
    #搜尋 3萬以上 工作名稱有"證卷"關鍵字、區域 台北市 新北市
    # & = and , | = or   

    #儲存成 Excel格式檔
    file_name = find_key #檔案名稱 依關鍵字取名
    save_excel = concat_104_1111.loc[((mask2 | mask3 | mask4) & mask1 & mask5) | ((mask2 | mask3 | mask4) & mask1 & mask6)]

"""
if __name__ == "__main__":
    app.run()

