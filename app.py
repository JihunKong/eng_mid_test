import streamlit as st
from modules.ai_helper import AIHelper
import os
import re
import time
import json
from typing import Tuple, List, Dict, Optional
import random
import requests
from datetime import datetime

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

def generate_fill_in_the_blank(text: str) -> Tuple[List[str], List[str]]:
    """빈칸 채우기 문제 생성"""
    result = call_ai_helper('generate_fill_in_blank', text)
    if not result:
        return [], []
        
    try:
        # 문제와 해설 섹션 분리
        parts = result.split('해설:')
        if len(parts) != 2:
            return [], []
            
        questions_part = parts[0].strip()
        answers_part = '해설:' + parts[1].strip()
        
        # 문제 목록 추출
        questions = []
        current_question = ""
        for line in questions_part.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line == '문제:':
                continue
                
            if line[0].isdigit() and line[1] == '.':
                if current_question:
                    questions.append(current_question)
                current_question = line + "\n"
            else:
                current_question += line + "\n"
                
        if current_question:
            questions.append(current_question)
            
        # 해설 목록 추출
        answers = []
        current_answer = ""
        for line in answers_part.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line == '해설:':
                continue
                
            if line[0].isdigit() and line[1] == '.':
                if current_answer:
                    answers.append(current_answer)
                current_answer = line + "\n"
            else:
                current_answer += line + "\n"
                
        if current_answer:
            answers.append(current_answer)
            
        return questions, answers
    except Exception as e:
        st.error(f"문제 생성 중 오류: {str(e)}")
        return [], []

def display_questions(questions: List[str], answers: List[str], user_answers: List[str]):
    """문제와 답안을 표시"""
    # 모든 문제 먼저 표시
    st.markdown("### 문제")
    for i, question in enumerate(questions, 1):
        st.markdown(f"**{question}**")
        st.markdown("---")
    
    # 답안 확인 버튼
    if st.button("답안 확인"):
        # 모든 해설 표시
        st.markdown("### 해설")
        for i, answer in enumerate(answers, 1):
            st.markdown(f"**{answer}**")
            st.markdown("---")

def display_text_with_translation(text: str, translation: str):
    """텍스트와 번역을 줄바꿈 기준으로 번갈아가며 표시"""
    # 줄바꿈을 기준으로 문장 분리
    english_lines = [line.strip() for line in text.split('\n') if line.strip()]
    korean_lines = [line.strip() for line in translation.split('\n') if line.strip()]
    
    # 최대 줄 수 맞추기
    min_lines = min(len(english_lines), len(korean_lines))
    english_lines = english_lines[:min_lines]
    korean_lines = korean_lines[:min_lines]
    
    # 줄 단위로 번갈아가며 표시
    for eng, kor in zip(english_lines, korean_lines):
        st.markdown(f"**{eng}**")
        st.markdown(f"*{kor}*")
        st.markdown("---")

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

# API 호출 함수에 재시도 로직 추가
def call_ai_helper(method, *args, max_retries=3, retry_delay=5):
    for attempt in range(max_retries):
        try:
            result = getattr(ai_helper, method)(*args)
            return result
        except Exception as e:
            if attempt < max_retries - 1:
                st.warning(f"API 호출 실패 (시도 {attempt + 1}/{max_retries}). {retry_delay}초 후 재시도합니다...")
                time.sleep(retry_delay)
            else:
                st.error(f"API 호출 실패: {str(e)}")
                return None

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
            
        # 각 파일의 기준점으로 영어/한국어 구분
        if line.startswith('수영해도 될까요?'):  # part1
            is_english = False
        elif line.startswith('반대의 성격, 훌륭한 동반자 관계'):  # part2
            is_english = False
        elif line.startswith('불을 끄고 호랑이를 살리세요'):  # part3
            is_english = False
            
        # 영어와 한국어 구분을 위한 추가 로직
        if is_english:
            # 영어 문장인 경우
            if any(char.isalpha() for char in line) and not any(ord('가') <= ord(char) <= ord('힣') for char in line):
                english_lines.append(line)
            else:
                korean_lines.append(line)
        else:
            # 한국어 문장인 경우
            if any(ord('가') <= ord(char) <= ord('힣') for char in line):
                korean_lines.append(line)
            else:
                english_lines.append(line)
    
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

def main():
    # 사이드바
    st.sidebar.title("📚 영어 학습 도우미")
    menu = st.sidebar.radio(
        "메뉴",
        ["홈", "본문 읽기", "문제 풀기", "빈칸 채우기", "단어 학습", "문장 재배열", "매칭 게임"]
    )
    
    # 선택한 메뉴에 따라 페이지 표시
    if menu == "홈":
        home_page()
    elif menu == "본문 읽기":
        reading_page()
    elif menu == "문제 풀기":
        quiz_page()
    elif menu == "빈칸 채우기":
        fill_in_blank_page()
    elif menu == "단어 학습":
        vocabulary_page()
    elif menu == "문장 재배열":
        sentence_rearrangement_page()
    elif menu == "매칭 게임":
        matching_game_page()

def home_page():
    """홈 페이지"""
    st.title("영어 학습 도우미")
    st.markdown("""
    안녕하세요! 영어 학습 도우미에 오신 것을 환영합니다.
    
    이 애플리케이션은 영어 학습을 도와주는 다양한 기능을 제공합니다:
    
    1. **문제 풀기**: 영어 지문을 바탕으로 다양한 문제를 풀어볼 수 있습니다.
    2. **빈칸 채우기**: 영어 지문에서 빈칸을 채우는 연습을 할 수 있습니다.
    3. **단어 학습**: 중요한 단어들을 학습할 수 있습니다.
    4. **문장 재배열**: 문장의 순서를 맞추는 연습을 할 수 있습니다.
    5. **매칭 게임**: 단어와 의미를 매칭하는 게임을 할 수 있습니다.
    
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
        
        if not content:
            st.error("파일을 읽을 수 없습니다.")
            return
        
        # 텍스트 분리
        english_text, korean_text = split_text_and_translation(content)
        
        # 텍스트 표시
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
        
        if not content:
            st.error("파일을 읽을 수 없습니다.")
            return
        
        # 영어 텍스트만 추출
        english_text, _ = split_text_and_translation(content)
        
        # 난이도 선택
        difficulty = st.selectbox("문제 난이도 선택", ["쉬움", "보통", "어려움"])
        
        # 문제 생성 버튼
        if st.button("문제 생성"):
            with st.spinner("문제를 생성 중입니다..."):
                difficulty_eng = {"쉬움": "easy", "보통": "medium", "어려움": "hard"}
                questions = call_ai_helper('generate_questions', english_text, difficulty_eng[difficulty])
                
                if questions:
                    st.session_state.questions = questions
                    st.success("문제가 생성되었습니다!")
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
        
        if not content:
            st.error("파일을 읽을 수 없습니다.")
            return
        
        # 영어 텍스트만 추출
        english_text, _ = split_text_and_translation(content)
        
        # 문제 생성
        if st.button("문제 생성"):
            with st.spinner("문제를 생성 중입니다..."):
                questions_text = call_ai_helper('generate_fill_in_blank', english_text)
                if not questions_text:
                    st.error("문제를 생성할 수 없습니다.")
                    return
                    
                # 문제와 해설 분리
                split_text = questions_text.split("해설:")
                if len(split_text) != 2:
                    st.error("문제와 해설을 분리할 수 없습니다.")
                    return
                    
                st.session_state.questions_section = split_text[0].strip()
                st.session_state.explanations_section = "해설:" + split_text[1].strip()
                st.success("문제가 생성되었습니다!")
        
        # 문제 표시
        if 'questions_section' in st.session_state:
            st.markdown("## 문제")
            st.markdown(st.session_state.questions_section)
            
            # 해설 표시 (버튼 클릭 시)
            if st.button("답안 확인"):
                st.markdown("## 해설")
                st.markdown(st.session_state.explanations_section)

def vocabulary_page():
    """단어 학습 페이지"""
    st.title("단어 학습")
    
    # 파일 선택
    selected_file = st.selectbox(
        "파일 선택",
        ["part1.md", "part2.md", "part3.md"]
    )
    
    if selected_file:
        content = read_markdown_file(selected_file)
        
        if not content:
            st.error("파일을 읽을 수 없습니다.")
            return
        
        # 영어 텍스트만 추출
        english_text, _ = split_text_and_translation(content)
        
        # 단어 입력
        word = st.text_input("학습할 단어를 입력하세요")
        
        if word and st.button("단어 설명 보기"):
            with st.spinner("단어 정보를 가져오는 중입니다..."):
                explanation = call_ai_helper('explain_vocabulary', word, english_text)
                
                if explanation:
                    st.markdown("## 단어 설명")
                    st.markdown(explanation)
                else:
                    st.error("단어 정보를 가져올 수 없습니다.")

def sentence_rearrangement_page():
    """문장 재배열 페이지"""
    st.title("문장 재배열")
    
    # 파일 선택
    selected_file = st.selectbox(
        "파일 선택",
        ["part1.md", "part2.md", "part3.md"]
    )
    
    if selected_file:
        content = read_markdown_file(selected_file)
        
        if not content:
            st.error("파일을 읽을 수 없습니다.")
            return
        
        # 영어 텍스트만 추출
        english_text, _ = split_text_and_translation(content)
        
        # 문제 생성
        if st.button("문제 생성"):
            with st.spinner("문제를 생성 중입니다..."):
                questions = call_ai_helper('generate_sentence_rearrangement', english_text)
                
                if questions:
                    st.session_state.rearrangement_questions = questions
                    st.success("문제가 생성되었습니다!")
                else:
                    st.error("문제를 생성할 수 없습니다.")
        
        # 문제 표시
        if 'rearrangement_questions' in st.session_state:
            st.markdown("## 문장 재배열 문제")
            st.markdown(st.session_state.rearrangement_questions)

def matching_game_page():
    """매칭 게임 페이지"""
    st.title("매칭 게임")
    
    # 파일 선택
    selected_file = st.selectbox(
        "파일 선택",
        ["part1.md", "part2.md", "part3.md"]
    )
    
    if selected_file:
        content = read_markdown_file(selected_file)
        
        if not content:
            st.error("파일을 읽을 수 없습니다.")
            return
        
        # 영어 텍스트만 추출
        english_text, _ = split_text_and_translation(content)
        
        # 게임 생성
        if st.button("게임 생성"):
            with st.spinner("게임을 생성 중입니다..."):
                game = call_ai_helper('generate_matching_game', english_text)
                
                if game:
                    st.session_state.matching_game = game
                    st.success("게임이 생성되었습니다!")
                else:
                    st.error("게임을 생성할 수 없습니다.")
        
        # 게임 표시
        if 'matching_game' in st.session_state:
            st.markdown("## 매칭 게임")
            st.markdown(st.session_state.matching_game)

# 푸터
st.markdown("---")
st.markdown("© 2025 완도고 2학년 영어 학습 도우미. All rights reserved.")

if __name__ == "__main__":
    main() 