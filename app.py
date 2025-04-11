# 이 파일은 삭제되었습니다. 

import streamlit as st
import os
from typing import List, Dict, Tuple
from modules.ai_helper import AIHelper

# 페이지 설정
st.set_page_config(
    page_title="영어 학습 도우미",
    page_icon="📚",
    layout="wide"
)

# API 키 확인
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    st.error("API 키가 설정되지 않았습니다. 환경 변수에 ANTHROPIC_API_KEY를 설정해주세요.")
    st.stop()

# AI 도우미 초기화
@st.cache_resource
def get_ai_helper():
    try:
        return AIHelper(api_key=api_key)
    except Exception as e:
        st.error(f"AI 도우미 초기화 중 오류 발생: {str(e)}")
        st.stop()

ai_helper = get_ai_helper()

def read_markdown_file(file_path):
    """마크다운 파일 읽기"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            if not content.strip():
                st.error(f"파일이 비어있습니다: {file_path}")
                return None
            return content
    except Exception as e:
        st.error(f"파일 읽기 오류: {str(e)}")
        return None

def main():
    """메인 함수"""
    st.sidebar.title("영어 학습 도우미")
    
    # 메뉴 선택
    menu = st.sidebar.radio(
        "메뉴",
        ["홈", "본문 읽기", "문제 풀기"]
    )
    
    if menu == "홈":
        home_page()
    elif menu == "본문 읽기":
        reading_page()
    elif menu == "문제 풀기":
        quiz_page()

def home_page():
    """홈 페이지"""
    st.title("영어 학습 도우미")
    st.markdown("""
    안녕하세요! 영어 학습 도우미에 오신 것을 환영합니다.
    
    이 앱은 다음과 같은 기능을 제공합니다:
    
    1. **본문 읽기**: 영어 텍스트와 한국어 번역을 함께 읽을 수 있습니다.
    2. **문제 풀기**: 객관식 문제를 풀어볼 수 있습니다.
    
    왼쪽 사이드바에서 원하는 기능을 선택하세요!
    """)

def reading_page():
    """본문 읽기 페이지"""
    st.title("본문 읽기")
    
    # 파일 선택
    selected_file = st.selectbox(
        "파일 선택",
        ["part1.md", "part2.md", "part3.md"]
    )
    
    if selected_file:
        content = read_markdown_file(selected_file)
        if content:
            st.markdown(content)

def quiz_page():
    """문제 풀기 페이지"""
    st.title("문제 풀기")
    
    # 파일 선택
    selected_file = st.selectbox(
        "파일 선택",
        ["part1.md", "part2.md", "part3.md"]
    )
    
    if selected_file:
        content = read_markdown_file(selected_file)
        if content:
            # 문제 생성 버튼
            if st.button("문제 생성"):
                with st.spinner("문제를 생성 중입니다..."):
                    questions = ai_helper.generate_questions(content)
                    if questions:
                        st.session_state.questions = questions
                    else:
                        st.error("문제를 생성할 수 없습니다.")
            
            # 문제 표시
            if 'questions' in st.session_state:
                st.markdown("## 문제")
                st.markdown(st.session_state.questions)

if __name__ == "__main__":
    main() 