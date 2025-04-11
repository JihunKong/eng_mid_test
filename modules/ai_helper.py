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
        """지문 기반 문제 생성"""
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
        
        지문:
        {text}
        """
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            system="You are an English teacher creating multiple-choice questions. Always provide ALL QUESTIONS first, then ALL ANSWERS AND EXPLANATIONS separately. Never mix them. Use Korean for question content. Add line breaks between questions and between explanations for better readability.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text 