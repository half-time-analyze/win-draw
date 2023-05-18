import pandas as pd
from collections import defaultdict

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time



df = pd.DataFrame()

# 크롬드라이버 실행
driver = webdriver.Chrome('./chromedriver') 

#크롬 드라이버에 url 주소 넣고 실행
url = 'https://www.xscores.com/soccer/england/premier-league/results/'
driver.get(url)

time.sleep(10)
row = 0
# CCC = driver.find_elements(By.CLASS_NAME, "ind_match_wrapper")
# print(CCC)
for i in range(364, 501):
    
    try:
        search_box = driver.find_element(By.CSS_SELECTOR, f"#scoretable > div.competition_data > div.results_wrapper > div > div > a:nth-child({i})")
        search_box.click()
        time.sleep(10)
        driver.find_element(By.CSS_SELECTOR, "#scoretable > div > div.match_menu_wrapper > div > div > div > div.match_tabs.match_tabs__match_stats").click()
        time.sleep(10)
        row += 1
    except:
        i += 1
        continue
    
    data1 = defaultdict(int)
    data2 = defaultdict(int)
    
    
    driver.find_element(By.CSS_SELECTOR, "#scoretable > div > div.match_menu_wrapper > div > div > div > div.match_tabs.match_tabs__match_stats").click()
    time.sleep(10)

    date = driver.find_element(By.CSS_SELECTOR, "#scoretable > div > div.teams_header > div.match_details_date").text
    teamName1 = driver.find_element(By.CSS_SELECTOR, "#scoretable > div > div.teams_header > div.teams_wrapper > div.hTeam > span").text
    teamName2 = driver.find_element(By.CSS_SELECTOR, "#scoretable > div > div.teams_header > div.teams_wrapper > div.aTeam > span").text
    homeAway1 = 1
    homeAway2 = 2

    data1['Match_date'] = date
    data2['Match_date'] = date
    data1['teamName'] = teamName1
    data2['teamName'] = teamName2
    data1['homeAway'] = homeAway1
    data2['homeAway'] = homeAway2


    for i in range(1, 100):
        try:
            col_name = driver.find_element(By.CSS_SELECTOR, f"#match_info_container > div > div:nth-child({i}) > div.stats_bar_descr > div").text
            AAA = driver.find_element(By.CSS_SELECTOR, f"#match_info_container > div > div:nth-child({i}) > div.stats_bar").text
            home, away = AAA.split('\n')
            data1[col_name] = home
            data2[col_name] = away
        except:
            continue

    print(data1)
    print(data2)

    df = df._append(data1, ignore_index=True)
    df = df._append(data2, ignore_index=True)
    
    
    driver.get(url)
    
    
    time.sleep(10)
    


print(df)

df.to_csv('soccer.csv', index=False)