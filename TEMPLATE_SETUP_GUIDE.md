# 📚 템플릿 저장소 설정 가이드

## 🎯 목표
`shop-template`을 GitHub에 업로드하고 템플릿 저장소로 설정하기

---

## 📝 Step 1: GitHub 저장소 생성

### 1-1. GitHub 웹사이트 접속
- https://github.com 로그인

### 1-2. 새 저장소 만들기
1. 우측 상단 **"+"** 클릭
2. **"New repository"** 선택
3. 저장소 설정:
   - **Repository name**: `shop-template`
   - **Description**: "Streamlit 기반 온라인 쇼핑몰 템플릿"
   - **Public** 선택 (중요!)
   - ❌ **README 파일 체크 안 함** (이미 있음)
   - ❌ **.gitignore 체크 안 함** (이미 있음)
   - ❌ **License 체크 안 함** (이미 있음)
4. **"Create repository"** 클릭

---

## 🚀 Step 2: 로컬에서 GitHub로 푸시

### 2-1. 터미널에서 실행 (현재 위치: c:\wepapp\shop-template)

```powershell
# 원격 저장소 추가 (본인의 GitHub 사용자명으로 변경)
git remote add origin https://github.com/사용자명/shop-template.git

# 브랜치 이름 확인 및 변경
git branch -M main

# GitHub에 푸시
git push -u origin main
```

### 2-2. 인증
- GitHub 사용자명과 Personal Access Token 입력
- (Token이 없으면 GitHub Settings → Developer settings → Personal access tokens에서 생성)

---

## ⭐ Step 3: 템플릿 저장소로 설정

### 3-1. GitHub 웹사이트에서 설정

1. 방금 만든 저장소 페이지 이동
   - `https://github.com/사용자명/shop-template`

2. 상단 탭에서 **"Settings"** 클릭

3. 왼쪽 메뉴에서 **"General"** 선택 (기본 선택됨)

4. 맨 위 "General" 섹션에서:
   - ☑️ **"Template repository"** 체크박스 선택
   
5. **"Save"** 또는 자동 저장 확인

---

## 🎉 Step 4: 완료 확인

### 4-1. 템플릿 저장소 확인
- 저장소 메인 페이지로 돌아가면
- 저장소 이름 옆에 **"Template"** 배지가 표시됨
- "Use this template" 버튼이 생성됨

### 4-2. 첫 번째 샵 만들기 테스트

1. **"Use this template"** 버튼 클릭
2. **"Create a new repository"** 선택
3. 새 저장소 이름 입력 (예: `abc-shop`)
4. **"Create repository"** 클릭
5. 로컬에 클론:
   ```powershell
   cd c:\wepapp
   git clone https://github.com/사용자명/abc-shop.git
   cd abc-shop
   ```
6. 설정 스크립트 실행:
   ```powershell
   .\setup-shop.ps1
   ```
7. 이미지 추가 및 Git 푸시
8. Streamlit Cloud 배포

---

## 💡 팁

### Personal Access Token 생성 방법
1. GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. "Generate new token" → "Generate new token (classic)"
4. Note: "Shop Template Token"
5. 권한 선택: ☑️ `repo` (전체 선택)
6. "Generate token"
7. 토큰 복사 (다시 볼 수 없으니 안전한 곳에 저장!)

### SSH 사용 (선택사항)
SSH를 설정하면 매번 인증할 필요 없음:
```powershell
git remote set-url origin git@github.com:사용자명/shop-template.git
```

---

## ❓ 문제 해결

### "remote origin already exists" 에러
```powershell
git remote remove origin
git remote add origin https://github.com/사용자명/shop-template.git
```

### 푸시 권한 에러
- Personal Access Token 권한 확인
- 토큰이 만료되지 않았는지 확인

### "Template repository" 옵션이 안 보임
- 저장소가 Public인지 확인 (Private은 유료)
- GitHub 계정이 인증되었는지 확인

---

## 🎊 다음 단계

템플릿 설정이 완료되면:

1. **팀원과 공유**
   - 저장소 URL 공유: `https://github.com/사용자명/shop-template`
   - "Use this template" 버튼으로 각자 상점 만들기

2. **백업**
   - 정기적으로 템플릿 업데이트
   - 버전 태그 활용 (v1.0, v1.1 등)

3. **커스터마이징**
   - 템플릿에 회사 로고 추가
   - 기본 색상 변경
   - 추가 기능 개발

---

**축하합니다! 🎉**
이제 몇 분 만에 새로운 상점을 무한대로 만들 수 있습니다!

