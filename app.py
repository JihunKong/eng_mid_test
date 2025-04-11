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
    
    # 메뉴 선택
    quiz_mode = st.sidebar.radio(
        "문제 유형",
        ["일반 객관식", "단계별 학습"]
    )
    
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
            
            # 한글 시작 문장 식별
            korean_start_markers = {
                "part1.md": "수영해도 될까요?",
                "part2.md": "반대의 성격, 훌륭한 동반자 관계",
                "part3.md": "불을 끄고 호랑이를 살리세요"
            }
            
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
            
            english_text = '\n'.join(line for line in english_lines if line.strip())
            
            # 난이도 선택
            difficulty = st.selectbox("난이도 선택", ["쉬움", "보통", "어려움"])
            difficulty_eng = {"쉬움": "easy", "보통": "medium", "어려움": "hard"}
            
            if quiz_mode == "일반 객관식":
                # 기존 문제 생성 방식
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
                            
                            # 선택지 형식 개선 (A), B), C), D)를 찾아서 줄바꿈 추가)
                            import re
                            options_pattern = r'([A-D]\))'
                            questions = re.sub(options_pattern, r'\n\1', questions)
                            
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
            
            elif quiz_mode == "단계별 학습":
                # 새로운 상호작용 방식의 문제 (하나씩 풀기)
                
                # 세션 상태 초기화
                if 'current_question' not in st.session_state:
                    st.session_state.current_question = None
                if 'question_history' not in st.session_state:
                    st.session_state.question_history = []
                if 'selected_answer' not in st.session_state:
                    st.session_state.selected_answer = None
                if 'show_explanation' not in st.session_state:
                    st.session_state.show_explanation = False
                if 'current_question_type' not in st.session_state:
                    st.session_state.current_question_type = "comprehension"
                if 'error_count' not in st.session_state:
                    st.session_state.error_count = 0
                
                # 오류 횟수가 많으면 사용자에게 알림
                if st.session_state.error_count > 2:
                    st.warning("문제 생성 중 여러 번 오류가 발생했습니다. 다른 유형이나 지문을 선택해보세요.")
                
                # 문제 유형 선택
                question_types = {
                    "comprehension": "지문 이해 문제",
                    "vocabulary": "어휘 문제",
                    "grammar": "문법 문제", 
                    "blank": "빈칸 추론 문제",
                    "ordering": "문장 배열 문제"
                }
                
                # 새 문제를 생성할 시점에만 문제 유형 선택 가능
                if st.session_state.current_question is None:
                    try:
                        selected_type = st.selectbox(
                            "문제 유형 선택",
                            list(question_types.keys()),
                            format_func=lambda x: question_types.get(x, x)
                        )
                        st.session_state.current_question_type = selected_type
                    except Exception as e:
                        st.error(f"문제 유형 선택 중 오류가 발생했습니다: {str(e)}")
                        st.session_state.current_question_type = "comprehension"
                
                # 문제 생성 버튼
                if st.session_state.current_question is None:
                    if st.button("새 문제 생성"):
                        with st.spinner("문제를 생성 중입니다..."):
                            try:
                                # 안전하게 AI 헬퍼 호출
                                if not english_text or len(english_text) < 10:
                                    st.error("지문이 너무 짧습니다. 다른 파일을 선택하세요.")
                                else:
                                    question_data = ai_helper.generate_single_question(
                                        english_text, 
                                        difficulty_eng.get(difficulty, "medium"),
                                        st.session_state.current_question_type
                                    )
                                    
                                    # 유효한 문제인지 확인
                                    if (isinstance(question_data, dict) and 
                                        "question" in question_data and
                                        "options" in question_data and 
                                        isinstance(question_data["options"], list)):
                                        
                                        st.session_state.current_question = question_data
                                        st.session_state.selected_answer = None
                                        st.session_state.show_explanation = False
                                        st.session_state.error_count = 0
                                    else:
                                        st.error("문제 생성에 실패했습니다. 다시 시도하세요.")
                                        st.session_state.error_count += 1
                            except Exception as e:
                                st.error(f"문제 생성 중 오류가 발생했습니다: {str(e)}")
                                st.session_state.error_count += 1
                
                # 문제 표시
                if st.session_state.current_question:
                    try:
                        question_data = st.session_state.current_question
                        
                        # 문제 내용 표시
                        current_type = st.session_state.current_question_type
                        if current_type in question_types:
                            st.markdown(f"## {question_types[current_type]}")
                        else:
                            st.markdown("## 문제")
                            
                        st.markdown(question_data.get('question', '문제 로딩 중...'))
                        
                        # 선택지 표시 (라디오 버튼)
                        options = question_data.get('options', [])
                        option_texts = []
                        
                        # 옵션이 비어있거나 리스트가 아닌 경우 처리
                        if not isinstance(options, list) or len(options) == 0:
                            options = ["A) 선택지를 불러올 수 없습니다.", "B) 옵션 B", "C) 옵션 C", "D) 옵션 D"]
                        
                        # 옵션 텍스트 확인
                        for opt in options:
                            if isinstance(opt, str) and opt.strip():
                                option_texts.append(opt)
                            
                        # 선택지가 비어있는 경우 기본값 추가
                        if len(option_texts) < 2:
                            option_texts = ["A) 선택지가 제공되지 않았습니다.", "B) 옵션 B", "C) 옵션 C", "D) 옵션 D"]
                        
                        if not st.session_state.show_explanation:
                            answer = st.radio(
                                "답을 선택하세요:",
                                option_texts,
                                key=f"answer_{len(st.session_state.question_history)}"
                            )
                            st.session_state.selected_answer = answer
                            
                            if st.button("제출"):
                                st.session_state.show_explanation = True
                                st.experimental_rerun()
                        
                        # 해설 표시
                        if st.session_state.show_explanation:
                            try:
                                correct_answer = question_data.get('answer', 'A')
                                # 문자열로 변환 및 단일 문자만 추출
                                if isinstance(correct_answer, str) and len(correct_answer) > 0:
                                    correct_answer = correct_answer[0].upper()  # 첫 글자만 사용
                                    if correct_answer not in ['A', 'B', 'C', 'D']:
                                        correct_answer = 'A'  # 기본값
                                else:
                                    correct_answer = 'A'  # 기본값
                                    
                                selected_option = st.session_state.selected_answer
                                
                                is_correct = False
                                correct_option = "정답을 확인할 수 없습니다."
                                
                                # 정답 확인
                                for opt in option_texts:
                                    if opt.startswith(correct_answer + ")") or opt.startswith(correct_answer + " "):
                                        correct_option = opt
                                        if selected_option == opt:
                                            is_correct = True
                                        break
                                
                                if is_correct:
                                    st.success("정답입니다! 👏")
                                else:
                                    st.error("오답입니다.")
                                    st.info(f"정답: {correct_option}")
                                
                                st.markdown("### 해설")
                                explanation = question_data.get('explanation', '해설이 제공되지 않았습니다.')
                                if not explanation or not isinstance(explanation, str):
                                    explanation = '해설이 제공되지 않았습니다.'
                                st.markdown(explanation)
                            except Exception as e:
                                st.error(f"해설 표시 중 오류가 발생했습니다: {str(e)}")
                            
                            # 다음 문제 또는 종료 버튼
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                if st.button("다음 문제"):
                                    # 현재 문제를 히스토리에 추가
                                    if isinstance(st.session_state.current_question, dict):
                                        st.session_state.question_history.append(st.session_state.current_question)
                                    # 새 문제 생성 준비
                                    st.session_state.current_question = None
                                    st.session_state.selected_answer = None
                                    st.session_state.show_explanation = False
                                    st.experimental_rerun()
                            
                            with col2:
                                if st.button("학습 종료"):
                                    # 히스토리 요약 표시 후 세션 초기화
                                    if isinstance(st.session_state.current_question, dict):
                                        st.session_state.question_history.append(st.session_state.current_question)
                                    total = len(st.session_state.question_history)
                                    st.session_state.current_question = None
                                    st.session_state.selected_answer = None
                                    st.session_state.show_explanation = False
                                    st.session_state.result_summary = f"총 {total}개의 문제를 풀었습니다."
                                    st.experimental_rerun()
                    except Exception as e:
                        st.error(f"문제 표시 중 오류가 발생했습니다: {str(e)}")
                        st.session_state.current_question = None
                        st.session_state.error_count += 1
                
                # 히스토리 요약 표시
                if 'result_summary' in st.session_state:
                    st.markdown("## 학습 결과")
                    st.markdown(st.session_state.result_summary)
                    if st.button("다시 시작"):
                        # 세션 초기화
                        for key in ['current_question', 'question_history', 'selected_answer', 
                                    'show_explanation', 'result_summary', 'error_count']:
                            if key in st.session_state:
                                del st.session_state[key]
                        st.session_state.current_question_type = "comprehension"
                        st.experimental_rerun()

if __name__ == "__main__":
    main() 