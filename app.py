import streamlit as st
import time
import os
from typing import Tuple, List, Dict, Optional
from datetime import datetime
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

def call_ai_helper(method, *args, max_retries=3):
    """AI 헬퍼 함수 호출"""
    for attempt in range(max_retries):
        try:
            result = getattr(ai_helper, method)(*args)
            return result
        except Exception as e:
            if attempt < max_retries - 1:
                st.warning(f"API 호출 실패, 재시도 중... ({attempt + 1}/{max_retries})")
                time.sleep(2)
            else:
                st.error(f"API 호출 실패: {str(e)}")
                return None

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

def split_text_and_translation(content):
    """텍스트와 번역 분리"""
    lines = content.split('\n')
    english_lines = []
    korean_lines = []
    
    # 영어와 한국어 구분 (간단한 방법)
    for i, line in enumerate(lines):
        if i % 2 == 0:  # 짝수 인덱스는 영어로 가정
            english_lines.append(line)
        else:  # 홀수 인덱스는 한국어로 가정
            korean_lines.append(line)
    
    english_text = '\n'.join(line for line in english_lines if line.strip())
    korean_text = '\n'.join(line for line in korean_lines if line.strip())
    
    return english_text, korean_text

def display_text_with_translation(text, translation):
    """텍스트와 번역 표시"""
    english_lines = text.split('\n')
    korean_lines = translation.split('\n')
    
    min_lines = min(len(english_lines), len(korean_lines))
    
    for i in range(min_lines):
        if english_lines[i].strip() and korean_lines[i].strip():
            st.markdown(f"**{english_lines[i]}**")
            st.markdown(f"*{korean_lines[i]}*")
            st.markdown("---")

def main():
    """메인 함수"""
    st.sidebar.title("영어 학습 도우미")
    
    # 메뉴 선택
    menu = st.sidebar.radio(
        "메뉴",
        ["홈", "본문 읽기", "문제 풀기", "빈칸 채우기"]
    )
    
    if menu == "홈":
        home_page()
    elif menu == "본문 읽기":
        reading_page()
    elif menu == "문제 풀기":
        quiz_page()
    elif menu == "빈칸 채우기":
        fill_in_blank_page()

def home_page():
    """홈 페이지"""
    st.title("영어 학습 도우미")
    st.markdown("""
    안녕하세요! 영어 학습 도우미에 오신 것을 환영합니다.
    
    이 앱은 다음과 같은 기능을 제공합니다:
    
    1. **본문 읽기**: 영어 텍스트와 한국어 번역을 함께 읽을 수 있습니다.
    2. **문제 풀기**: 객관식 문제를 풀어볼 수 있습니다.
    3. **빈칸 채우기**: 빈칸 채우기 문제를 풀어볼 수 있습니다.
    
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
            english_text, korean_text = split_text_and_translation(content)
            display_text_with_translation(english_text, korean_text)

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
            english_text, _ = split_text_and_translation(content)
            
            # 문제 생성 버튼
            if st.button("문제 생성"):
                with st.spinner("문제를 생성 중입니다..."):
                    questions = call_ai_helper('generate_questions', english_text)
                    if questions:
                        st.session_state.questions = questions
                    else:
                        st.error("문제를 생성할 수 없습니다.")
            
            # 문제 표시
            if 'questions' in st.session_state:
                st.markdown("## 문제")
                st.markdown(st.session_state.questions)

def fill_in_blank_page():
    """빈칸 채우기 문제 페이지"""
    st.title("빈칸 채우기 문제")
    
    # 파일 선택
    selected_file = st.selectbox(
        "파일 선택",
        ["part1.md", "part2.md", "part3.md"]
    )
    
    if selected_file:
        content = read_markdown_file(selected_file)
        if content:
            english_text, _ = split_text_and_translation(content)
            
            # 문제 생성 버튼
            if st.button("문제 생성"):
                with st.spinner("문제를 생성 중입니다..."):
                    result = call_ai_helper('generate_fill_in_blank', english_text)
                    if result:
                        # 문제와 해설 분리
                        parts = result.split('해설:')
                        if len(parts) == 2:
                            questions = parts[0].strip()
                            explanations = '해설:' + parts[1].strip()
                            
                            st.session_state.questions = questions
                            st.session_state.explanations = explanations
                        else:
                            st.error("문제와 해설을 분리할 수 없습니다.")
                    else:
                        st.error("문제를 생성할 수 없습니다.")
            
            # 문제와 해설 표시
            if 'questions' in st.session_state:
                st.markdown("## 문제")
                st.markdown(st.session_state.questions)
                
                if st.button("답안 확인"):
                    st.markdown("## 해설")
                    st.markdown(st.session_state.explanations)

if __name__ == "__main__":
    main() 