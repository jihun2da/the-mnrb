import streamlit as st
import pandas as pd
from pathlib import Path
import os
from PIL import Image
import json
import subprocess
from datetime import datetime
import time
import base64
import zipfile
import io

# 페이지 설정
st.set_page_config(
    page_title="OUR Shop",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 데이터 디렉토리 생성
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# 이미지 디렉토리
IMAGE_DIR = Path("image")

# 관리자 계정 정보
ADMIN_USERNAME = "our"
ADMIN_PASSWORD = "our123"

# CSS 스타일링
st.markdown("""
<style>
    /* 전체 페이지 스타일 */
    .main {
        background-color: #ffffff;
    }
    
    /* 헤더 스타일 */
    .header {
        background-color: #000000;
        color: white;
        padding: 20px;
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 30px;
    }
    
    /* 배너 슬라이드 스타일 */
    .banner-slider {
        position: relative;
        width: 100%;
        height: 400px;
        overflow: hidden;
        margin-bottom: 40px;
        border-radius: 12px;
    }
    
    .banner-slide {
        display: none;
        width: 100%;
        height: 100%;
        object-fit: cover;
        animation: fadeIn 1s;
    }
    
    .banner-slide.active {
        display: block;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .slider-dots {
        text-align: center;
        padding: 10px;
        position: absolute;
        bottom: 20px;
        width: 100%;
    }
    
    .dot {
        height: 12px;
        width: 12px;
        margin: 0 5px;
        background-color: #bbb;
        border-radius: 50%;
        display: inline-block;
        transition: background-color 0.3s;
    }
    
    .dot.active {
        background-color: #fff;
    }
    
    /* 공지사항 스타일 */
    .notice-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 40px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .notice-title {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .notice-content {
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* 상품 카드 스타일 */
    .product-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        background-color: white;
        height: 100%;
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .product-name {
        font-size: 16px;
        font-weight: 600;
        margin-top: 10px;
        color: #333;
    }
    
    .product-info {
        font-size: 14px;
        color: #666;
        margin-top: 5px;
    }
    
    .product-price {
        font-size: 18px;
        font-weight: bold;
        color: #e91e63;
        margin-top: 8px;
    }
    
    /* 푸터 스타일 */
    .footer {
        background-color: #2c3e50;
        color: white;
        padding: 40px 20px;
        margin-top: 60px;
        border-radius: 12px 12px 0 0;
    }
    
    .footer-section {
        margin-bottom: 20px;
    }
    
    .footer-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
        color: #ecf0f1;
    }
    
    .footer-content {
        font-size: 14px;
        line-height: 1.8;
        color: #bdc3c7;
    }
    
    .inquiry-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 30px;
        border-radius: 25px;
        border: none;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: transform 0.3s;
        display: inline-block;
        text-decoration: none;
    }
    
    .inquiry-button:hover {
        transform: scale(1.05);
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #000000;
        color: white;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stButton>button:hover {
        background-color: #333333;
    }
    
    /* 로그인 폼 스타일 */
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 40px;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        background-color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# 세션 스테이트 초기화
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

# 설정 파일 로드/저장 함수
def load_settings():
    settings_file = DATA_DIR / "settings.json"
    if settings_file.exists():
        with open(settings_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "banner_slide_interval": 3,
        "banners": [],
        "shop_name": "🌺 OAHU SHOP 🌺",
        "shop_name_font_size": 48,
        "shop_name_color": "#333333",
        "notice": {
            "title": "공지사항",
            "content": "신상품이 입고되었습니다!",
            "enabled": True
        },
        "business_info": {
            "company_name": "OAHU Shop",
            "ceo_name": "대표자명",
            "business_number": "123-45-67890",
            "address": "서울특별시 강남구",
            "phone": "02-1234-5678",
            "kakao_id": "",
            "instagram_id": "",
            "wechat_id": "",
            "enabled": True
        },
        "inquiry_form_fields": [
            {"id": "name", "label": "이름", "type": "text", "required": True},
            {"id": "email", "label": "이메일", "type": "email", "required": True},
            {"id": "phone", "label": "연락처", "type": "text", "required": False},
            {"id": "subject", "label": "문의 제목", "type": "text", "required": True},
            {"id": "message", "label": "문의 내용", "type": "textarea", "required": True}
        ]
    }

def save_settings(settings):
    settings_file = DATA_DIR / "settings.json"
    with open(settings_file, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

# 문의사항 로드/저장 함수
def load_inquiries():
    inquiry_file = DATA_DIR / "inquiries.json"
    if inquiry_file.exists():
        with open(inquiry_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"inquiries": []}

def save_inquiry(inquiry_data):
    inquiries = load_inquiries()
    inquiry_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    inquiry_data['id'] = len(inquiries['inquiries']) + 1
    inquiries['inquiries'].append(inquiry_data)
    
    inquiry_file = DATA_DIR / "inquiries.json"
    with open(inquiry_file, 'w', encoding='utf-8') as f:
        json.dump(inquiries, f, ensure_ascii=False, indent=2)

# 구글 시트 데이터 로드
@st.cache_data
def load_google_sheet_data():
    try:
        sheet_id = "1Cnd19QAMyNEgvEdfXTA1QtW0VMiTRMCBFGmrzKWezNQ"
        gid = "531747363"  # OUR 시트
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame({
            'A': [f'상품 {i}' for i in range(126, 152)],
            'B': [f'색상/사이즈 정보 {i}' for i in range(126, 152)],
            'C': [f'{50000 + i*1000}원' for i in range(26)]
        })

# 이미지 폴더 스캔
def get_product_folders():
    image_path = Path("image")
    if not image_path.exists():
        return []
    folders = [f for f in image_path.iterdir() if f.is_dir()]
    # 숫자 폴더명은 숫자로 정렬, 그 외는 문자열로 정렬
    folders = sorted(folders, key=lambda f: int(f.name) if f.name.isdigit() else float('inf'))
    return folders

# 폴더의 이미지 파일 가져오기
def get_folder_images(folder_path):
    images = sorted([f for f in folder_path.glob("*.jpg") if f.name != "ㅎ.jpg"])
    return images

# 썸네일 이미지 가져오기 (두 번째 이미지)
def get_thumbnail(folder_path):
    images = get_folder_images(folder_path)
    if len(images) >= 2:
        return images[1]
    elif len(images) > 0:
        return images[0]
    return None

# 이미지를 base64로 인코딩
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# 배너 슬라이더 표시
def show_banner_slider(settings):
    banners = settings.get('banners', [])
    
    if not banners:
        # 기본 배너
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    height: 300px; display: flex; align-items: center; justify-content: center;
                    margin-bottom: 40px; border-radius: 12px;">
            <h1 style="color: white; font-size: 48px; font-weight: bold;">NEW ARRIVALS</h1>
        </div>
        """, unsafe_allow_html=True)
        return
    
    slide_interval = settings.get('banner_slide_interval', 3) * 1000
    
    # 배너 이미지들 표시
    banner_container = st.container()
    with banner_container:
        # JavaScript로 슬라이드 구현
        banner_html = '<div class="banner-slider">'
        
        for idx, banner in enumerate(banners):
            active_class = "active" if idx == 0 else ""
            banner_html += f'<img src="data:image/jpeg;base64,{banner}" class="banner-slide {active_class}" id="slide{idx}">'
        
        # 슬라이드 인디케이터
        banner_html += '<div class="slider-dots">'
        for idx in range(len(banners)):
            active_class = "active" if idx == 0 else ""
            banner_html += f'<span class="dot {active_class}" id="dot{idx}"></span>'
        banner_html += '</div></div>'
        
        # JavaScript 슬라이드 로직
        banner_html += f"""
        <script>
        let slideIndex = 0;
        const slides = document.getElementsByClassName("banner-slide");
        const dots = document.getElementsByClassName("dot");
        
        function showSlides() {{
            for (let i = 0; i < slides.length; i++) {{
                slides[i].classList.remove("active");
                dots[i].classList.remove("active");
            }}
            slideIndex++;
            if (slideIndex > slides.length) {{slideIndex = 1}}
            slides[slideIndex-1].classList.add("active");
            dots[slideIndex-1].classList.add("active");
            setTimeout(showSlides, {slide_interval});
        }}
        
        showSlides();
        </script>
        """
        
        st.markdown(banner_html, unsafe_allow_html=True)

# 공지사항 표시
def show_notice(settings):
    notice = settings.get('notice', {})
    if notice.get('enabled', False):
        st.markdown(f"""
        <div class="notice-box">
            <div class="notice-title">📢 {notice.get('title', '공지사항')}</div>
            <div class="notice-content">{notice.get('content', '')}</div>
        </div>
        """, unsafe_allow_html=True)

# 푸터 표시
def show_footer(settings):
    business_info = settings.get('business_info', {})
    
    if business_info.get('enabled', False):
        # 사업자 정보 구성
        company_name = business_info.get('company_name', 'OAHU Shop')
        ceo_name = business_info.get('ceo_name', '')
        business_number = business_info.get('business_number', '')
        address = business_info.get('address', '')
        phone = business_info.get('phone', '')
        kakao_id = business_info.get('kakao_id', '')
        instagram_id = business_info.get('instagram_id', '')
        wechat_id = business_info.get('wechat_id', '')
        
        # HTML 생성
        footer_html = '<div class="footer"><div class="footer-section"><div class="footer-title">🏢 사업자 정보</div><div class="footer-content">'
        footer_html += f'상호: {company_name}<br>'
        footer_html += f'대표자: {ceo_name}<br>'
        footer_html += f'사업자등록번호: {business_number}<br>'
        footer_html += f'주소: {address}<br>'
        footer_html += f'전화: {phone}'
        
        if kakao_id:
            footer_html += f'<br>카카오톡: {kakao_id}'
        if instagram_id:
            footer_html += f'<br>인스타그램: {instagram_id}'
        if wechat_id:
            footer_html += f'<br>위챗: {wechat_id}'
        
        footer_html += '</div></div></div>'
        
        st.markdown(footer_html, unsafe_allow_html=True)
    
    # 문의하기 버튼
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📧 문의하기", use_container_width=True):
            st.session_state.page = 'inquiry'
            st.rerun()

# 메인 페이지
def show_main_page():
    settings = load_settings()
    
    # 헤더 (상점명)
    shop_name = settings.get('shop_name', '🌺 OAHU SHOP 🌺')
    shop_name_font_size = settings.get('shop_name_font_size', 48)
    shop_name_color = settings.get('shop_name_color', '#333333')
    
    st.markdown(f'''
    <div class="header" style="font-size: {shop_name_font_size}px !important; color: {shop_name_color} !important;">
        {shop_name}
    </div>
    ''', unsafe_allow_html=True)
    
    # 배너 슬라이더
    show_banner_slider(settings)
    
    # 공지사항
    show_notice(settings)
    
    # 데이터 로드
    df = load_google_sheet_data()
    folders = get_product_folders()
    
    if not folders:
        st.warning("상품 폴더를 찾을 수 없습니다.")
        return
    
    st.markdown("### 신상품")
    st.markdown("---")
    
    # 3열 그리드로 상품 표시
    cols_per_row = 3
    for i in range(0, len(folders), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j, col in enumerate(cols):
            idx = i + j
            if idx >= len(folders):
                break
            
            folder = folders[idx]
            folder_num = folder.name
            
            with col:
                # 썸네일 이미지
                thumbnail = get_thumbnail(folder)
                if thumbnail:
                    try:
                        img = Image.open(thumbnail)
                        st.image(img, use_container_width=True)
                    except:
                        st.info("이미지를 불러올 수 없습니다.")
                
                # 상품 정보
                row_idx = idx
                if row_idx < len(df):
                    product_name = df.iloc[row_idx, 0] if len(df.columns) > 0 else f"상품 {folder_num}"
                    product_info = df.iloc[row_idx, 1] if len(df.columns) > 1 else "정보 없음"
                    product_price = df.iloc[row_idx, 2] if len(df.columns) > 2 else "가격 문의"
                else:
                    product_name = f"상품 {folder_num}"
                    product_info = "정보 없음"
                    product_price = "가격 문의"
                
                st.markdown(f'<div class="product-name">{product_name}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="product-info">{product_info}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="product-price">{product_price}</div>', unsafe_allow_html=True)
                
                if st.button("상세보기", key=f"btn_{folder_num}"):
                    st.session_state.selected_product = folder
                    st.session_state.page = 'detail'
                    st.rerun()
    
    # 푸터
    show_footer(settings)
    
    # 관리자 로그인 링크
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔐 관리자 페이지"):
            st.session_state.page = 'login'
            st.rerun()

# 상품 상세 페이지
def show_detail_page():
    if not st.session_state.selected_product:
        st.session_state.page = 'home'
        st.rerun()
        return
    
    folder = st.session_state.selected_product
    folder_num = folder.name
    
    # 뒤로가기 버튼
    if st.button("← 목록으로 돌아가기"):
        st.session_state.page = 'home'
        st.session_state.selected_product = None
        st.rerun()
    
    st.markdown("---")
    
    # 상품 정보
    df = load_google_sheet_data()
    folders = get_product_folders()
    folder_idx = folders.index(folder) if folder in folders else 0
    
    if folder_idx < len(df):
        product_name = df.iloc[folder_idx, 0] if len(df.columns) > 0 else f"상품 {folder_num}"
        product_info = df.iloc[folder_idx, 1] if len(df.columns) > 1 else "정보 없음"
        product_price = df.iloc[folder_idx, 2] if len(df.columns) > 2 else "가격 문의"
    else:
        product_name = f"상품 {folder_num}"
        product_info = "정보 없음"
        product_price = "가격 문의"
    
    st.markdown(f"# {product_name}")
    st.markdown(f"**색상/사이즈:** {product_info}")
    st.markdown(f"**가격:** {product_price}")
    st.markdown("---")
    
    # 이미지 갤러리
    images = get_folder_images(folder)
    
    if not images:
        st.warning("상품 이미지가 없습니다.")
        return
    
    # 전체 이미지 다운로드 버튼
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # ZIP 파일 생성
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for img_path in images:
                zip_file.write(img_path, img_path.name)
        
        zip_buffer.seek(0)
        
        st.download_button(
            label="📦 전체 이미지 다운로드 (ZIP)",
            data=zip_buffer,
            file_name=f"{product_name}_images.zip",
            mime="application/zip",
            use_container_width=True
        )
    
    st.markdown("---")
    
    # 3열 그리드로 모든 이미지 표시
    cols_per_row = 3
    for i in range(0, len(images), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j, col in enumerate(cols):
            idx = i + j
            if idx >= len(images):
                break
            
            with col:
                try:
                    img = Image.open(images[idx])
                    st.image(img, use_container_width=True, caption=images[idx].name)
                    
                    # 이미지 다운로드 버튼
                    with open(images[idx], 'rb') as file:
                        st.download_button(
                            label="📥 다운로드",
                            data=file,
                            file_name=images[idx].name,
                            mime="image/jpeg",
                            key=f"download_{folder_num}_{idx}",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"이미지 로드 실패: {e}")

# 문의하기 페이지
def show_inquiry_page():
    st.markdown('<div class="header">📧 문의하기</div>', unsafe_allow_html=True)
    
    if st.button("← 메인으로 돌아가기"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown("---")
    
    settings = load_settings()
    form_fields = settings.get('inquiry_form_fields', [])
    
    st.markdown("### 문의사항을 남겨주세요")
    st.markdown("빠른 시일 내에 답변드리겠습니다.")
    
    with st.form("inquiry_form"):
        inquiry_data = {}
        
        for field in form_fields:
            field_id = field['id']
            label = field['label']
            field_type = field['type']
            required = field.get('required', False)
            
            label_text = f"{label} {'*' if required else ''}"
            
            if field_type == "textarea":
                inquiry_data[field_id] = st.text_area(label_text, height=150)
            elif field_type == "email":
                inquiry_data[field_id] = st.text_input(label_text, placeholder="example@email.com")
            else:
                inquiry_data[field_id] = st.text_input(label_text)
        
        submitted = st.form_submit_button("문의하기", use_container_width=True)
        
        if submitted:
            # 필수 필드 검증
            all_filled = True
            for field in form_fields:
                if field.get('required', False) and not inquiry_data.get(field['id']):
                    st.error(f"{field['label']}을(를) 입력해주세요.")
                    all_filled = False
                    break
            
            if all_filled:
                save_inquiry(inquiry_data)
                st.success("문의가 성공적으로 접수되었습니다! 빠른 시일 내에 답변드리겠습니다.")
                time.sleep(2)
                st.session_state.page = 'home'
                st.rerun()

# 로그인 페이지
def show_login_page():
    st.markdown('<div class="header">🔐 관리자 로그인</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        username = st.text_input("아이디", placeholder="아이디를 입력하세요")
        password = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("로그인", use_container_width=True):
                if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                    st.session_state.logged_in = True
                    st.session_state.page = 'admin'
                    st.success("로그인 성공!")
                    st.rerun()
                else:
                    st.error("아이디 또는 비밀번호가 올바르지 않습니다.")
        
        with col_b:
            if st.button("취소", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# 관리자 페이지
def show_admin_page():
    if not st.session_state.logged_in:
        st.session_state.page = 'login'
        st.rerun()
        return
    
    st.markdown('<div class="header">⚙️ 관리자 페이지</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("← 메인 페이지로"):
            st.session_state.page = 'home'
            st.rerun()
    
    with col2:
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.session_state.page = 'home'
            st.rerun()
    
    st.markdown("---")
    
    # 탭 메뉴
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🏪 상점명 & 배너", 
        "📢 공지사항", 
        "📦 상품 관리", 
        "🏢 사업자 정보",
        "📧 문의 양식",
        "💬 문의 내역",
        "🔄 Git 업데이트"
    ])
    
    settings = load_settings()
    
    # 배너 관리 탭
    with tab1:
        st.subheader("상점명 및 배너 설정")
        
        # 상점명 설정
        st.markdown("### 🏪 상점명 설정")
        
        col1, col2 = st.columns(2)
        
        with col1:
            shop_name = st.text_input(
                "상점명",
                value=settings.get('shop_name', '🌺 OAHU SHOP 🌺'),
                help="메인 페이지 상단에 표시될 상점명을 입력하세요"
            )
            
            shop_name_font_size = st.slider(
                "글자 크기",
                min_value=20,
                max_value=100,
                value=settings.get('shop_name_font_size', 48),
                help="상점명 글자 크기를 조절하세요"
            )
        
        with col2:
            shop_name_color = st.color_picker(
                "글자 색상",
                value=settings.get('shop_name_color', '#333333'),
                help="상점명 글자 색상을 선택하세요"
            )
            
            # 미리보기
            st.markdown("**미리보기:**")
            st.markdown(f'''
            <div style="font-size: {shop_name_font_size}px; color: {shop_name_color}; text-align: center; font-weight: bold; padding: 20px;">
                {shop_name}
            </div>
            ''', unsafe_allow_html=True)
        
        if st.button("💾 상점명 설정 저장", use_container_width=True):
            settings['shop_name'] = shop_name
            settings['shop_name_font_size'] = shop_name_font_size
            settings['shop_name_color'] = shop_name_color
            save_settings(settings)
            st.success("✅ 상점명 설정이 저장되었습니다!")
            st.rerun()
        
        st.markdown("---")
        
        # 배너 슬라이드 설정
        st.markdown("### 📸 배너 슬라이드 관리")
        
        # 슬라이드 시간 설정
        slide_interval = st.number_input(
            "슬라이드 전환 시간 (초)",
            min_value=1,
            max_value=10,
            value=settings.get('banner_slide_interval', 3),
            help="배너가 자동으로 전환되는 시간을 설정하세요"
        )
        
        if slide_interval != settings.get('banner_slide_interval', 3):
            settings['banner_slide_interval'] = slide_interval
            save_settings(settings)
            st.success(f"슬라이드 시간이 {slide_interval}초로 설정되었습니다!")
        
        st.markdown("---")
        
        # 배너 이미지 업로드 (다중)
        st.markdown("### 배너 이미지 업로드")
        st.info("최대 5장까지 업로드 가능합니다. 권장 크기: 1920x400px")
        
        uploaded_banners = st.file_uploader(
            "배너 이미지 선택 (여러 장 가능)",
            type=['jpg', 'jpeg', 'png'],
            accept_multiple_files=True,
            key="banner_upload"
        )
        
        if uploaded_banners:
            st.markdown("### 미리보기")
            cols = st.columns(min(len(uploaded_banners), 3))
            for idx, uploaded_file in enumerate(uploaded_banners[:5]):
                with cols[idx % 3]:
                    st.image(uploaded_file, use_container_width=True)
            
            if st.button("배너 적용", use_container_width=True):
                banner_list = []
                for uploaded_file in uploaded_banners[:5]:
                    bytes_data = uploaded_file.read()
                    base64_img = base64.b64encode(bytes_data).decode()
                    banner_list.append(base64_img)
                
                settings['banners'] = banner_list
                save_settings(settings)
                st.success(f"{len(banner_list)}장의 배너가 업데이트되었습니다!")
                st.rerun()
        
        # 현재 배너 표시
        st.markdown("---")
        st.markdown("### 현재 등록된 배너")
        current_banners = settings.get('banners', [])
        
        if current_banners:
            st.info(f"총 {len(current_banners)}장의 배너가 등록되어 있습니다.")
            
            cols = st.columns(min(len(current_banners), 3))
            for idx, banner_base64 in enumerate(current_banners):
                with cols[idx % 3]:
                    st.image(f"data:image/jpeg;base64,{banner_base64}", use_container_width=True)
            
            if st.button("모든 배너 제거", type="secondary"):
                settings['banners'] = []
                save_settings(settings)
                st.success("모든 배너가 제거되었습니다!")
                st.rerun()
        else:
            st.warning("등록된 배너가 없습니다. 기본 배너가 표시됩니다.")
    
    # 공지사항 관리 탭
    with tab2:
        st.subheader("공지사항 관리")
        
        notice = settings.get('notice', {})
        
        notice_enabled = st.checkbox(
            "공지사항 표시",
            value=notice.get('enabled', True)
        )
        
        notice_title = st.text_input(
            "공지사항 제목",
            value=notice.get('title', '공지사항'),
            placeholder="예: 신상품 입고"
        )
        
        notice_content = st.text_area(
            "공지사항 내용",
            value=notice.get('content', ''),
            height=150,
            placeholder="공지사항 내용을 입력하세요..."
        )
        
        if st.button("공지사항 저장", use_container_width=True):
            settings['notice'] = {
                'title': notice_title,
                'content': notice_content,
                'enabled': notice_enabled
            }
            save_settings(settings)
            st.success("공지사항이 저장되었습니다!")
            st.rerun()
        
        # 미리보기
        if notice_enabled:
            st.markdown("---")
            st.markdown("### 미리보기")
            st.markdown(f"""
            <div class="notice-box">
                <div class="notice-title">📢 {notice_title}</div>
                <div class="notice-content">{notice_content}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # 상품 관리 탭
    with tab3:
        st.subheader("상품 정보 관리")
        
        # 상품 업로드 섹션
        st.markdown("### 🆕 새 상품 등록")
        
        with st.form("upload_product_form"):
            # 상품 정보 입력
            product_name = st.text_input("상품명", placeholder="예: 반팔 티셔츠")
            product_info = st.text_input("색상/사이즈", placeholder="예: 블랙/FREE")
            product_price = st.text_input("가격", placeholder="예: 29,000원")
            
            # 이미지 업로드
            uploaded_files = st.file_uploader(
                "상품 이미지 업로드 (여러 장 선택 가능)",
                type=['jpg', 'jpeg', 'png'],
                accept_multiple_files=True,
                help="첫 번째 이미지는 대표 이미지로, 두 번째 이미지는 썸네일로 사용됩니다."
            )
            
            # 폴더 번호 자동 생성 미리보기
            folders = get_product_folders()
            if folders:
                folder_numbers = [int(f.name) for f in folders]
                next_folder_num = max(folder_numbers) + 1
            else:
                next_folder_num = 126
            
            st.info(f"📁 새 상품은 폴더 번호 **{next_folder_num}**에 저장됩니다.")
            
            submit_button = st.form_submit_button("✅ 상품 등록", use_container_width=True)
            
            if submit_button:
                if not product_name or not product_info or not product_price:
                    st.error("❌ 모든 상품 정보를 입력해주세요.")
                elif not uploaded_files:
                    st.error("❌ 최소 1개 이상의 이미지를 업로드해주세요.")
                else:
                    try:
                        # 새 폴더 생성
                        new_folder = IMAGE_DIR / str(next_folder_num)
                        new_folder.mkdir(parents=True, exist_ok=True)
                        
                        # 이미지 저장
                        for idx, uploaded_file in enumerate(uploaded_files, 1):
                            img = Image.open(uploaded_file)
                            img_path = new_folder / f"image_{idx}.jpg"
                            img.save(img_path, "JPEG")
                        
                        st.success(f"""
                        ✅ 상품이 성공적으로 등록되었습니다!
                        
                        - **폴더**: {next_folder_num}
                        - **상품명**: {product_name}
                        - **업로드된 이미지**: {len(uploaded_files)}장
                        
                        이제 [구글 시트](https://docs.google.com/spreadsheets/d/1Cnd19QAMyNEgvEdfXTA1QtW0VMiTRMCBFGmrzKWezNQ/edit?usp=sharing)에 상품 정보를 추가해주세요:
                        - **A열**: {product_name}
                        - **B열**: {product_info}
                        - **C열**: {product_price}
                        """)
                        
                        st.info("💡 구글 시트 업데이트 후 '🔄 상품 정보 새로고침' 버튼을 클릭하세요.")
                        
                    except Exception as e:
                        st.error(f"❌ 상품 등록 중 오류가 발생했습니다: {e}")
        
        st.markdown("---")
        
        # 기존 상품 이미지 수정 섹션
        st.markdown("### 📸 기존 상품 이미지 관리")
        
        folders = get_product_folders()
        if folders and len(folders) > 0:
            folder_names = [f.name for f in folders]
            
            if len(folder_names) > 0:
                selected_folder_name = st.selectbox(
                    "수정할 상품 폴더 선택",
                    options=folder_names,
                    help="이미지를 추가하거나 수정할 상품 폴더를 선택하세요."
                )
                
                if selected_folder_name:
                    try:
                        folder_path = IMAGE_DIR / selected_folder_name
                        
                        if not folder_path.exists():
                            st.error(f"폴더를 찾을 수 없습니다: {selected_folder_name}")
                        else:
                            existing_images = get_folder_images(folder_path)
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown(f"**현재 이미지: {len(existing_images)}장**")
                                if existing_images:
                                    # 썸네일로 현재 이미지 표시
                                    for i, img_path in enumerate(existing_images[:4], 1):
                                        try:
                                            img = Image.open(img_path)
                                            st.image(img, caption=f"image_{i}.jpg", width=100)
                                        except:
                                            pass
                                    if len(existing_images) > 4:
                                        st.info(f"외 {len(existing_images) - 4}장 더 있음")
                            
                            with col2:
                                with st.form(f"update_product_images_{selected_folder_name}"):
                                    st.markdown("**새 이미지 업로드**")
                                    new_images = st.file_uploader(
                                        "추가할 이미지 선택",
                                        type=['jpg', 'jpeg', 'png'],
                                        accept_multiple_files=True,
                                        key=f"uploader_{selected_folder_name}"
                                    )
                                    
                                    replace_mode = st.checkbox("기존 이미지 모두 삭제하고 교체")
                                    
                                    update_button = st.form_submit_button("🔄 이미지 업데이트", use_container_width=True)
                                    
                                    if update_button and new_images:
                                        try:
                                            if replace_mode:
                                                # 기존 이미지 삭제
                                                for img in existing_images:
                                                    img.unlink()
                                                start_idx = 1
                                                st.info("기존 이미지를 모두 삭제했습니다.")
                                            else:
                                                # 기존 이미지 유지, 새 번호부터 시작
                                                start_idx = len(existing_images) + 1
                                            
                                            # 새 이미지 저장
                                            for idx, uploaded_file in enumerate(new_images, start_idx):
                                                img = Image.open(uploaded_file)
                                                img_path = folder_path / f"image_{idx}.jpg"
                                                img.save(img_path, "JPEG")
                                            
                                            st.success(f"✅ {len(new_images)}장의 이미지가 업데이트되었습니다!")
                                            st.rerun()
                                            
                                        except Exception as e:
                                            st.error(f"❌ 이미지 업데이트 중 오류: {e}")
                    except Exception as e:
                        st.error(f"❌ 오류가 발생했습니다: {e}")
            else:
                st.warning("등록된 상품 폴더가 없습니다.")
        else:
            st.warning("등록된 상품이 없습니다.")
        
        st.markdown("---")
        
        # 기존 상품 관리 섹션
        st.markdown("### 📋 등록된 상품 관리")
        
        st.markdown("""
        상품 정보는 구글 시트에서 관리됩니다.
        
        **[구글 시트 바로가기](https://docs.google.com/spreadsheets/d/1Cnd19QAMyNEgvEdfXTA1QtW0VMiTRMCBFGmrzKWezNQ/edit?usp=sharing)**
        
        - **A열**: 상품명
        - **B열**: 색상/사이즈
        - **C열**: 가격
        
        구글 시트에서 정보를 수정한 후 아래 버튼을 클릭하여 새로고침하세요.
        """)
        
        if st.button("🔄 상품 정보 새로고침", use_container_width=True):
            st.cache_data.clear()
            st.success("상품 정보가 새로고침되었습니다!")
            st.rerun()
        
        # 현재 상품 목록 표시
        st.markdown("---")
        st.markdown("#### 현재 등록된 상품 목록")
        df = load_google_sheet_data()
        st.dataframe(df, use_container_width=True)
        
        # 상품 폴더 정보
        st.markdown("---")
        st.markdown("#### 상품 이미지 폴더")
        folders = get_product_folders()
        st.info(f"총 {len(folders)}개의 상품 폴더가 있습니다.")
        
        folder_names = [f.name for f in folders]
        st.write(", ".join(folder_names))
    
    # 사업자 정보 관리 탭
    with tab4:
        st.subheader("사업자 정보 관리")
        
        business_info = settings.get('business_info', {})
        
        business_enabled = st.checkbox(
            "사업자 정보 표시",
            value=business_info.get('enabled', True)
        )
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            company_name = st.text_input(
                "상호",
                value=business_info.get('company_name', 'OAHU Shop')
            )
            ceo_name = st.text_input(
                "대표자",
                value=business_info.get('ceo_name', '')
            )
            business_number = st.text_input(
                "사업자등록번호",
                value=business_info.get('business_number', '')
            )
            address = st.text_input(
                "주소",
                value=business_info.get('address', '')
            )
        
        with col_b:
            phone = st.text_input(
                "전화번호",
                value=business_info.get('phone', '')
            )
            kakao_id = st.text_input(
                "카카오톡 ID",
                value=business_info.get('kakao_id', ''),
                placeholder="예: @oahu_shop"
            )
            instagram_id = st.text_input(
                "인스타그램 ID",
                value=business_info.get('instagram_id', ''),
                placeholder="예: @oahu.official"
            )
            wechat_id = st.text_input(
                "위챗 ID",
                value=business_info.get('wechat_id', ''),
                placeholder="예: oahu_wechat"
            )
        
        if st.button("사업자 정보 저장", use_container_width=True):
            settings['business_info'] = {
                'company_name': company_name,
                'ceo_name': ceo_name,
                'business_number': business_number,
                'address': address,
                'phone': phone,
                'kakao_id': kakao_id,
                'instagram_id': instagram_id,
                'wechat_id': wechat_id,
                'enabled': business_enabled
            }
            save_settings(settings)
            st.success("사업자 정보가 저장되었습니다!")
            st.rerun()
    
    # 문의 양식 관리 탭
    with tab5:
        st.subheader("문의 양식 관리")
        
        st.markdown("문의 페이지에서 고객이 입력할 항목을 설정합니다.")
        
        form_fields = settings.get('inquiry_form_fields', [])
        
        st.markdown("#### 현재 양식 항목")
        
        for idx, field in enumerate(form_fields):
            with st.expander(f"📝 {field['label']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**ID**: {field['id']}")
                    st.write(f"**유형**: {field['type']}")
                    st.write(f"**필수**: {'예' if field.get('required', False) else '아니오'}")
                
                with col2:
                    if st.button("삭제", key=f"del_field_{idx}"):
                        form_fields.pop(idx)
                        settings['inquiry_form_fields'] = form_fields
                        save_settings(settings)
                        st.success("항목이 삭제되었습니다!")
                        st.rerun()
        
        st.markdown("---")
        st.markdown("#### 새 항목 추가")
        
        with st.form("add_field_form"):
            new_field_id = st.text_input("항목 ID (영문, 공백없이)", placeholder="예: product_name")
            new_field_label = st.text_input("항목 라벨", placeholder="예: 관심 상품")
            new_field_type = st.selectbox("항목 유형", ["text", "email", "textarea"])
            new_field_required = st.checkbox("필수 항목")
            
            if st.form_submit_button("항목 추가"):
                if new_field_id and new_field_label:
                    new_field = {
                        'id': new_field_id,
                        'label': new_field_label,
                        'type': new_field_type,
                        'required': new_field_required
                    }
                    form_fields.append(new_field)
                    settings['inquiry_form_fields'] = form_fields
                    save_settings(settings)
                    st.success("새 항목이 추가되었습니다!")
                    st.rerun()
                else:
                    st.error("ID와 라벨을 모두 입력해주세요.")
    
    # 문의 내역 탭
    with tab6:
        st.subheader("고객 문의 내역")
        
        inquiries_data = load_inquiries()
        inquiries_list = inquiries_data.get('inquiries', [])
        
        if inquiries_list:
            st.info(f"총 {len(inquiries_list)}건의 문의가 있습니다.")
            
            for inquiry in reversed(inquiries_list):
                with st.expander(
                    f"📧 {inquiry.get('subject', '제목 없음')} - {inquiry.get('timestamp', '')}",
                    expanded=False
                ):
                    for key, value in inquiry.items():
                        if key not in ['id', 'timestamp']:
                            st.write(f"**{key}**: {value}")
        else:
            st.info("아직 문의 내역이 없습니다.")
    
    # Git 업데이트 탭
    with tab7:
        st.subheader("Git 업데이트")
        
        st.markdown("""
        새 상품 이미지를 추가하거나 파일을 수정한 후 GitHub에 업로드합니다.
        
        **주의**: 이 기능은 로컬 환경에서만 작동합니다.
        Streamlit Cloud에서는 GitHub 웹 인터페이스를 사용하세요.
        """)
        
        commit_message = st.text_input(
            "커밋 메시지",
            value="Update products and settings",
            placeholder="예: Add new product images"
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📝 Git Status", use_container_width=True):
                try:
                    result = subprocess.run(
                        ['git', 'status', '--short'],
                        capture_output=True,
                        text=True,
                        cwd=Path.cwd()
                    )
                    if result.stdout:
                        st.code(result.stdout, language="text")
                    else:
                        st.success("변경사항이 없습니다.")
                except Exception as e:
                    st.error(f"오류: {e}")
        
        with col2:
            if st.button("✅ Git Commit", use_container_width=True):
                try:
                    # Add all changes
                    subprocess.run(['git', 'add', '-A'], check=True, cwd=Path.cwd())
                    
                    # Commit
                    result = subprocess.run(
                        ['git', 'commit', '-m', commit_message],
                        capture_output=True,
                        text=True,
                        cwd=Path.cwd()
                    )
                    
                    if result.returncode == 0:
                        st.success("커밋이 완료되었습니다!")
                        st.code(result.stdout, language="text")
                    else:
                        st.warning("커밋할 변경사항이 없거나 이미 커밋되었습니다.")
                except Exception as e:
                    st.error(f"오류: {e}")
        
        with col3:
            if st.button("🚀 Git Push", use_container_width=True):
                try:
                    result = subprocess.run(
                        ['git', 'push'],
                        capture_output=True,
                        text=True,
                        cwd=Path.cwd()
                    )
                    
                    if result.returncode == 0:
                        st.success("GitHub에 푸시되었습니다!")
                        st.info("Streamlit Cloud가 자동으로 재배포를 시작합니다.")
                        st.code(result.stdout, language="text")
                    else:
                        st.error("푸시 실패")
                        st.code(result.stderr, language="text")
                except Exception as e:
                    st.error(f"오류: {e}")
        
        st.markdown("---")
        st.markdown("#### 한 번에 실행")
        
        if st.button("🔄 Add → Commit → Push", use_container_width=True, type="primary"):
            try:
                with st.spinner("Git 업데이트 중..."):
                    # Add
                    subprocess.run(['git', 'add', '-A'], check=True, cwd=Path.cwd())
                    st.success("✅ 파일 추가 완료")
                    
                    # Commit
                    result = subprocess.run(
                        ['git', 'commit', '-m', commit_message],
                        capture_output=True,
                        text=True,
                        cwd=Path.cwd()
                    )
                    
                    if result.returncode == 0:
                        st.success("✅ 커밋 완료")
                        
                        # Push
                        result = subprocess.run(
                            ['git', 'push'],
                            capture_output=True,
                            text=True,
                            cwd=Path.cwd()
                        )
                        
                        if result.returncode == 0:
                            st.success("✅ GitHub 푸시 완료!")
                            st.balloons()
                            st.info("Streamlit Cloud가 자동으로 재배포를 시작합니다. 약 2-3분 소요됩니다.")
                        else:
                            st.error("푸시 실패")
                            st.code(result.stderr, language="text")
                    else:
                        st.warning("커밋할 변경사항이 없습니다.")
            except Exception as e:
                st.error(f"오류: {e}")

# 메인 라우팅
def main():
    page = st.session_state.page
    
    if page == 'home':
        show_main_page()
    elif page == 'detail':
        show_detail_page()
    elif page == 'inquiry':
        show_inquiry_page()
    elif page == 'login':
        show_login_page()
    elif page == 'admin':
        show_admin_page()
    else:
        show_main_page()

if __name__ == "__main__":
    main()
