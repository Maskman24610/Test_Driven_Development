from selenium import webdriver
from selenium.webdriver.common.keys import  Keys
import unittest
from selenium.common.exceptions import StaleElementReferenceException
from superlists.tools import tool

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox(executable_path="/home/joseph/git/Test_Driven_Development/superlists/geckodriver")
        self.browser.implicitly_wait(3)
        
    def tearDown(self):
        self.browser.quit()
    
    def check_for_row_in_list_table(self, row_text):
        #self.browser.refresh()
        #self.browser.get("http://localhost:8000")
        with(tool.wait_page_load(self.browser)):
            table = self.browser.find_element_by_id("id_list_table")
            rows = table.find_elements_by_tag_name("tr")
            self.assertIn(row_text, [row.text for row in rows])
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get("http://localhost:8000")
        
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
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        
        #self.browser.refresh()
        #self.browser.get("http://localhost:8000")
        #此時仍有一個文字方塊，讓他可以加入令一個項目
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)
        
        #網頁更新，此時他的清單有這兩項
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        self.check_for_row_in_list_table("2: Use peacock feathers make a fly")
        
        #table = self.browser.find_element_by_id("id_list_table")
        #rows = table.find_element_by_tag_name("tr")
        try:
            table = self.browser.find_element_by_id("id_list_table")
            rows = table.find_elements_by_tag_name("tr")
        except StaleElementReferenceException as msg:
            print ("查找元素異常 %s"%msg)
            print ("重新查找元素")
            table = self.browser.find_element_by_id("id_list_table")
            rows = table.find_elements_by_tag_name("tr")
        self.assertIn("1: Buy peacock feathers", [row.text for row in rows])
        self.assertIn(
            "2: Use peacock feathers to make a fly",
            [row.text for row in rows]
            )
        
        self.fail("Finish the test!")
if __name__=="__main__":
    unittest.main(warnings = "ignore")