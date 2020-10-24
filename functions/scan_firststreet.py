from selenium import webdriver
# from PIL import Image
# import io

options = webdriver.FirefoxOptions()
options.add_argument('--headless')

table_xpath = '/html/body/div[1]/div/main/div/section/article/section[4]/section/div[2]/div[1]/div/div[3]/nav'
url = 'https://floodfactor.com/property/111-greensboro-ave-tuscaloosa-alabama/10343212_fsid'
browser = webdriver.Firefox(options=options)
browser.get(url)

maps = browser.find_elements_by_class_name("mapInner")
map = maps[1]

text = browser.find_element_by_xpath(table_xpath)
text_list = text.text.split('\n')
percent_depth = dict(zip(text_list[::2], text_list[1::2]))


# marker = browser.find_elements_by_class_name('sc-hmzhuo dyBRwB')
#
# '/html/body/div[1]/div/main/div/section/article/section[4]/section/div[3]/div/div/div/div/div/div[2]/div/div[1]/svg'
# image = Image.open(io.BytesIO(map.screenshot_as_png))
# image.show()
#
# image_marker = Image.open(io.BytesIO(map.screenshot_as_png))
# image_marker.show()

# paletted = image.convert('P', palette=Image.ADAPTIVE, colors=10)
