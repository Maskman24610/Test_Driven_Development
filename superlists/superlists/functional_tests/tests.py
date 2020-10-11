from selenium import webdriver
from selenium.webdriver.common.keys import  Keys
#import unittest
#from tools import tool
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time
import sys

#因為LiveServerTestCase無法自動找到靜態檔案，但是StaticLiveServerTestCase可以
#所以改為使用StaticLiveServerTestCase
class NewVisitorTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if "liveserver" in arg:
                cls.server_url = "http://" + arg.split("=")[1]
                return    
        super().setUpClass()
        cls.server_url = cls.live_server_url
    
    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()
             
    def setUp(self):
        self.browser = webdriver.Firefox(executable_path="/home/joseph/git/Test_Driven_Development/superlists/geckodriver")
        self.browser.implicitly_wait(3)
        
    def tearDown(self):
        self.browser.quit()
         
    def wait_for_row_in_list_table(self, row_text):
        MAX_WAIT = 10
        start_time = time.time()
        while True:  
            try:
                table = self.browser.find_element_by_id('id_list_table')  
                rows = table.find_elements_by_tag_name('tr')
                time.sleep(1)
                self.assertIn(row_text, [row.text for row in rows])
                return  
            except (AssertionError, WebDriverException) as e:  
                if time.time() - start_time > MAX_WAIT:  
                    raise e 
                time.sleep(0.5)  
    def check_for_row_in_list_table(self, row_text):
        #self.browser.refresh()
        #self.browser.get("http://localhost:8000")
        #with(tool.wait_page_load(self.browser)):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        #with(tool.wait_page_load(self.browser)):
        self.assertIn(row_text, [row.text for row in rows])
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.server_url)
        
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)
        
        #馬上輸入一個待辦事項
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            "Enter a to-do item"
            )
        
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        edith_list_url = self.browser.current_url
        #self.wait_for_row_in_list_table("1: Buy peacock feathers")
        
        self.assertRegex(edith_list_url, "/lists/.+")
        #with(tool.wait_page_load(self.browser)):
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        
        #self.browser.refresh()
        #self.browser.get("http://localhost:8000")
        #此時仍有一個文字方塊，讓他可以加入令一個項目
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        #網頁更新，此時他的清單有這兩項
        #with(tool.wait_page_load(self.browser)):
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        self.check_for_row_in_list_table("2: Use peacock feathers to make a fly")
        
        #現在有一個新的使用者Francis 來到網站
        ##我們使用一個新的瀏覽器殲段工作來確保
        ##前一個使用者的任何資訊都不會被cookies等機制送出
        self.browser.quit()
        self.browser = webdriver.Firefox(executable_path="/home/joseph/git/Test_Driven_Development/superlists/geckodriver")
        
        #Francis造訪首頁，並沒有出現前一個使用者的清單的跡象
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)
        
        
        #Francis 輸入一個新項目，做出一個新的清單
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        #Francis取捯他自己獨一無二的清單
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/+.")
        self.assertNotEqual(francis_list_url, edith_list_url)
        
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)
        
        #self.fail("Finish the test!")
    def test_layout_and_stying(self):
        #前往首頁
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)
        
        #開始編輯新清單，看到這裡的
        #輸入方塊也妥善的置中
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta = 5,
            )
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )