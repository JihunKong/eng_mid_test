import streamlit as st
from modules.ai_helper import AIHelper
import os
import re
import time

# WebSocket 설정
st.set_page_config(
    page_title="영어 학습 도우미",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/streamlit/streamlit/issues',
        'Report a bug': 'https://github.com/streamlit/streamlit/issues',
        'About': '영어 학습 도우미 v1.0'
    }
)

# WebSocket 연결 상태 관리
if 'websocket_connected' not in st.session_state:
    st.session_state['websocket_connected'] = False
    st.session_state['last_connection_attempt'] = time.time()

# WebSocket 연결 재시도 로직
def check_websocket_connection():
    if not st.session_state['websocket_connected']:
        current_time = time.time()
        if current_time - st.session_state['last_connection_attempt'] > 5:  # 5초마다 재시도
            st.session_state['last_connection_attempt'] = current_time
            try:
                # 연결 시도
                st.session_state['websocket_connected'] = True
            except Exception as e:
                st.warning("연결이 불안정합니다. 페이지를 새로고침해주세요.")
                st.session_state['websocket_connected'] = False

# API 키 확인
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    st.error("⚠️ API 키가 설정되지 않았습니다. 환경 변수에 ANTHROPIC_API_KEY를 설정해주세요.")
    st.stop()

# AI 도우미 초기화
@st.cache_resource
def get_ai_helper():
    try:
        return AIHelper(api_key=api_key)
    except Exception as e:
        st.error(f"⚠️ AI 도우미 초기화 중 오류가 발생했습니다: {str(e)}")
        st.stop()

ai_helper = get_ai_helper()

# 지문과 해석 분리 함수
def split_text_and_translation(text):
    """텍스트를 영어 지문과 한국어 해석으로 분리"""
    lines = text.split('\n')
    english_lines = []
    korean_lines = []
    is_english = True
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 영어와 한국어를 구분하는 로직
        if line.startswith('Lesson') or line.startswith('Can I Swim?') or line.startswith('Diego') or line.startswith('I was') or line.startswith('The events'):
            is_english = True
        elif line.startswith('수영해도 될까요?') or line.startswith('Tom Michell은') or line.startswith('Diego의') or line.startswith('나는') or line.startswith('그날'):
            is_english = False
            
        if is_english:
            english_lines.append(line)
        else:
            korean_lines.append(line)
    
    # 빈 줄 제거
    english_text = '\n'.join(line for line in english_lines if line.strip())
    korean_text = '\n'.join(line for line in korean_lines if line.strip())
    
    return english_text, korean_text

# 마크다운 파일 읽기 함수
def read_markdown_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # 파일 내용이 비어있는지 확인
            if not content.strip():
                st.error(f"⚠️ {file_path} 파일이 비어있습니다.")
                return None
            return content
    except FileNotFoundError:
        st.error(f"⚠️ {file_path} 파일을 찾을 수 없습니다.")
        return None
    except Exception as e:
        st.error(f"⚠️ 파일을 읽는 중 오류가 발생했습니다: {str(e)}")
        return None

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
    
    이 앱은 다음과 같은 기능을 제공합니다:
    1. 📖 읽기 모드: 마크다운 파일에서 영어 지문을 읽고 한국어 해석을 확인할 수 있습니다.
    2. ✍️ 연습 모드: 다양한 유형의 연습 문제를 풀어볼 수 있습니다.
    3. 📝 테스트 모드: 선택한 지문에 대한 테스트를 생성하고 풀어볼 수 있습니다.
    4. 📊 학습 분석: 학습 진행 상황을 분석하고 피드백을 받을 수 있습니다.
    
    왼쪽 사이드바에서 원하는 학습 모드를 선택해주세요.
""")

if page == "읽기 모드":
    st.header("📖 읽기 모드")
    st.markdown("""
        마크다운 파일에서 영어 지문을 읽고 한국어 해석을 확인할 수 있습니다.
        아래에서 읽고 싶은 지문을 선택해주세요.
    """)
    
    # 마크다운 파일 선택
    selected_file = st.selectbox(
        "지문 선택",
        ["part1.md", "part2.md", "part3.md"]
    )
    
    if selected_file:
        content = read_markdown_file(selected_file)
        english_text, korean_text = split_text_and_translation(content)
        
        if english_text and korean_text:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("영어 지문")
                st.write(english_text)
            with col2:
                st.subheader("한국어 해석")
                st.write(korean_text)
        else:
            st.warning("선택한 파일에서 지문을 불러올 수 없습니다. 파일이 올바른 형식인지 확인해주세요.")
    
elif page == "연습 모드":
    st.header("✍️ 연습 모드")
    st.markdown("""
        다양한 유형의 연습 문제를 풀어볼 수 있습니다.
        아래에서 연습 유형을 선택해주세요.
    """)
    
    exercise_type = st.selectbox(
        "연습 유형 선택",
        ["빈칸 채우기", "문장 재배열", "매칭 게임"]
    )
    
    # 마크다운 파일 선택
    selected_file = st.selectbox(
        "연습을 위한 지문 선택",
        ["part1.md", "part2.md", "part3.md"]
    )
    
    if selected_file:
        content = read_markdown_file(selected_file)
        english_text, _ = split_text_and_translation(content)
        
        if english_text:
            if exercise_type == "빈칸 채우기":
                st.subheader("빈칸 채우기")
                with st.spinner("문제를 생성 중입니다..."):
                    try:
                        questions = ai_helper.generate_fill_in_blank(english_text)
                        st.write(questions)
                    except Exception as e:
                        st.error(f"⚠️ 문제 생성 중 오류가 발생했습니다: {str(e)}")
            
            elif exercise_type == "문장 재배열":
                st.subheader("문장 재배열")
                with st.spinner("문제를 생성 중입니다..."):
                    try:
                        questions = ai_helper.generate_sentence_rearrangement(english_text)
                        st.write(questions)
                    except Exception as e:
                        st.error(f"⚠️ 문제 생성 중 오류가 발생했습니다: {str(e)}")
            
            elif exercise_type == "매칭 게임":
                st.subheader("매칭 게임")
                with st.spinner("문제를 생성 중입니다..."):
                    try:
                        questions = ai_helper.generate_matching_game(english_text)
                        st.write(questions)
                    except Exception as e:
                        st.error(f"⚠️ 문제 생성 중 오류가 발생했습니다: {str(e)}")
        else:
            st.warning("선택한 파일에서 지문을 불러올 수 없습니다. 파일이 올바른 형식인지 확인해주세요.")
    
elif page == "테스트 모드":
    st.header("📝 테스트 모드")
    
    # 마크다운 파일 선택
    selected_file = st.selectbox(
        "테스트를 위한 지문 선택",
        ["part1.md", "part2.md", "part3.md"]
    )
    
    if selected_file:
        content = read_markdown_file(selected_file)
        english_text, _ = split_text_and_translation(content)
        
        if english_text:
            st.text_area("테스트 지문", english_text, height=200, disabled=True)
            
            difficulty = st.select_slider("난이도", options=["쉬움", "보통", "어려움"])
            num_questions = st.slider("문제 수", min_value=3, max_value=10, value=5)
            
            if st.button("문제 생성"):
                with st.spinner("문제를 생성 중입니다..."):
                    try:
                        questions = ai_helper.generate_questions(english_text, difficulty, num_questions)
                        st.write(questions)
                    except Exception as e:
                        st.error(f"⚠️ 문제 생성 중 오류가 발생했습니다: {str(e)}")
    
elif page == "학습 분석":
    st.header("📊 학습 분석")
    st.write("학습 진행도와 성취도를 분석합니다.")
    # 학습 분석 기능 구현 예정

# 푸터
st.markdown("---")
st.markdown("© 2024 영어 학습 도우미. All rights reserved.") 