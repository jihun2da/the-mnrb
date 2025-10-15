# ⚡ 5분 만에 새 상점 만들기

## 🎯 전제 조건
- ✅ `shop-template`이 GitHub에 템플릿 저장소로 등록되어 있어야 함
- ✅ 구글 시트 준비 (상품명, 옵션, 가격)
- ✅ 상품 이미지 준비 (폴더별로 정리)

---

## 🚀 빠른 생성 절차

### 1️⃣ GitHub에서 새 저장소 만들기 (30초)

1. https://github.com/사용자명/shop-template 접속
2. **"Use this template"** 버튼 클릭
3. **"Create a new repository"** 선택
4. 저장소 이름 입력 (예: `abc-shop`)
5. **Public** 선택
6. **"Create repository"** 클릭

---

### 2️⃣ 로컬에 클론 (30초)

```powershell
cd c:\wepapp
git clone https://github.com/사용자명/abc-shop.git
cd abc-shop
```

---

### 3️⃣ 상점 설정 (1분)

```powershell
.\setup-shop.ps1
```

**입력 예시:**
```
상점명: ABC Shop
표시명: 🛍️ ABC SHOP 🛍️
관리자 아이디: abc
관리자 비밀번호: abc123
구글 시트 GID: 123456789
```

> 💡 GID는 구글 시트 URL에서 `gid=숫자` 부분

---

### 4️⃣ 상품 이미지 추가 (2분)

```powershell
# image 폴더에 상품 이미지 복사
# 예시:
# image/1/image_1.jpg, image_2.jpg...
# image/2/image_1.jpg, image_2.jpg...
```

**중요**: 폴더명은 **숫자**로! (1, 2, 3...)

---

### 5️⃣ GitHub에 푸시 (30초)

```powershell
git add .
git commit -m "Setup ABC Shop"
git push
```

---

### 6️⃣ Streamlit Cloud 배포 (1분)

1. https://streamlit.io/cloud 접속
2. **"New app"** 클릭
3. 저장소 선택: `사용자명/abc-shop`
4. **Main file path**: `app.py`
5. **Deploy!** 클릭

⏱️ **배포 대기**: 2-3분

---

## ✅ 완료!

### 접속 URL
- `https://abc-shop.streamlit.app/`

### 관리자 페이지
- 우측 하단 ⚙️ 버튼 클릭
- 아이디/비밀번호 입력

---

## 🔄 여러 상점 만들기

**동일한 과정 반복:**

| 상점명 | 저장소 | URL | 시간 |
|--------|--------|-----|------|
| ABC Shop | abc-shop | abc-shop.streamlit.app | 5분 |
| DEF Shop | def-shop | def-shop.streamlit.app | 5분 |
| GHI Shop | ghi-shop | ghi-shop.streamlit.app | 5분 |

**10개 상점 = 50분 만에 완성!** ⚡

---

## 💡 Pro Tips

### 배치 작업
여러 상점을 한 번에 만들 때:
1. 모든 저장소를 먼저 GitHub에서 생성
2. 로컬에 모두 클론
3. 각각 setup-shop.ps1 실행
4. 이미지 한 번에 복사
5. 한 번에 모두 푸시

### 이미지 준비
미리 폴더별로 정리:
```
준비 폴더/
  ├── abc-shop-images/
  │   ├── 1/
  │   ├── 2/
  │   └── 3/
  ├── def-shop-images/
  │   ├── 1/
  │   ├── 2/
  │   └── 3/
  └── ...
```

### 구글 시트
한 파일에 여러 시트 생성:
- Sheet1: ABC 상품
- Sheet2: DEF 상품
- Sheet3: GHI 상품

각 시트의 GID를 setup-shop.ps1에 입력

---

## ❓ 자주 묻는 질문

**Q: 템플릿을 수정하면?**
A: 기존에 만든 상점에는 영향 없음. 새로 만드는 상점에만 적용됨.

**Q: 여러 상점의 이미지를 한 곳에서 관리?**
A: 각 저장소는 독립적. 하지만 심볼릭 링크나 공유 폴더 활용 가능.

**Q: 상점 삭제는?**
A: GitHub 저장소 삭제 → Streamlit Cloud에서 앱 삭제

**Q: 비용은?**
A: 
- GitHub: 무료 (Public 저장소)
- Streamlit Cloud: 무료 (Community 플랜)
- 제한: 각 상점당 동시 접속자 20-30명

---

**즐거운 상점 만들기 되세요! 🎊**

