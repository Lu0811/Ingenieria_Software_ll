import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from HtmlTestRunner import HTMLTestRunner

EXPECTED = "Expected: "
RESULT = "|Result: "
USERNAME = "user1@gmail.com"

class TestLogin(unittest.TestCase):
    def setUp(self):
        # Configuración: Se ejecuta antes de cada caso de prueba
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:3000/")
        self.xpath_username = """//*[@id="root"]/div/div[3]/div[2]/form/div[1]/input"""
        self.xpath_password = """//*[@id="root"]/div/div[3]/div[2]/form/div[2]/input"""
        self.xpath_btn_login = """//*[@id="root"]/div/div[3]/div[2]/form/div[3]/button"""
        self.xpath_login_error = """//*[@id="root"]/div/div[3]/div[2]/form/h3"""
        self.xpath_homename = """//*[@id="root"]/div/div[3]/div[1]/div[2]/div[2]/span[1]"""
        self.xpath_miperfil = """//*[@id="root"]/div/div[3]/div[1]/div[2]/span/a"""
        self.xpath_logout = """//*[@id="root"]/div/div[3]/div[1]/div[2]/button"""

    def tearDown(self):
        self.driver.close()

    def test_login_success(self):
        self.driver.find_element(By.XPATH, self.xpath_username).send_keys(USERNAME)
        self.driver.find_element(By.XPATH, self.xpath_password).send_keys("admin")

        self.driver.find_element(By.XPATH, self.xpath_btn_login).click()
        self.driver.implicitly_wait(5)
        
        result = self.driver.find_element(By.XPATH, self.xpath_homename).text
        print(EXPECTED,"Shinji Ikari")
        print(RESULT, result)
        self.assertEqual(result, "Shinji Ikari")

    
    def test_login_invalid_password(self):
        self.driver.find_element(By.XPATH, self.xpath_username).send_keys(USERNAME)
        self.driver.find_element(By.XPATH, self.xpath_password).send_keys("zxcvb")
        self.driver.find_element(By.XPATH,self.xpath_btn_login).click()
        self.driver.implicitly_wait(5)

        result = self.driver.find_element(By.XPATH, self.xpath_login_error).text

        print(EXPECTED, "Login")  
        print(RESULT, result)
        self.assertEqual(result, "Login")
    
    def test_login_invalid_username(self):
        self.driver.find_element(By.XPATH, self.xpath_username).send_keys("someuser@@gmail.com")
        self.driver.find_element(By.XPATH, self.xpath_password).send_keys("admin")
        self.driver.find_element(By.XPATH,self.xpath_btn_login).click()
        self.driver.implicitly_wait(5)

        result = self.driver.find_element(By.XPATH, self.xpath_login_error).text

        print(EXPECTED, "Login")  
        print(RESULT, result)
        self.assertEqual(result, "Login")

    def test_login_empty_username(self):
        self.driver.find_element(By.XPATH, self.xpath_username).send_keys("")
        self.driver.find_element(By.XPATH, self.xpath_password).send_keys("admin")
        self.driver.find_element(By.XPATH,self.xpath_btn_login).click()
        self.driver.implicitly_wait(5)

        result = self.driver.find_element(By.XPATH, self.xpath_login_error).text

        print(EXPECTED, "Login")  
        print(RESULT, result)
        self.assertEqual(result, "Login")

    def test_login_empty_password(self):
        self.driver.find_element(By.XPATH, self.xpath_username).send_keys(USERNAME)
        self.driver.find_element(By.XPATH, self.xpath_password).send_keys("")
        self.driver.find_element(By.XPATH,self.xpath_btn_login).click()
        self.driver.implicitly_wait(5)

        result = self.driver.find_element(By.XPATH, self.xpath_login_error).text

        print(EXPECTED, "Login")
        print(RESULT, result)
        self.assertEqual(result, "Login")

if __name__ == "__main__":
    report_name = 'test_login_report.txt'
    suite = unittest.TestSuite()
    suite.addTest(TestLogin('test_login_success'))
    suite.addTest(TestLogin('test_login_invalid_password'))
    suite.addTest(TestLogin('test_login_invalid_username'))
    suite.addTest(TestLogin('test_login_empty_username'))
    suite.addTest(TestLogin('test_login_empty_password'))

    with open(report_name, 'w') as f:
        runner = HTMLTestRunner(stream=f, verbosity=2, report_name="reporte_de_pruebas")
        result = runner.run(suite)
    print(result)