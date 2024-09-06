import csv
import time
import random
import signal
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options

# 전역 변수로 중지 플래그 설정
stop_crawling = False

def signal_handler(signum, frame):
    global stop_crawling
    print("\n크롤링을 안전하게 중지합니다. 잠시만 기다려주세요...")
    stop_crawling = True

# SIGINT (Ctrl+C) 시그널 핸들러 등록
signal.signal(signal.SIGINT, signal_handler)

def initialize_driver():
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    return webdriver.Chrome(options=options)

def search_and_extract(driver, song_number):
    search_input = driver.find_element(By.NAME, "strText")
    search_input.clear()
    search_input.send_keys(str(song_number))

    search_button = driver.find_element(By.CSS_SELECTOR, "img[src='../images/tjsong/btn_search.gif']")
    search_button.click()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.board_type1"))
        )

        result_table = driver.find_element(By.CSS_SELECTOR, "table.board_type1")
        rows = result_table.find_elements(By.TAG_NAME, "tr")[1:]

        results = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 3:
                song_num = cols[0].text
                song_title = cols[1].text
                artist = cols[2].text
                results.append([song_num, song_title, artist])
        return results
    except (NoSuchElementException, TimeoutException):
        return []


def save_checkpoint(song_number):
    with open('checkpoint.txt', 'w') as f:
        f.write(str(song_number))

def load_checkpoint():
    try:
        with open('checkpoint.txt', 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 1

def main():
    global stop_crawling
    start_number = load_checkpoint()
    end_number = 87243
    songs_per_file = 1000
    max_runtime = timedelta(hours=6)

    driver = initialize_driver()
    driver.get("https://www.tjmedia.com/tjsong/song_search.asp")

    select = Select(driver.find_element(By.NAME, "strType"))
    select.select_by_value("16")

    checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox'][name='strWord'][value='1']")
    if not checkbox.is_selected():
        checkbox.click()

    current_file_number = start_number // songs_per_file + 1
    csv_file = open(f'tj_songs_{current_file_number}.csv', 'a', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file)

    if start_number % songs_per_file == 1:
        csv_writer.writerow(['곡번호', '곡제목', '가수'])

    start_time = datetime.now()

    try:
        for song_number in range(start_number, end_number + 1):
            if stop_crawling:
                print("사용자에 의해 크롤링이 중지되었습니다.")
                break

            if datetime.now() - start_time > max_runtime:
                print("최대 실행 시간 도달. 프로그램을 종료합니다.")
                break

            if song_number % songs_per_file == 1 and song_number != start_number:
                csv_file.close()
                current_file_number += 1
                csv_file = open(f'tj_songs_{current_file_number}.csv', 'w', newline='', encoding='utf-8')
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['곡번호', '곡제목', '가수'])

            try:
                results = search_and_extract(driver, song_number)
                if results:
                    for result in results:
                        csv_writer.writerow(result)
                    print(f"곡 번호 {song_number} 크롤링 완료")
                else:
                    print(f"곡 번호 {song_number}에 대한 결과 없음")
            except Exception as e:
                print(f"오류 발생: {e}. 곡 번호 {song_number} 건너뜀")

            save_checkpoint(song_number + 1)
            time.sleep(random.uniform(3, 7))

    finally:
        driver.quit()
        csv_file.close()
        print("크롤링 완료 또는 중지됨")

if __name__ == "__main__":
    main()
