from selenium import webdriver
import time
import hesapinst
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sqlite3

browser = webdriver.Edge(executable_path="C:\Program Files (x86)\msedgedriver.exe")
browser.maximize_window()

url = "https://www.instagram.com/"

browser.get(url)
time.sleep(1)

username = browser.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input")
password = browser.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input")

username.send_keys(hesapinst.username)
password.send_keys(hesapinst.password)
time.sleep(1)

login_button = browser.find_element_by_xpath("//*[@id='loginForm']/div/div[3]/button")
login_button.click()
time.sleep(10)

browser.find_element_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[6]").click()
time.sleep(2)

browser.find_element_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[6]/div[2]/div[2]/div[2]/a[1]").click()
time.sleep(2)

#Çalışmayan kısım burası (profil kısmındaki takipçilere tıklayıp takipçilerin olduğu listeyi açması lazım ama html kodunu bulduramadım bir türlü selenium'a)#
browser.find_element_by_css_selector("._aacl _aacs _aact _aacx _aada").click()
time.sleep(1)
#####################################################################################


#Burası açılan takipçiler listesinde full aşağı inip bütün listenin yüklenmesini sağlayacak#
jscommand="""
followers = document.querySelector(".isgrP");
followers.scrollTo(0, followers.scrollHeight);
var lenOfPage=followers.scrollHeight;
return lenOfPage;
"""
lenOfPage = browser.execute_script(jscommand)
match=False
while(match==False):
    lastCount = lenOfPage
    time.sleep(1)
    lenOfPage = browser.execute_script(jscommand)
    if lastCount == lenOfPage:
        match=True
time.sleep(2)

takipciler = browser.find_elements_by_xpath("//*[@class='FPmhX notranslate  _0imsa ']")
###############################################################


#Data Base Connect#######################################################
connect = sqlite3.connect("followers.db")
cursor = connect.cursor()

cursor.execute("Create Table If Not Exists takipciler (İsim TEXT)")
cursor.execute("Create Table If Not Exists takip_edilenler (İsim TEXT)")

cursor.execute("DELETE FROM takip_edilenler")
cursor.execute("DELETE FROM takipciler")

connect.commit()
#########################################################################
for takipci in takipciler:
    sorgu2 = "Select * From takipciler where İsim =?"
    cursor.execute(sorgu2,(takipci.text,))
    var = cursor.fetchall()

    if len(var)==0:
        sorgu = "Insert Into takipciler Values(?)"
        cursor.execute(sorgu, (takipci.text,))
        connect.commit()

#burda takipcileri dataya yazdıkdan sonra takip edilenlere geçtiği kısım#
browser.find_element_by_xpath("/html/body/div[6]/div/div/div[1]/div/div[2]/button").click()
time.sleep(1)
browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a").click()
time.sleep(1)

lenOfPage = browser.execute_script(jscommand)
match=False
while(match==False):
    lastCount = lenOfPage
    time.sleep(1)
    lenOfPage = browser.execute_script(jscommand)
    if lastCount == lenOfPage:
        match=True
time.sleep(2)

takip_edilenler = browser.find_elements_by_xpath("//*[@class='FPmhX notranslate  _0imsa ']")
time.sleep(2)

for takip in takip_edilenler:
    sorgu3 = "Select * From takip_edilenler where İsim =?"
    cursor.execute(sorgu3,(takip.text,))
    var = cursor.fetchall()

    if len(var)==0:
        sorgu4 = "Insert Into takip_edilenler Values(?)"
        cursor.execute(sorgu4, (takip.text,))
        connect.commit()
#################################################################

###############Gt Yapmayan filtreleme###############
sayı = 1
for i in takip_edilenler:
    cursor.execute("Select * From takipciler where İsim =?",(i.text,))
    a = cursor.fetchall()

    if len(a) == 0:
        print(str(sayı)+": "+i.text + ": seni geri takip etmiyor")
        sayı += 1
time.sleep(1)

browser.close()
####################################################################