import anthropic
from typing import List, Dict, Any, Optional
import re
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
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                system="You are an English teacher creating multiple-choice questions. Always provide ALL QUESTIONS first, then ALL ANSWERS AND EXPLANATIONS separately. Never mix them. Use Korean for question content. Add line breaks between questions and between explanations for better readability. Format each option (A, B, C, D) on a new line.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            if hasattr(response, 'content') and len(response.content) > 0:
                return response.content[0].text
            else:
                return "문제를 생성할 수 없습니다. 응답이 비어있습니다."
        except Exception as e:
            return f"문제 생성 중 오류가 발생했습니다: {str(e)[:100]}"
    
    def _create_default_question(self, error_msg: str = "") -> Dict[str, Any]:
        """기본 문제 객체 생성"""
        if error_msg:
            error_msg = f" - {error_msg}"
        
        return {
            "question": f"문제 생성 중 오류가 발생했습니다{error_msg}",
            "options": [
                "A) 다시 시도해주세요",
                "B) 다른 유형의 문제를 선택해보세요",
                "C) 난이도를 변경해보세요",
                "D) 다른 지문을 선택해보세요"
            ],
            "answer": "A",
            "explanation": "기술적인 문제로 문제 생성에 실패했습니다. 다시 시도해주세요."
        }
    
    def generate_single_question(self, text: str, difficulty: str = "medium", question_type: str = "comprehension") -> Dict[str, Any]:
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
            "answer": "A",
            "explanation": "자세한 해설"
        }}
        
        반드시 JSON 형식으로 응답해주세요. 다른 설명이나 텍스트는 포함하지 마세요.
        JSON 포맷을 정확히 지켜주세요. 특히 answer 필드는 A, B, C, D 중 하나만 포함해야 합니다.
        
        지문:
        {text}
        """
        
        try:
            # API 호출
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system="You are an English teacher creating multiple-choice questions for high school students. Create ONE question at a time. Return your response in valid JSON format with the following keys: question, options (array), answer (A, B, C, or D), and explanation. Use Korean for question content and explanations.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # 응답 확인
            if not hasattr(response, 'content') or len(response.content) == 0:
                return self._create_default_question("API 응답이 비어있습니다")
            
            # 응답 처리
            content = response.content[0].text
            
            # JSON 추출 시도
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if not json_match:
                return self._create_default_question("JSON 형식을 찾을 수 없습니다")
            
            json_str = json_match.group(0)
            
            # JSON 파싱 시도
            try:
                question_data = json.loads(json_str)
            except json.JSONDecodeError:
                return self._create_default_question("JSON 파싱 오류")
            
            # 필수 필드 검사 및 보정
            required_fields = ["question", "options", "answer", "explanation"]
            for field in required_fields:
                if field not in question_data:
                    if field == "options":
                        question_data[field] = ["A) 옵션이 없습니다", "B) 옵션2", "C) 옵션3", "D) 옵션4"]
                    elif field == "answer":
                        question_data[field] = "A"
                    else:
                        question_data[field] = f"{field} 필드가 누락되었습니다"
            
            # options 필드 검사
            if not isinstance(question_data["options"], list):
                question_data["options"] = ["A) 옵션이 올바르지 않습니다", "B) 옵션2", "C) 옵션3", "D) 옵션4"]
            elif len(question_data["options"]) < 2:
                while len(question_data["options"]) < 4:
                    question_data["options"].append(f"{chr(65 + len(question_data['options']))}) 추가 옵션")
            
            # answer 필드 검사 (A, B, C, D 중 하나인지)
            if not isinstance(question_data["answer"], str) or question_data["answer"] not in ["A", "B", "C", "D"]:
                question_data["answer"] = "A"
            
            return question_data
            
        except Exception as e:
            return self._create_default_question(str(e)[:50]) 