import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, StaleElementReferenceException, ElementClickInterceptedException
from requests.exceptions import ConnectionError
import csv
import os

def get_lyrics(song_titles):
    # Chrome 드라이버 설정
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=service, options=options)

    results = []

    try:
        for song_title in song_titles:
            # 검색 결과 페이지로 직접 이동
            driver.get(f"https://music.bugs.co.kr/search/integrated?q={song_title}")
            
            # 검색 결과에서 첫 번째 곡 선택 (JavaScript 사용)
            driver.execute_script("document.querySelector('a.trackInfo').click();")
            
            # 가사 로딩 대기 및 추출 (JavaScript 사용)
            lyrics = WebDriverWait(driver, 10).until(lambda d: d.execute_script("""
                let lyrics = document.evaluate("/html/body/div[2]/div[2]/article/section[2]/div/div/xmp", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                return lyrics ? lyrics.textContent : null;
            """))
            
            lyrics = lyrics if lyrics else "가사를 찾을 수 없습니다."
            results.append([song_title, lyrics])

            print(f"{song_title} 가사 추출 완료")
    except (TimeoutException, NoSuchElementException) as e:
        print(f"{song_title} 가사 추출 실패: {str(e)}")
        results.append([song_title, "가사 추출 실패"])
    except WebDriverException as e:
        print(f"WebDriver 오류: {str(e)}")
        results.append([song_title, "WebDriver 오류"])
    except ConnectionError as e:
        print(f"네트워크 연결 오류: {str(e)}")
        results.append([song_title, "네트워크 연결 오류"])
    except (StaleElementReferenceException, ElementClickInterceptedException) as e:
        print(f"페이지 요소 상호작용 오류: {str(e)}")
        results.append([song_title, "페이지 요소 오류"])
    except IOError as e:
        print(f"파일 입출력 오류: {str(e)}")
    except Exception as e:
        print(f"예상치 못한 오류 발생: {str(e)}")
        results.append([song_title, "알 수 없는 오류"])
    
    finally:
        driver.quit()

    # CSV 파일로 저장
    file_exists = os.path.isfile('lyrics.csv')
    with open('lyrics.csv', 'a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['노래 제목', '가사'])  # 파일이 없을 때만 헤더 추가
        writer.writerows(results)

    print("가사가 lyrics.csv 파일에 추가되었습니다.")

def main():
    parser = argparse.ArgumentParser(description='노래 가사 추출 프로그램')
    parser.add_argument('-lyrics', '-l', nargs='+', help='노래 제목 (여러 개 입력 가능)')
    
    args = parser.parse_args()
    
    if args.lyrics:
        get_lyrics(args.lyrics)
    else:
        print("노래 제목을 입력해주세요. 사용 예: python bugs_lyrics.py -lyrics '노래제목1' '노래제목2'")

if __name__ == "__main__":
    main()