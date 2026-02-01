#!/usr/bin/env python3
"""
SWRO 해수담수화 플랜트 엔지니어 학습 메일 시스템
90일 집중 과정으로 전문가 수준까지 도달
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

from email_sender import EmailSender


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

    max_days = 90  # 90일 과정
    if delta > max_days:
        delta = ((delta - 1) % max_days) + 1
    elif delta < 1:
        delta = 1
    return delta


def get_topic_for_day(curriculum: dict, day: int) -> dict:
    """특정 일차의 학습 주제 가져오기"""
    for module in curriculum["modules"]:
        for topic in module.get("topics", []):
            if topic["day"] == day:
                return {"module": module, "topic": topic}
    return None


def generate_terms_section(terms: dict) -> str:
    """전문 용어 섹션 생성"""
    if not terms:
        return ""
    items = "".join(f'<div class="term"><strong>{term}:</strong> {desc}</div>' for term, desc in terms.items())
    return f"<div class='section'><h2>📚 전문 용어</h2><div class='terms'>{items}</div></div>"


def markdown_to_html(text: str) -> str:
    """간단한 마크다운을 HTML로 변환"""
    if not text:
        return ""

    # 헤더 변환
    text = re.sub(r'^## (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)

    # 굵은 글씨
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

    # 코드 블록
    text = re.sub(r'```\n?(.*?)\n?```', r'<pre class="code-block">\1</pre>', text, flags=re.DOTALL)

    # 인라인 코드
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)

    # 줄바꿈
    text = text.replace('\n\n', '</p><p>')
    text = text.replace('\n', '<br>')

    return f"<p>{text}</p>"


def create_email_content(curriculum: dict, day: int, topic_data: dict) -> str:
    """풍부한 학습 콘텐츠 이메일 생성"""
    program_info = curriculum["program_info"]
    max_days = program_info.get("duration_days", 90)

    if not topic_data:
        return f"<html><body><h1>Day {day} 콘텐츠 준비 중</h1></body></html>"

    module = topic_data["module"]
    topic = topic_data["topic"]
    progress_percent = (day / max_days) * 100

    # 확장 콘텐츠 섹션 생성
    detailed_section = ""
    if topic.get("detailed_explanation"):
        detailed_section = f'''
        <div class="section detailed">
            <h2>📖 상세 학습 내용</h2>
            <div class="detailed-content">
                {markdown_to_html(topic["detailed_explanation"])}
            </div>
        </div>'''

    exercises_section = ""
    if topic.get("exercises"):
        exercises_section = f'''
        <div class="section exercises">
            <h2>✏️ 연습 문제</h2>
            <div class="exercises-content">
                {markdown_to_html(topic["exercises"])}
            </div>
        </div>'''

    quiz_section = ""
    if topic.get("quiz"):
        quiz_items = ""
        for i, q in enumerate(topic["quiz"], 1):
            if isinstance(q, dict):
                quiz_items += f'''
                <div class="quiz-item">
                    <p><strong>Q{i}.</strong> {q.get("q", q.get("question", ""))}</p>
                    <p class="quiz-answer">💡 정답: {q.get("a", q.get("answer", ""))}</p>
                </div>'''
        if quiz_items:
            quiz_section = f'''
            <div class="section quiz">
                <h2>🧠 오늘의 퀴즈</h2>
                {quiz_items}
            </div>'''

    html_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SWRO 학습 Day {day}</title>
    <style>
        body {{ font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif; line-height: 1.9; color: #333; max-width: 900px; margin: 0 auto; padding: 15px; background: #f0f4f8; }}
        .container {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #0d47a1 0%, #1976d2 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 25px; }}
        .header h1 {{ margin: 0 0 10px 0; font-size: 26px; }}
        .header .meta {{ opacity: 0.9; font-size: 15px; }}
        .level-badge {{ display: inline-block; background: rgba(255,255,255,0.25); padding: 6px 16px; border-radius: 20px; margin-top: 12px; font-size: 13px; }}
        .module-info {{ background: #e3f2fd; padding: 18px; border-radius: 10px; margin-bottom: 25px; border-left: 5px solid #1976d2; font-size: 15px; }}
        .section {{ margin-bottom: 30px; padding: 20px; background: #fafafa; border-radius: 10px; }}
        .section h2 {{ color: #0d47a1; font-size: 20px; margin: 0 0 18px 0; padding-bottom: 12px; border-bottom: 2px solid #1976d2; }}
        .section h3 {{ color: #1565c0; font-size: 17px; margin: 20px 0 12px 0; }}
        .section h4 {{ color: #1976d2; font-size: 15px; margin: 15px 0 10px 0; }}
        .key-points {{ background: #fff; padding: 18px 22px; border-radius: 8px; border: 1px solid #e0e0e0; }}
        .key-points ul {{ margin: 0; padding-left: 22px; }}
        .key-points li {{ margin-bottom: 10px; }}
        .terms {{ display: grid; gap: 12px; }}
        .term {{ background: #fff8e1; padding: 14px 18px; border-radius: 8px; border-left: 4px solid #ffc107; }}
        .term strong {{ color: #f57c00; }}
        .formula {{ background: #e8f5e9; padding: 18px; border-radius: 8px; font-family: 'Consolas', 'Monaco', monospace; white-space: pre-wrap; border-left: 4px solid #4caf50; font-size: 14px; overflow-x: auto; }}
        .tip {{ background: #e1f5fe; padding: 18px; border-radius: 8px; border-left: 4px solid #03a9f4; }}
        .detailed-content {{ background: #fff; padding: 20px; border-radius: 8px; border: 1px solid #e0e0e0; }}
        .detailed-content h3 {{ color: #1565c0; border-bottom: 1px solid #e0e0e0; padding-bottom: 8px; }}
        .detailed-content h4 {{ color: #1976d2; }}
        .detailed-content pre {{ background: #263238; color: #aed581; padding: 15px; border-radius: 6px; overflow-x: auto; }}
        .exercises-content {{ background: #fff3e0; padding: 20px; border-radius: 8px; }}
        .quiz-item {{ background: #fff; padding: 15px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #e0e0e0; }}
        .quiz-answer {{ color: #2e7d32; font-weight: 500; margin-top: 8px; }}
        .code-block {{ background: #263238; color: #aed581; padding: 12px; border-radius: 6px; display: block; margin: 10px 0; }}
        code {{ background: #eceff1; padding: 2px 6px; border-radius: 4px; font-size: 13px; }}
        .progress {{ margin-top: 25px; }}
        .progress-bar {{ background: #e0e0e0; border-radius: 10px; height: 24px; overflow: hidden; }}
        .progress-fill {{ background: linear-gradient(90deg, #4caf50, #8bc34a); height: 100%; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px; font-weight: bold; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0; text-align: center; color: #757575; font-size: 13px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th, td {{ border: 1px solid #e0e0e0; padding: 10px; text-align: left; }}
        th {{ background: #f5f5f5; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{topic['title']}</h1>
            <div class="meta">Day {day} / {max_days} | 3개월 전문가 속성 과정</div>
            <span class="level-badge">📚 {module['level']}</span>
        </div>

        <div class="module-info">
            <strong>모듈 {module['module_id']}:</strong> {module['title']} ({module['duration_days']}일)
        </div>

        <div class="section">
            <h2>🎯 오늘의 학습 목표</h2>
            <p style="font-size: 16px; color: #424242;">{topic['content']}</p>
        </div>

        <div class="section">
            <h2>📌 핵심 포인트</h2>
            <div class="key-points">
                <ul>
                    {"".join(f'<li>{point}</li>' for point in topic['key_points'])}
                </ul>
            </div>
        </div>

        {generate_terms_section(topic.get('technical_terms', {}))}

        {"<div class='section'><h2>📐 공식 및 계산</h2><div class='formula'>" + topic['formula'] + "</div></div>" if topic.get('formula') else ""}

        {"<div class='section'><h2>💡 실무 팁</h2><div class='tip'>" + topic['practical_tip'] + "</div></div>" if topic.get('practical_tip') else ""}

        {detailed_section}
        {exercises_section}
        {quiz_section}

        <div class="progress">
            <p><strong>전체 진행률</strong> (Day {day}/{max_days})</p>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress_percent:.1f}%;">{progress_percent:.1f}%</div>
            </div>
        </div>

        <div class="footer">
            <p><strong>{program_info['title']}</strong></p>
            <p>📧 매일 아침 발송되는 전문가 학습 메일</p>
        </div>
    </div>
</body>
</html>'''

    return html_content


def main():
    """메인 실행 함수"""
    recipient_email = os.environ.get("RECIPIENT_EMAIL")
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    start_date = os.environ.get("START_DATE", datetime.now().strftime("%Y-%m-%d"))

    if not all([recipient_email, sender_email, sender_password]):
        print("Error: 필수 환경 변수가 설정되지 않았습니다.")
        return 1

    curriculum = load_curriculum()
    day = get_current_day(start_date)
    print(f"📚 현재 학습 일차: Day {day}")

    topic_data = get_topic_for_day(curriculum, day)

    if topic_data:
        print(f"📖 오늘의 주제: {topic_data['topic']['title']}")
        subject = f"[SWRO Day {day}] {topic_data['topic']['title']}"
    else:
        print(f"📖 Day {day} 콘텐츠 없음")
        subject = f"[SWRO Day {day}] 학습 내용"

    email_content = create_email_content(curriculum, day, topic_data)

    email_sender = EmailSender(sender_email, sender_password)
    success = email_sender.send_html_email(
        to_email=recipient_email,
        subject=subject,
        html_content=email_content
    )

    if success:
        print(f"✅ 학습 메일 발송 완료: {recipient_email}")
        return 0
    else:
        print("❌ 메일 발송 실패")
        return 1


if __name__ == "__main__":
    exit(main())
