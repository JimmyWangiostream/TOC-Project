# TOC-Project

## FSM:
![fsm](https://i.imgur.com/n7iFLqi.png)


##  How To Communication with teleBot?
commandline => **python3 app.py**
打開telebot 應用程式 搜尋 "GoGgMenubot" 即可與teleBot對話囉!

## How to draw fsm on website?
commandlind 1=>**./ngrok http 5000**
找出https://......io
並把**drawfsm.py**的variable **API_TOKEN**  (in line 13) 改成 " https://......io/**hook**  "儲存後
commandline 2=>**python3 drawfsm.py**
打開瀏覽器進入" https://......io/**show-fsm** "後即可看到 fsm囉

### Bonus
**a.** Praitical or any other creative design -??

**b.** More telegram functionalities -- Sending images 於 GoGgMenubo中的"hasperson"狀態輸入 "menu " Implement 此功能
                                    (By SendPhoto(userid,圖片url) 於 app.py 的line 152

**c.** Dynamic data -- parsing website 於GoGgMenubo中的"hasperson"狀態輸入 "news " Implement 此功能 
                   (By BeautifulSoup於 app.py 的 line 155開始)
