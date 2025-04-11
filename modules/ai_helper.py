from anthropic import Anthropic
from typing import List, Dict, Any
import anthropic
import json

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
            model=self.model,
            max_tokens=4000,
            system="You are an English teacher creating test questions.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text
    
    def generate_fill_in_blank(self, text: str):
        prompt = f"""
        다음 영어 지문을 바탕으로 객관식 문제 5개를 생성해주세요.
        
        문제 생성 규칙:
        1. 각 문제는 지문의 핵심 내용을 정확하게 묻는 질문이어야 합니다.
        2. 보기는 4개이며, 정답은 지문에서 직접적으로 언급된 내용이어야 합니다.
        3. 해설은 지문의 구체적인 부분을 인용하여 설명해야 합니다.
        4. 문제, 보기, 정답, 해설은 모두 한국어로 작성해야 합니다.

        출력 형식:
        문제 1:
        문제 내용
        A) 보기 1
        B) 보기 2
        C) 보기 3
        D) 보기 4

        문제 2:
        문제 내용
        A) 보기 1
        B) 보기 2
        C) 보기 3
        D) 보기 4

        ...

        정답 1:
        정답
        해설

        정답 2:
        정답
        해설

        ...

        지문:
        {text}
        """
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            system="You are an English teacher creating multiple-choice questions. You must create questions that test comprehension of the text, with clear correct answers and detailed explanations.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        try:
            return response.content[0].text
        except:
            return ""
    
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
            model=self.model,
            max_tokens=4000,
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
            model=self.model,
            max_tokens=4000,
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