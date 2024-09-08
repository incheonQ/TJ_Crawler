# Bugs 가사 추출기

이 프로그램은 Bugs 음악 사이트에서 노래 가사를 자동으로 추출하는 Python 스크립트입니다.

## 기능

- 사용자가 입력한 노래 제목으로 Bugs 사이트에서 가사를 검색합니다.
- 검색된 가사를 CSV 파일로 저장합니다.
- 여러 노래의 가사를 한 번에 추출할 수 있습니다.

## 요구 사항

- Python 3.6 이상
- 다음 Python 패키지가 필요합니다:
  - selenium
  - webdriver_manager
  - requests

## 설치

1. 이 저장소를 클론하거나 다운로드합니다.
2. Chrome 브라우저가 설치되어 있는지 확인합니다.
3. Chrome WebDriver를 다운로드합니다:
   - [ChromeDriver](https://developer.chrome.com/docs/chromedriver/downloads?hl=ko) 혹은 [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) 페이지에서 사용 중인 Chrome 버전에 맞는 WebDriver를 다운로드합니다.
   - 다운로드한 WebDriver를 시스템 경로에 추가하거나, 스크립트와 같은 디렉토리에 위치시킵니다.
4. 필요한 Python 패키지를 설치합니다:

```
pip install selenium webdriver_manager requests
```

## 사용방법
```
python bugs_lyrics.py -lyrics "노래제목1" "노래제목2" "노래제목3"
```
- `-lyrics` 또는 `-l` 옵션 뒤에 원하는 노래 제목을 따옴표로 묶어 입력합니다.
- 여러 노래 제목을 공백으로 구분하여 입력할 수 있습니다.

## 출력

- 추출된 가사는 `lyrics.csv` 파일에 저장됩니다.
- CSV 파일은 '노래 제목'과 '가사' 두 열로 구성됩니다.
- 프로그램을 여러 번 실행하면 결과가 기존 CSV 파일에 추가됩니다.

## 주의사항

- 이 프로그램은 교육 및 개인 사용 목적으로만 사용해야 합니다.
- Bugs 사이트의 이용 약관을 준수하여 사용하세요.
- 과도한 요청은 IP 차단의 원인이 될 수 있으니 주의하세요.
