{
  `content`: `# 🌟 영어 학습 도우미 (English Learning Assistant)

영어 학습 도우미는 학생들의 영어 학습을 돕기 위한 종합 학습 플랫폼입니다. Claude 3.7 Sonnet AI를 활용하여 개인화된 학습 경험을 제공합니다.

## 📚 주요 기능

### 1. 파트별 학습
- 영어 지문을 3개 파트로 나누어 단계별 학습 
  part1.md, part2.md, part3.md를 활용
- 각 파트별 난이도 조절 및 학습 진행도 추적

### 2. 다양한 학습 모드
- **읽기 모드**: 영어/한국어 병렬 보기, 영어만 보기, 한국어만 보기
- **연습 모드**: 빈칸 채우기, 문장 재배열, 매칭 게임
- **테스트 모드**: 객관식 및 주관식 문제로 이해도 평가

### 3. AI 기반 학습 지원
- **맞춤형 문제 생성**: Claude AI가 학생 수준에 맞는 문제 실시간 생성
- **개인화된 피드백**: 학생의 답변에 대한 상세한 피드백 제공
- **어휘 설명**: 어려운 단어나 표현에 대한 맥락 기반 설명
- **추가 예문 생성**: 학습 중인 표현을 다양한 상황에서 활용하는 예문 제공

### 4. 학습 데이터 분석
- 학습 진행도 및 성취도 시각화
- 취약점 분석 및 맞춤형 학습 계획 제안

## 🔧 설치 및 설정

### 필수 요구사항
- Python 3.8 이상
- Streamlit 1.25.0 이상
- Anthropic API 키

### 설치 방법
```bash
# 저장소 클론
git clone https://github.com/yourusername/english-learning-assistant.git
cd english-learning-assistant

# 필요한 패키지 설치
pip install -r requirements.txt

# 환경 변수 설정
# Windows
set ANTHROPIC_API_KEY=your_api_key_here

# Mac/Linux
export ANTHROPIC_API_KEY=your_api_key_here
```

### 앱 실행하기
```bash
streamlit run app.py
```

## 🔐 환경 변수 설정

앱을 실행하기 전에 다음 환경 변수를 설정해야 합니다:

- `ANTHROPIC_API_KEY`: Anthropic의 API 키 (Claude 3.7 Sonnet 사용을 위해 필요)
- `STREAMLIT_SERVER_PORT`: (선택) 서버 포트 지정 (기본값: 8501)
- `STREAMLIT_SERVER_HEADLESS`: (선택) 헤드리스 모드 실행 시 'true'로 설정

### .streamlit/secrets.toml 파일 설정
```toml
# .streamlit/secrets.toml
ANTHROPIC_API_KEY = \"your_api_key_here\"
```

## 📁 프로젝트 구조
```
english-learning-assistant/
├── app.py                  # 메인 애플리케이션 파일
├── requirements.txt        # 필요한 패키지 목록
├── README.md               # 프로젝트 설명
├── .streamlit/
│   └── config.toml         # Streamlit 설정
├── data/
│   ├── lessons/            # 학습 텍스트 데이터
│   └── audio/              # 오디오 파일 (TTS)
├── modules/
│   ├── ai_helper.py        # Claude AI 통합 모듈
│   ├── text_processor.py   # 텍스트 처리 모듈
│   ├── exercise_gen.py     # 연습 문제 생성 모듈
│   └── analytics.py        # 학습 데이터 분석 모듈
└── pages/
    ├── 01_reading.py       # 읽기 학습 페이지
    ├── 02_practice.py      # 연습 페이지
    ├── 03_test.py          # 테스트 페이지
    └── 04_analytics.py     # 학습 분석 페이지
```

## 🤖 Claude 3.7 Sonnet AI 활용 방법

### AI 기능 설정
`modules/ai_helper.py` 파일에서 Claude API를 활용한 다양한 기능이 구현되어 있습니다:

```python
from anthropic import Anthropic
import os

class AIHelper:
    def __init__(self):
        self.client = Anthropic(api_key=os.environ.get(\"ANTHROPIC_API_KEY\"))
        self.model = \"claude-3-7-sonnet-20250219\"
    
    def generate_questions(self, text, difficulty=\"medium\", num_questions=5):
        \"\"\"지문 기반 문제 생성\"\"\"
        prompt = f\"\"\"
        다음 영어 지문을 읽고 {difficulty} 난이도의 객관식 문제 {num_questions}개를 생성해주세요:
        
        {text}
        
        각 문제는 다음 형식으로 작성해주세요:
        - 문제 번호와 질문
        - 4개의 선택지 (a, b, c, d)
        - 정답 및 해설
        \"\"\"
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[
                {\"role\": \"user\", \"content\": prompt}
            ]
        )
        return response.content[0].text
    
    def explain_vocabulary(self, word, context):
        \"\"\"단어 설명 및 예문 제공\"\"\"
        # 구현 코드...
    
    def provide_feedback(self, student_answer, correct_answer):
        \"\"\"학생 답변에 대한 피드백 제공\"\"\"
        # 구현 코드...
    
    def generate_similar_examples(self, expression):
        \"\"\"유사 표현 및 예문 생성\"\"\"
        # 구현 코드...
```

### AI 기능 활용 예시
```python
# app.py 또는 다른 페이지에서의 활용 예시
import streamlit as st
from modules.ai_helper import AIHelper

# AI 도우미 초기화
ai_helper = AIHelper()

# 사용자가 단어 설명을 요청할 때
if st.button(\"단어 설명 보기\"):
    word = st.session_state.selected_word
    context = st.session_state.word_context
    explanation = ai_helper.explain_vocabulary(word, context)
    st.write(explanation)

# 맞춤형 문제 생성
if st.button(\"문제 생성\"):
    text = st.session_state.current_text
    difficulty = st.select_slider(\"난이도\", options=[\"쉬움\", \"보통\", \"어려움\"])
    num_questions = st.slider(\"문제 수\", min_value=3, max_value=10, value=5)
    
    with st.spinner(\"문제를 생성 중입니다...\"):
        questions = ai_helper.generate_questions(text, difficulty, num_questions)
    
    st.write(questions)
```

## 📊 학습 데이터 관리

학생들의 학습 데이터는 로컬 SQLite 데이터베이스 또는 클라우드 데이터베이스에 저장할 수 있습니다. 주요 데이터 포인트:

- 학습 진행도
- 정답률 및 오답 패턴
- 학습 시간 및 빈도
- 어휘 및 표현 습득 수준

## 🔄 향후 개발 계획

- 다중 사용자 지원 및 교사용 대시보드
- 모바일 앱 버전 개발
- 추가 학습 자료 및 테마 확장
- AI 음성 인식을 통한 발음 평가 기능
- 학생 간 협업 학습 기능

## 📝 라이센스

이 프로젝트는 MIT 라이센스 하에 제공됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.

  `file_path`: `README.md`
