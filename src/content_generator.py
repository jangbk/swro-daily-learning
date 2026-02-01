#!/usr/bin/env python3
"""
OpenAI API를 이용한 AI 콘텐츠 생성 모듈
"""

import os
from typing import Optional

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class ContentGenerator:
    """OpenAI API를 이용한 학습 콘텐츠 생성"""

    def __init__(self, api_key: str):
        """
        Args:
            api_key: OpenAI API 키
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("openai 패키지가 설치되지 않았습니다. pip install openai")

        self.client = openai.OpenAI(api_key=api_key)

    def generate_supplement(self, topic: dict) -> Optional[str]:
        """
        기존 토픽에 대한 AI 보충 설명 생성

        Args:
            topic: 커리큘럼 토픽 데이터

        Returns:
            str: AI가 생성한 보충 설명 (HTML 형식)
        """
        prompt = f"""당신은 SWRO(해수역삼투) 해수담수화 플랜트 전문가입니다.
다음 학습 주제에 대해 실무 엔지니어에게 도움이 되는 보충 설명을 작성해 주세요.

주제: {topic['title']}
내용: {topic['content']}
핵심 포인트: {', '.join(topic['key_points'])}

다음 내용을 포함해 주세요:
1. 실제 현장에서 겪을 수 있는 상황 예시
2. 자주 하는 실수와 주의사항
3. 관련 산업 표준이나 가이드라인 (있다면)

형식: 간결한 HTML (p, ul, li 태그 사용). 200자 내외로 작성해 주세요."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "SWRO 해수담수화 플랜트 전문 기술 컨설턴트"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content

        except Exception as e:
            print(f"AI 콘텐츠 생성 실패: {e}")
            return None

    def generate_daily_content(self, day: int, curriculum: dict) -> str:
        """
        특정 일차에 대한 전체 학습 콘텐츠 생성 (커리큘럼에 없는 날)

        Args:
            day: 학습 일차
            curriculum: 전체 커리큘럼 데이터

        Returns:
            str: 전체 이메일 HTML 콘텐츠
        """
        # 해당 일차가 속한 모듈 찾기
        current_module = None
        for module in curriculum["modules"]:
            if module["start_day"] <= day < module["start_day"] + module["duration_days"]:
                current_module = module
                break

        if current_module is None:
            # 마지막 모듈 사용
            current_module = curriculum["modules"][-1]

        prompt = f"""당신은 SWRO 해수담수화 플랜트 전문가 교육자입니다.
'{current_module['title']}' 모듈의 Day {day} 학습 콘텐츠를 생성해 주세요.

레벨: {current_module['level']}
모듈 설명: {current_module['title']}

다음 구조로 작성해 주세요:
1. 오늘의 학습 주제 (제목)
2. 학습 목표 (3-4개 bullet points)
3. 핵심 개념 설명
4. 관련 수식이나 계산 (있다면)
5. 실무 적용 팁

HTML 형식으로 깔끔하게 작성해 주세요."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "SWRO 해수담수화 플랜트 교육 전문가"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )

            ai_content = response.choices[0].message.content
            progress_percent = (day / 365) * 100

            return f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>SWRO 학습 Day {day}</title>
    <style>
        body {{
            font-family: 'Noto Sans KR', 'Malgun Gothic', sans-serif;
            line-height: 1.8;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 25px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .ai-badge {{
            display: inline-block;
            background-color: #007bff;
            color: white;
            padding: 3px 10px;
            border-radius: 3px;
            font-size: 12px;
            margin-bottom: 10px;
        }}
        .content {{
            padding: 20px;
        }}
        .progress-bar {{
            background-color: #e9ecef;
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
            margin-top: 20px;
        }}
        .progress-fill {{
            background: linear-gradient(90deg, #28a745, #20c997);
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 12px;
            font-weight: bold;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Day {day} - {current_module['title']}</h1>
            <span class="ai-badge">AI Generated Content</span>
        </div>

        <div class="content">
            {ai_content}
        </div>

        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress_percent:.1f}%;">
                {progress_percent:.1f}%
            </div>
        </div>

        <div class="footer">
            <p>{curriculum['program_info']['title']}</p>
            <p>📧 매일 아침 발송되는 학습 메일입니다.</p>
        </div>
    </div>
</body>
</html>
"""

        except Exception as e:
            print(f"AI 콘텐츠 생성 실패: {e}")
            return f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>SWRO 학습 Day {day}</title>
</head>
<body>
    <h1>Day {day} 학습</h1>
    <p>AI 콘텐츠 생성 중 오류가 발생했습니다.</p>
    <p>오류: {str(e)}</p>
</body>
</html>
"""


def generate_quiz(topic: dict, api_key: str) -> Optional[dict]:
    """
    학습 주제에 대한 퀴즈 생성

    Args:
        topic: 학습 주제 데이터
        api_key: OpenAI API 키

    Returns:
        dict: 퀴즈 데이터 (질문, 선택지, 정답, 해설)
    """
    if not OPENAI_AVAILABLE or not api_key:
        return None

    client = openai.OpenAI(api_key=api_key)

    prompt = f"""다음 SWRO 학습 주제에 대한 객관식 퀴즈 1문제를 생성해 주세요.

주제: {topic['title']}
내용: {topic['content']}

JSON 형식으로 응답해 주세요:
{{
    "question": "질문 내용",
    "options": ["A. 선택지1", "B. 선택지2", "C. 선택지3", "D. 선택지4"],
    "correct": "A",
    "explanation": "정답 해설"
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "SWRO 기술 퀴즈 출제자"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
            response_format={"type": "json_object"}
        )

        import json
        return json.loads(response.choices[0].message.content)

    except Exception as e:
        print(f"퀴즈 생성 실패: {e}")
        return None
