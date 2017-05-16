# SimCity4Backup

(Korean)

심시티 4 유저 데이터를 백업하는 프로그램입니다. (개인적 용도로 사용하기 위함)

다음을 지원합니다.
* 건물, 도시, 스크린샷을 zipfile 라이브러리로 압축하여 백업 파일을 만듭니다.
* 건물, 도시, 스크린샷 중 백업할 항목을 선택할 수 있습니다.
* 자동으로 건물, 도시, 스크린샷이 저장된 디렉터리를 찾아줍니다.
* 백업 파일이 저장될 디렉터리를 변경할 수 있습니다.

## 사용 방법

### 실행하기
<pre>D:\SC4Backup>SC4Backup.exe [-v|-y]</pre>

### 옵션 목록
`-v` : 버전 표시 <br>
`-y` : 건물, 도시, 스크린샷을 백업할 지 물어보지 않고 백업

### 설정 변경
`scb.cfg` 파일을 수정합니다. 처음 실행하면, 자동으로 심시티의 유저 데이터가 저장된 디렉터리를 찾습니다. 백업 파일이 저장될 디렉터리는 이 프로그램을 실행한 디렉터리로 지정됩니다. 다음은 `scb.cfg` 파일의 구조와 설명입니다.

<pre>SRC_DIR=C:\Users\hahaf\Documents\SimCity 4\
DEST_DIR=C:\Users\hahaf\Documents\</pre>

`SRC_DIR` : 심시티 유저 데이터가 저장된 디렉터리<br>
`DEST_DIR` : 백업 파일을 저장할 디렉터리

(English)

SimCity 4 User Data Backup program for Windows. (For personal use)

This script supports:
* Making a plugin/region/screenshot backup with zipfile library(python).
* Choosing whether to make a backup of plugin/regions/screenshots.
* Automatically find plugin/region/screenshot directory.
* You can change destination directory where your backup file will be stored.

## How To Use

### Execute The Program
<pre>D:\SC4Backup>SC4Backup.exe [-v|-y]</pre>

### Options
`-v` : Display the version of this program <br>
`-y` : Backup user data without asking you what you want to backup.

### Modify Configurations
Edit `scb.cfg` file. If you execute this program for the first time, it will find the directory where the user data of SimCity 4 are stored. Current directory will be designated to the directory where backup files are stored. Following are the structure and the description of `scb.cfg` file.

<pre>SRC_DIR=C:\Users\hahaf\Documents\SimCity 4\
DEST_DIR=C:\Users\hahaf\Documents\</pre>

`SRC_DIR` : Directory which user data of SimCity 4 are stored.<br>
`DEST_DIR` : Directory where your backup files will be stored.
