import requests
from bs4 import BeautifulSoup
import re
import random
import time
from urllib.parse import quote
from tqdm import tqdm, trange
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import date
# from IPython.display import clear_output
import os,os.path
import glob
import yagmail

# , find_salary, find_area, related_key
def email(find_key='金融', select_salary = 40000, select_area = list(['台北市', '新北市', '桃園市']), related_key = '分析'):
    def get_todate():
        return date.today()

    def selenium_get_Code_104(url):
        #heroku selenium使用
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        
        #一般本地windows liunx使用
        # chrome_options = Options() # 啟動無頭模式
        # chrome_options.add_argument('--headless')  #規避google bug
        # chrome_options.add_argument('--disable-gpu')
        # driver = webdriver.Chrome(chrome_options=chrome_options)

        driver.get(url)
        save = driver.page_source
        driver.quit()#關閉瀏覽器
        soup = BeautifulSoup(save, "html.parser")
        page = soup.select('.page-select.js-paging-select.gtm-paging-top')[0].find_all('option')[-1].get('value')
        return page

    def read_url(url):
        USER_AGENT_LIST = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
            "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            ]
        USER_AGENT = random.choice(USER_AGENT_LIST)
        headers = {'user-agent': USER_AGENT}
        s = requests.Session()
        req = s.get(url, headers = headers)
        soup = BeautifulSoup(req.text, "html.parser")
        return soup

    def csv_column_104(path_csv, key_txt): #建立行標題
        with open(path_csv + '.csv', mode='a+', newline='', encoding='utf-8') as employee_file: 
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow(['日期', '工作名稱', '公司名稱', '公司地址', '薪資', '工作內容', '地區', '經歷', '學歷', '公司人數', '文章編號', '工作網址'])

    def find_title_104(key_txt):
        #路徑組合
        today = get_todate()
        path_csv = 'jobs_csv/'+ str(today) + key_txt + '_104人力銀行'
        if not os.path.isdir('jobs_csv'): # 確認是否有jobs_csv資料夾  沒有則返回Ture
            os.mkdir('jobs_csv') # 建立jobs_csv資料夾
            print('建立jobs_csv資料夾完成')
        csv_column_104(path_csv, key_txt) #建立行標題
        csv_save = ""
        key = quote(key_txt)
        #  104 api searchTempExclude=2  -> 設定排除派遣
        find_page_url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={0}&order=15&asc=0&page=1&mode=s&jobsource=2018indexpoc&searchTempExclude=2'.format(key)
        get_sum_page = int(selenium_get_Code_104(find_page_url))
        print('共有：' + str(get_sum_page) + ' 頁')
        for i in tqdm(range(1, get_sum_page+1)):  #set page 1 to find all max page ,tqdm讀取進度條
            url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={0}&order=15&asc=0&page={1}&mode=s&jobsource=2018indexpoc&searchTempExclude=2'.format(key, i) 
            #time.sleep(random.randint(2,10)) #隨機等待
            soup = read_url(url) #讀取網頁
            print('目前爬取頁面是：' + url)
            for title_1 in soup.select('.b-block__left'):
                #有三個資料是無資料的，遇到無資料就跳過這個迴圈
                if title_1.select('.b-list-inline.b-clearfix.job-list-item__company') != soup.select('.b-block__left')[0].select('.b-list-inline.b-clearfix.job-list-item__company'):
                    #日期
                    try:
                        #正常代表找到 讚 廣告 (業主買廣告)，發生異常代表找不到 讚，執行except找日期 
                        date_match__ = title_1.select('.b-icon--gray.b-icon--w18')[0].select('use')[0]
                        date = '廣告'
                    except:
                        date = title_1.select('.b-tit__date')[0].get_text().replace('\n','').replace(' ','')
            
                    #地區
                    area = title_1.select('.b-list-inline.b-clearfix.job-list-intro.b-content')[0].find('li').get_text()
                    #經歷(年資)
                    experience = title_1.select('.b-list-inline.b-clearfix.job-list-intro.b-content')[0].find_all('li')[1].get_text()
                    try: #業者沒有輸入學歷，遇到錯誤處理
                        #學歷
                        education = title_1.select('.b-list-inline.b-clearfix.job-list-intro.b-content')[0].find_all('li')[2].get_text()
                    except:
                        education = ""
                    #工作網址
                    title_url = title_1.select('.js-job-link')[0].get('href')[2:]
                    #get 文章編號
                    title_str = title_url.split('?')[0].split('/')[-1] #get 文章編號
                    #標題名稱
                    title = title_1.select('.js-job-link')[0].get_text() #get title
                    #print(title + title_url + area)
                    #公司名
                    company_name = title_1.select('li')[1].find('a').get('title').split('\n')[0][4:]
                    try:
                        #公司地址
                        company_address = title_1.select('li')[1].find('a').get('title').split('\n')[1][5:]
                    except:
                        company_address = ""
                    try:
                        #簡介
                        introduction = title_1.select('.job-list-item__info.b-clearfix.b-content')[0].get_text()
                        #處理string \r \n5 \n轉成''
                        introduction = introduction.replace('\r','').replace('\n5','').replace('\n','')
                    except:
                        introduction = ""
                    #薪資
                    try:
                        salary = title_1.select('.b-tag--default')[0].get_text()
                    except:
                        salary = 0 #沒有寫薪資或待遇面議，設定 0
                        
                    if salary == '待遇面議':
                        salary = "待遇面議"
                    else: #數字處理 25000~35000 取25000最低薪資為主要，三位數 = 日薪，四位數 = 論件計酬
                        try:
                            salary = re.search('\d+.\d+', salary).group()
                        except:
                            salary = 0
                    #員工人數
                    try:
                        people = title_1.select('.b-tag--default')[1].get_text()
                    except:
                        people = ""
                    #clear_output() # 清除輸出 用於清除進度讀，註解#不使用：用來檢查出錯的網址

                    with open(path_csv + '.csv', mode='a+', newline='', encoding='utf-8') as employee_file: #w
                        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        employee_writer.writerow([date, title, company_name, company_address, salary, introduction, area, experience, education, people, title_str, title_url])
                else:
                    continue
        return print('爬取104完成：請開啟csv檔案')


    # input_go = input('輸入關鍵字')
    # save_title_data = find_title_104(input_go)




    ############ 1111人力銀行 #########


    def selenium_get_Code_1111(url):
        #heroku selenium使用
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

        # 一般本地windows liunx使用
        # chrome_options = Options() # 啟動無頭模式
        # chrome_options.add_argument('--headless')  #規避google bug
        # chrome_options.add_argument('--disable-gpu')
        # driver = webdriver.Chrome(chrome_options=chrome_options)

        driver.get(url)
        save = driver.page_source
        driver.quit()#關閉瀏覽器
        soup = BeautifulSoup(save, "html.parser")
        
        page = soup.select('.custom-select')[0].select('option')[0].text
        page = page.split('/')
        page = page[1].strip(' ')
        return page


    def csv_column_1111(path_csv): #建立行標題
        with open(path_csv + '.csv', mode='a+', newline='', encoding='utf-8') as employee_file: 
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow(['日期', '工作名稱', '公司名稱', '公司地址', '薪資', '工作內容', '地區', '經歷', '學歷', '工作網址'])

    def find_data_1111(soup):
        #錢錢
        mnone = soup.select('.needs') 
        #縣市區域
        location = soup.select('.needs')
        #日期
        get_date = soup.select('.date')
        #簡介
        jbInfoTxt = soup.select('.jbInfoTxt')
        #網址
        jobs_url = soup.select('.position0')
        #公司名稱、類別、住址
        company_data = soup.select('.d-md-flex')
        #工作標題
        title = soup.select('.position0')
        #工作經驗
        jobs_exp = soup.select('.needs')
        # 學歷
        education = soup.select('.needs')
        return mnone, location, jbInfoTxt, jobs_url, company_data, title, jobs_exp, get_date, education

            
    def find_title_1111(key_txt):
        #路徑組合
        today = get_todate()
        path_csv = 'jobs_csv/' + str(today) + key_txt + '_1111人力銀行'
        if not os.path.isdir('jobs_csv'): # 確認是否有jobs_csv資料夾  沒有則返回Ture
            os.mkdir('jobs_csv') # 建立jobs_csv資料夾
            print('建立jobs_csv資料夾完成')
        csv_column_1111(path_csv) #建立行標題
        key = quote(key_txt)
        find_page_url = 'https://www.1111.com.tw/job-bank/job-index.asp?si=1&ss=s&ks={0}&page=1'.format(key)
        #取得最大page數
        get_sum_page = int(selenium_get_Code_1111(find_page_url))
        print('共有：' + str(get_sum_page) + ' 頁')
        
        for i in tqdm(range(1, get_sum_page+1)):
            url = 'https://www.1111.com.tw/job-bank/job-index.asp?si=1&ss=s&ks={0}&page={1}'.format(key, i)
            soup = read_url(url) #讀取網頁
            #讀取網頁資料
            mnone, location, jbInfoTxt, jobs_url, company_data, title, jobs_exp, get_date, education = find_data_1111(soup)
            print('目前爬取頁面是：' + url)
            for mnone, location, jbInfoTxt, jobs_url, company_data, title, jobs_exp, get_date, education in zip(mnone, location, jbInfoTxt, jobs_url, company_data, title, jobs_exp, get_date, education):
                #錢 取最低薪資
                try:
                    mnone = mnone.find_all("span")[1].get_text()
                    get_mone = re.search('\d+.\d+', mnone).group()
                except:
                    get_mone = '面議（經常性薪資4萬/月含以上）' #可能需要直接給40,000
                #日期
                get_date = get_date.get_text()[5:]
                
                #縣市區域
                location = location.find_all("span")[0].get_text()
                
                #簡介
                jbInfoTxt = jbInfoTxt.get_text().replace("\xa0", "") #刪除\xa0
                
                #工作網址
                jobs_url = 'https://www.1111.com.tw{0}'.format(jobs_url.find('a').get('href'))
        
                #公司名
                company = company_data.find_all('a')[0].get('title').replace('\r','').split('\n')[0][6:]
                
                #公司分類 目前暫不使用
                category = company_data.find_all('a')[0].get('title').replace('\r','').split('\n')[1][6:]
                
                #公司地址
                address = company_data.find_all('a')[0].get('title').replace('\r','').split('\n')[2][6:]
                
                #工作標題
                title = title.find('a').get('title')
                
                # 工作經驗
                jobs_exp = jobs_exp.find_all("span")[2].get_text()
                
                # 學歷
                education = education.find_all("span")[3].get_text()
                # 儲存
                
                # clear_output() # 清除輸出 用於清除進度讀
                
                with open(path_csv + '.csv', mode='a+', newline='', encoding='utf-8') as employee_file: #w
                    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    employee_writer.writerow([get_date, title, company, address, get_mone, jbInfoTxt, location, jobs_exp, education, jobs_url])
        return print('爬取1111完成：請開啟csv檔案')


    # find_key = '金融'
    find_title_104(find_key)
    find_title_1111(find_key)
    
    #讀取爬取到的資料
    get_file_name = glob.glob('jobs_csv/*.csv')
    data_104 = pd.read_csv(get_file_name[0])
    data_1111 = pd.read_csv(get_file_name[1])

    # 日期、工作名稱、公司地址、薪資、工作內容、地區、經歷、學歷、工作網址 依想要的順序排序
    new_data_1111 =  data_1111[['日期', '工作名稱', '薪資', '地區', '工作內容', '公司地址', '經歷', '學歷', '工作網址']]
    new_data_104 = data_104[['日期', '工作名稱', '薪資', '地區', '工作內容', '公司地址', '經歷', '學歷', '工作網址']]
    
    # 接資料
    concat_104_1111 = pd.concat([new_data_1111, new_data_104], axis=0)
    concat_104_1111.shape

    # index重設定
    concat_104_1111.reset_index(drop=True, inplace=True) #drop=True 刪除原有index , inplace 直接更新現有的DataFrame
    
    # 清理資料
    """
    1. 將 待遇面議 轉換成 0
    2. 將 面議（經常性薪資4萬/月含以上）轉成 40000
    3. 將 時薪 例如：150~200 轉成只取最低時薪 150
    4. 移除數字中的, 例如"30,000"將,移除
    """

    #將四萬改成0  但是也可以改成40,000
    concat_104_1111['薪資'] = concat_104_1111.薪資.str.replace('面議（經常性薪資4萬/月含以上）', '40000')

    #將待遇面議改成0
    concat_104_1111['薪資'] = concat_104_1111.薪資.str.replace('待遇面議', '0')

    #時薪 取最低時薪
    concat_104_1111.loc[concat_104_1111.薪資.str.contains('~'),'薪資'] = concat_104_1111.loc[concat_104_1111.薪資.str.contains('~'),'薪資'].str.split('~').str[0]

    #數字有"30,000"將,移除
    concat_104_1111.loc[:,'薪資'] = concat_104_1111['薪資'].apply(lambda x:x.replace(',','')) 

    # 薪資轉成int type
    concat_104_1111.loc[:,'薪資'] = concat_104_1111['薪資'].astype(int)    

    # 過濾
    #3萬以上
    # mask1 = concat_104_1111.薪資 >= 30000
    # mask2 = concat_104_1111.地區.str.contains('台北市')
    # mask3 = concat_104_1111.地區.str.contains('新北市')
    # mask4 = concat_104_1111.地區.str.contains('桃園市')
    # mask5 = concat_104_1111.工作名稱.str.contains('分析師')
    
    mask1 = concat_104_1111.薪資 >= int(select_salary)
    mask2 = concat_104_1111.地區.str.contains(select_area[0])
    mask3 = concat_104_1111.地區.str.contains(select_area[1])
    mask4 = concat_104_1111.地區.str.contains(select_area[2])
    mask5 = concat_104_1111.工作名稱.str.contains(related_key)

    #搜尋 3萬以上 工作名稱有"證卷"關鍵字、區域 台北市 新北市
    # & = and , | = or   
    concat_104_1111.loc[(mask1 & mask2 & mask5) | (mask1 & mask3 & mask5) | (mask1 & mask4 & mask5)].head()

    #儲存成 Excel格式檔
    file_name = find_key #檔案名稱 依關鍵字取名
    save_excel = concat_104_1111.loc[(mask1 & mask2 & mask5) | (mask1 & mask3 & mask5) | (mask1 & mask4 & mask5)]
    save_excel.to_excel('jobs_csv/{}.xlsx'.format(file_name), sheet_name='passengers', index=False)
    print('完成工作')

    # 將工作資訊寄給自己gmail

    file = glob.glob('jobs_csv/*.xlsx') #傳送多個檔案 以list型態
    yag = yagmail.SMTP("你的email", oauth2_file="oauth2_creds.json")
    yag.send(
        to="你的email", subject="爬蟲：熱騰騰的工作資訊", #to = "收件人信箱" 需傳送多個 使用list ['aaaa@123.com', 'bbb@123.com']
        contents="熱騰騰的工作資料",
        attachments= file
        )

if __name__ == "__main__":
    # email('分析師')
    email(find_key='金融', select_salary = 40000, select_area = list(['台北市', '新北市', '桃園市']), related_key = '分析')
