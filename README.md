# 🛍️ Shop Template

**Streamlit 기반 온라인 쇼핑몰 템플릿**

이 템플릿을 사용하면 몇 분 만에 나만의 온라인 상점을 만들 수 있습니다!

---

## ✨ 주요 기능

- 📦 **상품 관리**: 이미지와 정보를 쉽게 관리
- 🔐 **관리자 페이지**: 배너, 공지사항, 상품 등록 관리
- 📊 **구글 시트 연동**: 상품 정보 실시간 업데이트
- 📱 **반응형 디자인**: 모바일/PC 모두 지원
- 💾 **이미지 다운로드**: 고객이 상품 이미지 다운로드 가능
- 📧 **문의 시스템**: 고객 문의 접수 및 관리

---

## 🚀 빠른 시작

### 1. 이 템플릿 사용하기

GitHub에서:
1. **"Use this template"** 버튼 클릭
2. 새 저장소 이름 입력 (예: `my-shop`)
3. **"Create repository"** 클릭

### 2. 로컬에 클론

```bash
git clone https://github.com/사용자명/my-shop.git
cd my-shop
```

### 3. 상점 설정

PowerShell에서:
```powershell
.\setup-shop.ps1
```

입력 사항:
- 상점명 (예: ABC Shop)
- 상점 표시명 (예: 🌺 ABC SHOP 🌺)
- 관리자 아이디
- 관리자 비밀번호
- 구글 시트 GID

### 4. 상품 이미지 추가

`image` 폴더에 상품 이미지를 넣으세요:
```
image/
  ├── 1/           # 첫 번째 상품
  │   ├── image_1.jpg
  │   ├── image_2.jpg
  │   └── ...
  ├── 2/           # 두 번째 상품
  │   └── ...
  └── ...
```

### 5. 구글 시트 설정

1. [구글 시트 생성](https://docs.google.com/spreadsheets/)
2. 다음 형식으로 입력:
   - **A열**: 상품명
   - **B열**: 옵션 (색상/사이즈)
   - **C열**: 가격
3. **파일 → 공유 → 링크가 있는 모든 사용자**로 설정
4. URL에서 `gid=숫자` 부분 복사

### 6. Git 푸시

```bash
git add .
git commit -m "Setup my shop"
git push
```

### 7. Streamlit Cloud 배포

1. [Streamlit Cloud](https://streamlit.io/cloud) 접속
2. **"New app"** 클릭
3. 저장소 선택
4. **Main file path**: `app.py`
5. **Deploy!** 클릭

---

## 📁 프로젝트 구조

```
my-shop/
├── app.py                 # 메인 애플리케이션
├── requirements.txt       # Python 패키지
├── setup-shop.ps1        # 자동 설정 스크립트
├── .gitignore            # Git 무시 파일
├── .streamlit/
│   └── config.toml       # Streamlit 설정
├── data/                 # 동적 데이터 (자동 생성)
│   ├── settings.json     # 상점 설정
│   └── inquiries.json    # 고객 문의
└── image/                # 상품 이미지
    ├── 1/
    ├── 2/
    └── ...
```

---

## 🔧 수동 설정 (선택사항)

자동 스크립트를 사용하지 않으려면:

### app.py 수정

```python
# 페이지 설정 (15-20번 라인)
st.set_page_config(
    page_title="내 상점명",  # 여기 수정
    ...
)

# 관리자 계정 (29-31번 라인)
ADMIN_USERNAME = "admin"     # 여기 수정
ADMIN_PASSWORD = "password"  # 여기 수정

# 구글 시트 (302-304번 라인)
gid = "구글시트GID"  # 여기 수정
```

---

## 📊 관리자 페이지

관리자 페이지 접속:
- 메인 페이지 우측 하단 **⚙️ 관리자 페이지** 버튼 클릭

기능:
- 🏪 **상점명 & 배너**: 상점명, 배너 이미지, 슬라이드 시간 설정
- 📢 **공지사항**: 공지사항 작성/수정
- 📦 **상품 관리**: 새 상품 등록, 기존 상품 이미지 관리
- 🏢 **사업자 정보**: 사업자 정보 입력
- 📝 **문의 양식**: 문의 양식 커스터마이징
- 📧 **문의 내역**: 고객 문의 확인
- 🔄 **Git 업데이트**: 변경사항 GitHub에 푸시

---

## 🛠️ 기술 스택

- **Framework**: Streamlit
- **Language**: Python 3.8+
- **Dependencies**:
  - streamlit >= 1.32.0
  - pandas >= 2.0.0
  - Pillow >= 10.0.0

---

## 📝 라이센스

MIT License - 자유롭게 사용, 수정, 배포 가능

---

## 💡 팁

### 이미지 최적화
- 권장 크기: 800x800 ~ 1200x1200px
- 파일 크기: 500KB 이하 권장
- 형식: JPG (PNG도 지원)

### 상품 수
- 무료 플랜: 최대 50개 상품 권장
- 유료 플랜: 제한 없음

### 동시 접속자
- Community 플랜: 20-30명
- Starter 플랜: 100-200명
- Team 플랜: 500명+

---

## 🆘 문제 해결

### 이미지가 순서대로 안 나와요
→ 폴더명이 숫자인지 확인 (1, 2, 3... 순서)

### 구글 시트 연동이 안 돼요
→ 시트 공유 설정이 "링크가 있는 모든 사용자"로 되어있는지 확인

### 관리자 로그인이 안 돼요
→ `setup-shop.ps1` 실행 시 설정한 ID/PW 확인

---

## 📞 지원

문제가 있으시면 GitHub Issues에 등록해주세요!

---

**Made with ❤️ using Streamlit**
