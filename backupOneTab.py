from selenium import webdriver

chromedriver = 'D:/_W/_Web/_downloads/chromedriver_win32/chromedriver'
options = webdriver.ChromeOptions()
options.add_extension('C:/Users/joshc/AppData/Local/Google/Chrome/User Data/Default/Extensions/chphlpgkkbolifaimnlloiipkdnihall/1.33_0')

driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
driver.get('chrome-extension://chphlpgkkbolifaimnlloiipkdnihall/onetab.html')