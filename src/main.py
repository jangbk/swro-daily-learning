#!/usr/bin/env python3
"""
SWRO 해수담수화 플랜트 엔지니어 학습 메일 시스템
매일 체계적인 학습 콘텐츠를 이메일로 발송합니다.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from email_sender import EmailSender
from content_generator import ContentGenerator


def load_curriculum() -> dict:
    """커리큘럼 데이터 로드"""
    curriculum_path = Path(__file__).parent.parent / "data" / "curriculum.json"
    with open(curriculum_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_current_day(start_date: str) -> int:
    """시작일로부터 현재 학습 일차 계산"""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    today = datetime.now()
    delta = (today - start).days + 1

    # 365일 사이클로 반복
    if delta > 365:
        delta = ((delta - 1) % 365) + 1
    elif delta < 1:
        delta = 1

    return delta


def get_topic_for_day(curriculum: dict, day: int) -> dict:
    """특정 일차의 학습 주제 가져오기"""
    for module in curriculum["modules"]:
        for topic in module.get("topics", []):
            if topic["day"] == day:
                return {
                    "module": module,
                    "topic": topic
                }

    # 해당 일차에 정의된 주제가 없으면 AI로 생성
    return None


def create_email_content(curriculum: dict, day: int, topic_data: dict,
                         use_ai: bool = False, openai_api_key: str = None) -> str:
    """이메일 콘텐츠 생성"""
    program_info = curriculum["program_info"]

    if topic_data:
        module = topic_data["module"]
        topic = topic_data["topic"]

        # 기본 커리큘럼 기반 콘텐츠
        html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
        .header .day {{
            font-size: 18px;
            opacity: 0.9;
            margin-top: 5px;
        }}
        .header .level {{
            display: inline-block;
            background-color: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            margin-top: 10px;
            font-size: 14px;
        }}
        .module-info {{
            background-color: #e8f4fd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #2a5298;
        }}
        .section {{
            margin-bottom: 25px;
        }}
        .section h2 {{
            color: #1e3c72;
            border-bottom: 2px solid #2a5298;
            padding-bottom: 10px;
            font-size: 20px;
        }}
        .section h3 {{
            color: #2a5298;
            font-size: 18px;
            margin-top: 20px;
        }}
        .key-points {{
            background-color: #f8f9fa;
            padding: 15px 20px;
            border-radius: 8px;
        }}
        .key-points ul {{
            margin: 0;
            padding-left: 20px;
        }}
        .key-points li {{
            margin-bottom: 8px;
        }}
        .terms {{
            display: grid;
            gap: 10px;
        }}
        .term {{
            background-color: #fff3cd;
            padding: 12px 15px;
            border-radius: 6px;
            border-left: 3px solid #ffc107;
        }}
        .term strong {{
            color: #856404;
        }}
        .formula {{
            background-color: #e7f3e7;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            overflow-x: auto;
            border-left: 4px solid #28a745;
        }}
        .tip {{
            background-color: #d1ecf1;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #17a2b8;
        }}
        .tip-icon {{
            font-size: 20px;
            margin-right: 10px;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
            font-size: 14px;
        }}
        .progress {{
            margin-top: 20px;
        }}
        .progress-bar {{
            background-color: #e9ecef;
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
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
        .ai-content {{
            background-color: #f0f7ff;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
            border: 1px solid #b8daff;
        }}
        .ai-label {{
            display: inline-block;
            background-color: #007bff;
            color: white;
            padding: 3px 10px;
            border-radius: 3px;
            font-size: 12px;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{topic['title']}</h1>
            <div class="day">Day {day} / 365</div>
            <span class="level">{module['level']}</span>
        </div>

        <div class="module-info">
            <strong>모듈 {module['module_id']}:</strong> {module['title']}
        </div>

        <div class="section">
            <h2>오늘의 학습 내용</h2>
            <p>{topic['content']}</p>
        </div>

        <div class="section">
            <h3>핵심 포인트</h3>
            <div class="key-points">
                <ul>
                    {"".join(f'<li>{point}</li>' for point in topic['key_points'])}
                </ul>
            </div>
        </div>

        {"<div class='section'><h3>전문 용어</h3><div class='terms'>" +
         "".join(f'<div class="term"><strong>{term}:</strong> {desc}</div>'
                 for term, desc in topic.get('technical_terms', {}).items()) +
         "</div></div>" if topic.get('technical_terms') else ""}

        {"<div class='section'><h3>공식 및 계산</h3><div class='formula'>" +
         topic['formula'] + "</div></div>" if topic.get('formula') else ""}

        {"<div class='section'><h3>실무 팁</h3><div class='tip'><span class='tip-icon'>💡</span>" +
         topic['practical_tip'] + "</div></div>" if topic.get('practical_tip') else ""}
"""

        # AI 보충 설명 추가 (선택적)
        if use_ai and openai_api_key:
            generator = ContentGenerator(openai_api_key)
            ai_supplement = generator.generate_supplement(topic)
            if ai_supplement:
                html_content += f"""
        <div class="ai-content">
            <span class="ai-label">AI 보충 설명</span>
            <div>{ai_supplement}</div>
        </div>
"""

        # 진행률 및 푸터
        progress_percent = (day / 365) * 100
        html_content += f"""
        <div class="progress">
            <p><strong>전체 진행률</strong></p>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress_percent:.1f}%;">
                    {progress_percent:.1f}%
                </div>
            </div>
        </div>

        <div class="footer">
            <p>{program_info['title']}</p>
            <p>📧 매일 아침 발송되는 학습 메일입니다.</p>
            <p>학습 문의: 이 메일에 회신해 주세요.</p>
        </div>
    </div>
</body>
</html>
"""
    else:
        # 커리큘럼에 없는 날은 AI로 콘텐츠 생성
        if use_ai and openai_api_key:
            generator = ContentGenerator(openai_api_key)
            ai_content = generator.generate_daily_content(day, curriculum)
            html_content = ai_content
        else:
            html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>SWRO 학습 Day {day}</title>
</head>
<body>
    <h1>Day {day} 학습</h1>
    <p>오늘의 학습 콘텐츠가 준비 중입니다.</p>
    <p>AI 콘텐츠 생성을 위해 OpenAI API 키를 설정해 주세요.</p>
</body>
</html>
"""

    return html_content


def main():
    """메인 실행 함수"""
    # 환경 변수에서 설정 로드
    recipient_email = os.environ.get("RECIPIENT_EMAIL")
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")  # Gmail 앱 비밀번호
    start_date = os.environ.get("START_DATE", datetime.now().strftime("%Y-%m-%d"))
    use_ai = os.environ.get("USE_AI", "true").lower() == "true"
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    # 필수 환경 변수 확인
    if not all([recipient_email, sender_email, sender_password]):
        print("Error: 필수 환경 변수가 설정되지 않았습니다.")
        print("필요한 환경 변수:")
        print("  - RECIPIENT_EMAIL: 수신자 이메일")
        print("  - SENDER_EMAIL: 발신자 Gmail")
        print("  - SENDER_PASSWORD: Gmail 앱 비밀번호")
        return 1

    # 커리큘럼 로드
    curriculum = load_curriculum()

    # 현재 학습 일차 계산
    day = get_current_day(start_date)
    print(f"📚 현재 학습 일차: Day {day}")

    # 오늘의 학습 주제 가져오기
    topic_data = get_topic_for_day(curriculum, day)

    if topic_data:
        print(f"📖 오늘의 주제: {topic_data['topic']['title']}")
        print(f"   모듈: {topic_data['module']['title']}")
        print(f"   레벨: {topic_data['module']['level']}")
    else:
        print(f"📖 Day {day}에 대한 AI 생성 콘텐츠를 준비합니다.")

    # 이메일 콘텐츠 생성
    email_content = create_email_content(
        curriculum,
        day,
        topic_data,
        use_ai=use_ai,
        openai_api_key=openai_api_key
    )

    # 이메일 제목 생성
    if topic_data:
        subject = f"[SWRO 학습 Day {day}] {topic_data['topic']['title']}"
    else:
        subject = f"[SWRO 학습 Day {day}] 오늘의 학습 내용"

    # 이메일 발송
    email_sender = EmailSender(sender_email, sender_password)
    success = email_sender.send_html_email(
        to_email=recipient_email,
        subject=subject,
        html_content=email_content
    )

    if success:
        print(f"✅ 학습 메일이 {recipient_email}로 발송되었습니다.")
        return 0
    else:
        print("❌ 메일 발송에 실패했습니다.")
        return 1


if __name__ == "__main__":
    exit(main())
