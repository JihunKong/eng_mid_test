import streamlit as st
from modules.ai_helper import AIHelper
import os

# 페이지 설정
st.set_page_config(
    page_title="영어 학습 도우미",
    page_icon="📚",
    layout="wide"
)

# API 키 확인
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    st.error("⚠️ API 키가 설정되지 않았습니다. 환경 변수에 ANTHROPIC_API_KEY를 설정해주세요.")
    st.stop()

# AI 도우미 초기화
@st.cache_resource
def get_ai_helper():
    return AIHelper()

ai_helper = get_ai_helper()

# 사이드바
st.sidebar.title("📚 영어 학습 도우미")
page = st.sidebar.radio(
    "학습 모드 선택",
    ["읽기 모드", "연습 모드", "테스트 모드", "학습 분석"]
)

# 메인 콘텐츠
st.title("영어 학습 도우미")
st.markdown("""
    안녕하세요! 영어 학습을 도와드리는 AI 도우미입니다.
    왼쪽 사이드바에서 원하는 학습 모드를 선택해주세요.
""")

if page == "읽기 모드":
    st.header("📖 읽기 모드")
    text = st.text_area("영어 지문을 입력하세요", height=200)
    
    if text:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("영어")
            st.write(text)
        with col2:
            st.subheader("한국어")
            # 여기에 번역 기능 추가 예정
    
elif page == "연습 모드":
    st.header("✍️ 연습 모드")
    exercise_type = st.selectbox(
        "연습 유형 선택",
        ["빈칸 채우기", "문장 재배열", "매칭 게임"]
    )
    
    if exercise_type == "빈칸 채우기":
        st.write("빈칸 채우기 연습을 시작합니다.")
        # 빈칸 채우기 기능 구현 예정
    
elif page == "테스트 모드":
    st.header("📝 테스트 모드")
    text = st.text_area("테스트를 위한 지문을 입력하세요", height=200)
    
    if text:
        difficulty = st.select_slider("난이도", options=["쉬움", "보통", "어려움"])
        num_questions = st.slider("문제 수", min_value=3, max_value=10, value=5)
        
        if st.button("문제 생성"):
            with st.spinner("문제를 생성 중입니다..."):
                questions = ai_helper.generate_questions(text, difficulty, num_questions)
                st.write(questions)
    
elif page == "학습 분석":
    st.header("📊 학습 분석")
    st.write("학습 진행도와 성취도를 분석합니다.")
    # 학습 분석 기능 구현 예정

# 푸터
st.markdown("---")
st.markdown("© 2024 영어 학습 도우미. All rights reserved.") 