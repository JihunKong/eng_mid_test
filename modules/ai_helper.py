from anthropic import Anthropic
from typing import List, Dict, Any

class AIHelper:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API 키가 제공되지 않았습니다.")
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-7-sonnet-20250219"
    
    def generate_questions(self, text: str, difficulty: str = "medium", num_questions: int = 5) -> str:
        """지문 기반 문제 생성"""
        prompt = f"""
        다음 영어 지문을 읽고 {difficulty} 난이도의 객관식 문제 {num_questions}개를 생성해주세요:
        
        {text}
        
        각 문제는 다음 형식으로 작성해주세요:
        - 문제 번호와 질문
        - 4개의 선택지 (a, b, c, d)
        - 정답 및 해설
        """
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    
    def explain_vocabulary(self, word: str, context: str) -> str:
        """단어 설명 및 예문 제공"""
        prompt = f"""
        다음 단어를 설명하고 예문을 제공해주세요:
        단어: {word}
        문맥: {context}
        
        다음 형식으로 작성해주세요:
        1. 단어의 의미
        2. 문맥에서의 의미
        3. 예문 2개
        """
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    
    def provide_feedback(self, student_answer: str, correct_answer: str) -> str:
        """학생 답변에 대한 피드백 제공"""
        prompt = f"""
        다음 학생 답변에 대한 피드백을 제공해주세요:
        
        학생 답변: {student_answer}
        정답: {correct_answer}
        
        다음 형식으로 작성해주세요:
        1. 정답 여부
        2. 잘한 점
        3. 개선이 필요한 점
        4. 추가 학습 팁
        """
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    
    def generate_similar_examples(self, expression: str) -> str:
        """유사 표현 및 예문 생성"""
        prompt = f"""
        다음 표현과 유사한 표현들을 생성하고 예문을 제공해주세요:
        표현: {expression}
        
        다음 형식으로 작성해주세요:
        1. 유사 표현 3개
        2. 각 표현의 예문
        3. 사용 시 주의사항
        """
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text 