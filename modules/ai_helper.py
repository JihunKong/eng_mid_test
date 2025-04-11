import anthropic
from typing import List, Dict

class AIHelper:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API 키가 제공되지 않았습니다.")
        try:
            self.client = anthropic.Anthropic(api_key=api_key)
            self.model = "claude-3-7-sonnet-20250219"
        except Exception as e:
            raise ValueError(f"Anthropic 클라이언트 초기화 실패: {str(e)}")
    
    def generate_questions(self, text: str, difficulty: str = "medium", num_questions: int = 5) -> str:
        """지문 기반 객관식 문제 생성"""
        prompt = f"""
        다음 영어 지문을 바탕으로 {difficulty} 난이도의 객관식 문제 {num_questions}개를 생성해주세요.
        
        문제와 해설은 다음과 같이 완전히 분리해서 작성해주세요:
        
        문제:
        
        문제 1
        문제 내용
        A) 보기 1
        B) 보기 2
        C) 보기 3
        D) 보기 4
        
        문제 2
        문제 내용
        A) 보기 1
        B) 보기 2
        C) 보기 3
        D) 보기 4
        
        [문제 3, 4, 5 동일한 형식으로 작성]
        
        해설:
        
        문제 1
        정답: 정답
        해설: 해설
        
        문제 2
        정답: 정답
        해설: 해설
        
        [문제 3, 4, 5 동일한 형식으로 작성]
        
        각 문제와 문제 사이, 그리고 각 해설과 해설 사이에는 줄바꿈을 추가하여 가독성을 높여주세요.
        또한, 각 문제에서 선택지(A, B, C, D)는 다음과 같이 각각 줄바꿈하여 표시해주세요:
        
        문제 1
        문제 내용
        A) 보기 1
        B) 보기 2
        C) 보기 3
        D) 보기 4
        
        지문:
        {text}
        """
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            system="You are an English teacher creating multiple-choice questions. Always provide ALL QUESTIONS first, then ALL ANSWERS AND EXPLANATIONS separately. Never mix them. Use Korean for question content. Add line breaks between questions and between explanations for better readability. Format each option (A, B, C, D) on a new line.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text
    
    def generate_single_question(self, text: str, difficulty: str = "medium", question_type: str = "comprehension") -> dict:
        """단일 문제 생성 (다양한 유형)"""
        # 문제 유형별 프롬프트 조정
        type_prompts = {
            "comprehension": "지문 이해에 관한 문제를 만들어주세요. 지문의 주제, 요지, 내용 이해 등에 관한 문제를 생성합니다.",
            "vocabulary": "어휘에 관한 문제를 만들어주세요. 밑줄 친 단어의 의미나 유사어, 반의어, 문맥에 맞는 단어 등을 묻는 문제를 생성합니다.",
            "grammar": "문법에 관한 문제를 만들어주세요. 시제, 관사, 전치사, 접속사, 구문 등 영어 문법에 관한 문제를 생성합니다.",
            "blank": "빈칸 추론 문제를 만들어주세요. 지문의 빈칸에 들어갈 적절한 표현을 추론하는 문제를 생성합니다.",
            "ordering": "문장 배열 문제를 만들어주세요. 문장의 순서를 올바르게 배열하는 문제를 생성합니다."
        }
        
        prompt = f"""
        다음 영어 지문을 바탕으로 {difficulty} 난이도의 {type_prompts.get(question_type, "지문 이해")} 문제를 1개만 생성해주세요.
        
        문제는 고등학교 2학년 영어 내신 시험 수준으로 출제해주세요.
        
        다음 형식으로 제공해주세요:
        {{
            "question": "문제 내용",
            "options": [
                "A) 보기 1",
                "B) 보기 2",
                "C) 보기 3",
                "D) 보기 4"
            ],
            "answer": "정답 (A, B, C, D 중 하나)",
            "explanation": "자세한 해설"
        }}
        
        반드시 JSON 형식으로 응답해주세요. 다른 설명이나 텍스트는 포함하지 마세요.
        
        지문:
        {text}
        """
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system="You are an English teacher creating multiple-choice questions for high school students. Create ONE question at a time. Return your response in valid JSON format. Use Korean for question content and explanations.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        try:
            # JSON 응답 찾기 (중괄호로 둘러싸인 부분)
            import re
            import json
            
            content = response.content[0].text
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            else:
                # JSON이 아닌 경우 응답 구조화 시도
                return {
                    "question": content,
                    "options": ["A) 답변이 올바른 형식으로 제공되지 않았습니다"],
                    "answer": "A",
                    "explanation": "응답 형식 오류"
                }
        except Exception as e:
            return {
                "question": "문제 생성 중 오류가 발생했습니다",
                "options": [f"A) 오류: {str(e)}"],
                "answer": "A",
                "explanation": "응답 처리 오류"
            } 