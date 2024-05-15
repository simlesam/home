from datetime import datetime
import sqlite3
import streamlit as st
from streamlit_image_select import image_select
import datetime
import requests
import base64
import json
from pytz import timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials

conn=sqlite3.connect("./db/bmdb.db")

# 前置作業
scopes = ["https://spreadsheets.google.com/feeds"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["cjson"], scopes)
gss_client = gspread.authorize(credentials)

#開啟 Google Sheet 資料表
#spreadsheet_key = '1b6OiZ8USWq94vvf-0jg3WSnP8RVggRFpt2_qn_5fcKM' 
spreadsheet_key = '1SksIfxb-kWnALp3R2bkRmqjmx3jTSSTfFW8dtrh4jMY' 
        
sheet = gss_client.open_by_key(spreadsheet_key).sheet1

class DateTimeEncoder(json.JSONEncoder):
   def default(self,obj):
      if isinstance(obj,datetime.datetime):
         return obj.strftime('%Y-%m-%d %H:%m:%S')
      elif isinstance(obj,datetime.date):
         return obj.strftime('%Y-%m-%d')
      return json.JSONEncoder.default(self,obj)


st.set_page_config(page_title="行動服務", page_icon="🖼️")
st.markdown("## 行動服務登記")

def main_bg(main_bg):
   main_bg_ext="png"
   st.markdown(
      f'''
      <style>
      .stApp{{
      background:url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg,"rb").read()).decode()});
      background-size:cover
      }}
      </style>
      ''',
      unsafe_allow_html=True
   )
main_bg('./example_picture/background.png')

room=""

img = image_select(
    label="請選擇會議室",
    images=[
        "./example_picture/204_small.png",
        "./example_picture/208_small.png",
        "./example_picture/1305_small.png",
        "./example_picture/1307_small.png",
        "./example_picture/1308A_small.png",
        "./example_picture/1308B_small.png",
        "./example_picture/1309_small.png",
    ],
    captions=["204","208","1305","1307","1308A","1308B","1309"],  
)

if img=="./example_picture/204_small.png":
   room="204簡報室"

elif img=="./example_picture/208_small.png":
   room="208會議室"

elif img=="./example_picture/1305_small.png":
   room="1305會議室"

elif img=="./example_picture/1307_small.png":
   room="1307會議室"

elif img=="./example_picture/1308A_small.png":
   room="1308A會議室"

elif img=="./example_picture/1308B_small.png":
   room="1308B會議室"

elif img=="./example_picture/1309_small.png":
   room="1309會議室"

st.markdown("請選擇需要的服務")
serve1=st.checkbox('玻璃杯',value=False,key="serve1")
if serve1:glasscup = st.slider(
    "玻璃杯",
    0,
    100,
    key="glasscup",
)
else :glasscup=0

serve2=st.checkbox('滑輪桌',value=False,key="serve2")
if serve2:table = st.slider(
    "滑輪桌",
    0,
    8,
    key="table",
)
else :table=0

serve3=st.checkbox('活動椅',value=False,key="serve3")
if serve3:chair = st.slider(
    "活動椅(有椅背)",
    0,
    40,
    key="chair",
)
else :chair=0
   
serve4=st.checkbox('海報架',value=False,key="serve4")
if serve4:seapaper = st.slider(
    "海報架",
    0,
    6,
    key="seapaper",
)
else :seapaper=0
   



with st.form("my_form"):
   inputdate=st.date_input('使用日期',datetime.date.today(),key="inputdate")

   ttime = st.selectbox(
    '使用時間',
    ['09:00', '10:00', '11:00', '13:00','14:00','15:00','16:00'],key="ttime")
   name=st.text_input('輸入姓名：',key="name")
   number=st.text_input('分機：',key="number")
   submitted = st.form_submit_button("確定提交")


   
   

message = '\n'
# LINE Notify 權杖
token = "cgvPZ8W4KSbOVuKloO4zgOSldKc4ZWciybgg4WkplUU"; 
#安防群組

# 設定台灣台北時區
#tz = timezone('Asia/Taipei')
# 取得目前時間
#now = datetime.now() + timedelta(hours=8)

def sendLineNotify(room,inputdate,ttime,name,glasscup,table,chair,seapaper,imessage):
  
  #myday=innow.strftime('%Y-%m-%d')
  #mytime=innow.strftime('%H:%M:%S')
 
  # HTTP 標頭參數與資料
  headers = {"Authorization": "Bearer " + token}
  #imessage+=f'日期：{myday}\n時間：{mytime}\n車位：{inleveloption}-{inparkingNo}\n車牌：{incarNo}'
  imessage+=f'{room}\n日期:{inputdate}-{ttime}\n申請人:{name}\n玻璃杯:{glasscup}\n滑輪桌:{table}\n活動椅:{chair}\n海報架:{seapaper}'
  data = {'message': imessage}
  # 以 requests 發送 POST 請求
  requests.post("https://notify-api.line.me/api/notify",headers=headers, data=data)
  writetoSQLite(room,inputdate,ttime,name,number,glasscup,table,chair,seapaper)
  return  

def writetoSQLite(room,inputdate,ttime,name,number,glasscup,table,chair,seapaper):
   try:
       # 建立資料庫連線 SQLite
       cursor=conn.cursor()
       sqlstr='INSERT INTO 行動服務 (會議室,使用日期,使用時間,姓名,姓名代號,玻璃杯,滑輪桌,焦糖椅,海報架) VALUES (?,?,?,?,?,?,?,?,?);'
       cursor.execute(sqlstr,(room,inputdate,ttime,name,number,glasscup,table,chair,seapaper))
       conn.commit()
   except Exception as e:
      print("Error: %s" % e) 
   #Close the cursor and delete it
   cursor.close()
   del cursor 
   return  

#def writetogoogle(room,inputdate,ttime,name,number):
#      url='https://script.google.com/macros/s/AKfycbzsykcqzdQ3gz6IbGj26ybhN4Py98OG-PQ-g4nsNHGwgbfa-ORY-QjZ5vcR1ScgMKvQPg/exec'
#      params={
#        'name':'工作表1',
#         'top':'true',
#         'data':[f'{room}',f'{inputdate}',f'{ttime}',f'{name}',f'{number}']
#      }
#      requests.get(url=url,params=params)


if submitted & ((name != "") & (number != "")):
      #room=st.session_state["room"]
      inputdate=st.session_state["inputdate"]
      ttime=st.session_state["ttime"]
      name=st.session_state["name"]
      number=st.session_state["number"]
  #st.write(f'{leveloption}-{parkingNo}：{carNo}')
      st.write(f'已登記 :red[{name}]於 :red[{inputdate}-{room}] 的預約，感謝您的申請!')
  #Line Notify
      sendLineNotify(room,inputdate,ttime,name,glasscup,table,chair,seapaper,message)
      ddate=json.dumps(inputdate,cls=DateTimeEncoder)
      data=[room,ddate,ttime,name,number,glasscup,table,chair,seapaper]
      sheet.append_row(data)
