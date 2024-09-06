from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import csv
import random
import argparse

def initialize_driver():
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    driver = webdriver.Chrome(options=options)
    return driver

def search_and_extract(driver, artist_name):
    search_input = driver.find_element(By.NAME, "strText")
    search_input.clear()
    search_input.send_keys(artist_name)

    select = Select(driver.find_element(By.NAME, "strType"))
    select.select_by_value("2")

    search_button = driver.find_element(By.CSS_SELECTOR, "img[src='../images/tjsong/btn_search.gif']")
    search_button.click()

    all_results = []
    page = 1

    while True:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.board_type1"))
            )

            result_table = driver.find_element(By.CSS_SELECTOR, "table.board_type1")
            rows = result_table.find_elements(By.TAG_NAME, "tr")[1:]

            if not rows:
                break

            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 5:
                    song_num = cols[0].text
                    song_title = cols[1].text
                    artist = cols[2].text
                    lyricist = cols[3].text
                    composer = cols[4].text
                    all_results.append([song_num, song_title, artist, lyricist, composer])

            # 다음 페이지로 이동
            try:
                next_page = driver.find_element(By.XPATH, f"//a[contains(text(), '{page + 1}')]")
                next_page.click()
                page += 1
                time.sleep(random.uniform(1, 3))  # 페이지 로딩을 위한 대기
            except NoSuchElementException:
                break  # 다음 페이지가 없으면 종료

        except (NoSuchElementException, TimeoutException):
            break

    return all_results

def main():
    parser = argparse.ArgumentParser(description='TJ 노래방 곡 정보 크롤러')
    parser.add_argument('-s', '--singer', type=str, help='가수명 (쉼표로 구분하여 여러 명 입력 가능)')
    args = parser.parse_args()

    if args.singer:
        artists = [artist.strip() for artist in args.singer.split(',')]
    else:
        artists = input('가수명을 입력해주세요. 여러 명을 입력할 경우 쉼표로 구분해주세요. \n >>>').split(',')
        artists = [artist.strip() for artist in artists]

    driver = initialize_driver()
    driver.get("https://www.tjmedia.com/tjsong/song_search.asp")

    for artist in artists:
        print(f"{artist} 검색 중...")
        results = search_and_extract(driver, artist)
        if results:
            filename = f'tj_songs_by_{artist.replace(" ", "_")}.csv'
            with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['곡번호', '곡제목', '가수', '작사', '작곡'])
                for result in results:
                    csv_writer.writerow(result)
            print(f"{artist}의 {len(results)}곡을 크롤링 완료. 파일명: {filename}")
        else:
            print(f"{artist}의 검색 결과가 없습니다.")

        time.sleep(random.uniform(3, 7))

    driver.quit()
    print("모든 가수 크롤링 완료")

if __name__ == "__main__":
    main()