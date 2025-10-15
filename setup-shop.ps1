# ===================================================================
# Shop Setup Script
# ===================================================================
# 이 스크립트는 템플릿에서 새로운 상점을 설정합니다.
# ===================================================================

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "   Shop Configuration Setup" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# 사용자 입력 받기
Write-Host "상점 정보를 입력해주세요:" -ForegroundColor Yellow
Write-Host ""

$shopName = Read-Host "상점명 (예: ABC Shop)"
$shopNameDisplay = Read-Host "상점 표시명 (예: 🌺 ABC SHOP 🌺)"
$adminUsername = Read-Host "관리자 아이디"
$adminPassword = Read-Host "관리자 비밀번호"
$googleSheetGid = Read-Host "구글 시트 GID"

Write-Host ""
Write-Host "입력하신 정보:" -ForegroundColor Green
Write-Host "  상점명: $shopName" -ForegroundColor White
Write-Host "  표시명: $shopNameDisplay" -ForegroundColor White
Write-Host "  관리자: $adminUsername / $adminPassword" -ForegroundColor White
Write-Host "  시트 GID: $googleSheetGid" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "이 정보로 설정하시겠습니까? (Y/N)"
if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "설정이 취소되었습니다." -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "설정 중..." -ForegroundColor Yellow

# app.py 파일 수정
Write-Host "  [1/3] app.py 수정 중..." -ForegroundColor Cyan
$appPyContent = Get-Content "app.py" -Raw -Encoding UTF8

# 페이지 타이틀 변경
$appPyContent = $appPyContent -replace 'page_title="OUR Shop"', "page_title=`"$shopName`""

# 관리자 계정 변경
$appPyContent = $appPyContent -replace 'ADMIN_USERNAME = "our"', "ADMIN_USERNAME = `"$adminUsername`""
$appPyContent = $appPyContent -replace 'ADMIN_PASSWORD = "our123"', "ADMIN_PASSWORD = `"$adminPassword`""

# 구글 시트 GID 변경
$appPyContent = $appPyContent -replace 'gid = "531747363"', "gid = `"$googleSheetGid`""

# 기본 상점명 변경
$appPyContent = $appPyContent -replace "'shop_name': '🌺 OUR SHOP 🌺'", "'shop_name': '$shopNameDisplay'"
$appPyContent = $appPyContent -replace "'company_name': 'OUR Shop'", "'company_name': '$shopName'"

# 파일 저장
[System.IO.File]::WriteAllText("$PWD\app.py", $appPyContent, [System.Text.UTF8Encoding]::new($false))

# README.md 파일 수정
Write-Host "  [2/3] README.md 수정 중..." -ForegroundColor Cyan
$readmeContent = Get-Content "README.md" -Raw -Encoding UTF8
$readmeContent = $readmeContent -replace 'OUR Shop', $shopName
$readmeContent = $readmeContent -replace 'our / our123', "$adminUsername / $adminPassword"
[System.IO.File]::WriteAllText("$PWD\README.md", $readmeContent, [System.Text.UTF8Encoding]::new($false))

# .streamlit 디렉토리 확인
Write-Host "  [3/3] Streamlit 설정 확인 중..." -ForegroundColor Cyan
if (-not (Test-Path ".streamlit")) {
    New-Item -Path ".streamlit" -ItemType Directory | Out-Null
}
if (-not (Test-Path ".streamlit\config.toml")) {
    @"
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
"@ | Out-File -FilePath ".streamlit\config.toml" -Encoding UTF8
}

Write-Host ""
Write-Host "=======================================" -ForegroundColor Green
Write-Host "   설정 완료!" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host ""
Write-Host "다음 단계:" -ForegroundColor Yellow
Write-Host "  1. image 폴더에 상품 이미지를 넣으세요 (1, 2, 3... 폴더)" -ForegroundColor White
Write-Host "  2. 구글 시트에 상품 정보를 입력하세요" -ForegroundColor White
Write-Host "  3. Git 커밋 및 푸시:" -ForegroundColor White
Write-Host "     git add ." -ForegroundColor Gray
Write-Host "     git commit -m 'Setup $shopName'" -ForegroundColor Gray
Write-Host "     git push" -ForegroundColor Gray
Write-Host "  4. Streamlit Cloud에서 Deploy 클릭" -ForegroundColor White
Write-Host ""
Write-Host "관리자 로그인 정보:" -ForegroundColor Cyan
Write-Host "  아이디: $adminUsername" -ForegroundColor White
Write-Host "  비밀번호: $adminPassword" -ForegroundColor White
Write-Host ""

