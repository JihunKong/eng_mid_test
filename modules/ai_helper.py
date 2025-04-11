from anthropic import Anthropic
from typing import List, Dict, Any
import anthropic
import json

class AIHelper:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API 키가 제공되지 않았습니다.")
        try:
            self.client = Anthropic()
            self.client.api_key = api_key
        except Exception as e:
            raise ValueError(f"Anthropic 클라이언트 초기화 실패: {str(e)}")
        self.model = "claude-3-7-sonnet-20250219"
    
    def generate_questions(self, text: str, difficulty: str = "medium", num_questions: int = 5) -> str:
        """지문 기반 문제 생성"""
        prompt = f"""
        다음 영어 지문을 바탕으로 {difficulty} 난이도의 객관식 문제 {num_questions}개를 생성해주세요.
        각 문제는 다음 형식을 따라야 합니다:
        1. 문제
        2. 4개의 보기 (A, B, C, D)
        3. 정답
        4. 해설

        지문:
        {text}
        """
        
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            temperature=0.7,
            system="You are an English teacher creating test questions.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text
    
    def generate_fill_in_blank(self, text: str):
        prompt = f"""
        다음 영어 지문을 바탕으로 빈칸 채우기 문제 5개를 생성해주세요.
        각 문제는 다음 형식을 따라야 합니다:
        1. 문장 (빈칸 포함)
        2. 정답
        3. 해설

        지문:
        {text}
        """
        
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            temperature=0.7,
            system="You are an English teacher creating fill-in-the-blank exercises.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text
    
    def generate_sentence_rearrangement(self, text: str):
        prompt = f"""
        다음 영어 지문을 바탕으로 문장 재배열 문제 5개를 생성해주세요.
        각 문제는 다음 형식을 따라야 합니다:
        1. 섞인 문장들
        2. 정답 순서
        3. 해설

        지문:
        {text}
        """
        
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            temperature=0.7,
            system="You are an English teacher creating sentence rearrangement exercises.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text
    
    def generate_matching_game(self, text: str):
        prompt = f"""
        다음 영어 지문을 바탕으로 매칭 게임 문제 5개를 생성해주세요.
        각 문제는 다음 형식을 따라야 합니다:
        1. 영어 단어/문장과 한국어 의미를 매칭하는 문제
        2. 정답
        3. 해설

        지문:
        {text}
        """
        
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            temperature=0.7,
            system="You are an English teacher creating matching game exercises.",
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
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise ValueError(f"단어 설명 생성 중 오류 발생: {str(e)}")
    
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
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise ValueError(f"피드백 생성 중 오류 발생: {str(e)}")
    
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
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise ValueError(f"유사 예문 생성 중 오류 발생: {str(e)}") 