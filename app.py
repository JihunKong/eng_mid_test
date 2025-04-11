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
            # 한글 시작 문장 식별
            korean_start_markers = {
                "part1.md": "수영해도 될까요?",
                "part2.md": "반대의 성격, 훌륭한 동반자 관계",
                "part3.md": "불을 끄고 호랑이를 살리세요"
            }
            
            # 줄바꿈으로 텍스트 분리
            lines = content.split('\n')
            english_lines = []
            korean_lines = []
            
            # 한글 시작 인덱스 찾기
            korean_start_idx = 0
            for i, line in enumerate(lines):
                if korean_start_markers.get(selected_file) in line:
                    korean_start_idx = i
                    break
            
            # 줄바꿈을 기준으로 영어와 한글 분리
            for i in range(korean_start_idx):
                if lines[i].strip():
                    english_lines.append(lines[i])
            
            for i in range(korean_start_idx, len(lines)):
                if lines[i].strip():
                    korean_lines.append(lines[i])
            
            # 최소 라인 수 계산
            min_lines = min(len(english_lines), len(korean_lines))
            
            # 영어/한국어 번갈아 표시
            st.markdown("## 본문")
            for i in range(min_lines):
                if english_lines[i].strip():
                    st.markdown(f"**{english_lines[i]}**")
                if i < len(korean_lines) and korean_lines[i].strip():
                    st.markdown(f"*{korean_lines[i]}*")
                st.markdown("---")
            
            # 남은 라인 표시 (길이가 다를 경우)
            if len(english_lines) > min_lines:
                for i in range(min_lines, len(english_lines)):
                    if english_lines[i].strip():
                        st.markdown(f"**{english_lines[i]}**")
                        st.markdown("---")
            
            if len(korean_lines) > min_lines:
                for i in range(min_lines, len(korean_lines)):
                    if korean_lines[i].strip():
                        st.markdown(f"*{korean_lines[i]}*")
                        st.markdown("---")

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
            # 영어/한국어 분리
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
            
            # 난이도 선택
            difficulty = st.selectbox("난이도 선택", ["쉬움", "보통", "어려움"])
            difficulty_eng = {"쉬움": "easy", "보통": "medium", "어려움": "hard"}
            
            # 문제 생성 버튼
            if st.button("문제 생성"):
                with st.spinner("문제를 생성 중입니다..."):
                    questions = ai_helper.generate_questions(english_text, difficulty_eng[difficulty])
                    if questions:
                        # 문제와 해설 분리
                        if "문제:" in questions and "해설:" in questions:
                            parts = questions.split("해설:")
                            if len(parts) == 2:
                                questions_part = parts[0].strip()
                                explanations_part = "해설:" + parts[1].strip()
                                # 문제와 해설 사이에 여백 추가
                                questions = f"{questions_part}\n\n{explanations_part}"
                        st.session_state.questions = questions
                    else:
                        st.error("문제를 생성할 수 없습니다.")
            
            # 문제 표시
            if 'questions' in st.session_state:
                # 문제와 해설 사이에 줄바꿈이 있는지 확인하고 표시
                if "문제:" in st.session_state.questions and "해설:" in st.session_state.questions:
                    parts = st.session_state.questions.split("해설:")
                    if len(parts) == 2:
                        st.markdown("## 문제")
                        st.markdown(parts[0].replace("문제:", "").strip())
                        st.markdown("---")
                        st.markdown("## 해설")
                        st.markdown(parts[1].strip())
                    else:
                        st.markdown(st.session_state.questions)
                else:
                    st.markdown(st.session_state.questions)

if __name__ == "__main__":
    main() 