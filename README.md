# SWRO 해수담수화 플랜트 엔지니어 일일 학습 시스템

매일 아침 SWRO(Seawater Reverse Osmosis) 해수담수화 플랜트의 Process & Mechanical 엔지니어링 학습 메일을 자동으로 발송하는 시스템입니다.

## 📚 학습 과정 구성

| 단계 | 기간 | 레벨 | 주요 내용 |
|------|------|------|----------|
| 1 | Day 1-30 | 기초 | 담수화 기술 개요, RO 원리, 플랜트 구성 |
| 2 | Day 31-60 | 중급 | 전처리 시스템 설계 |
| 3 | Day 61-100 | 중급 | RO 시스템 설계 |
| 4 | Day 101-135 | 중급 | 기계 장비 설계 |
| 5 | Day 136-180 | 고급 | 운전 최적화 |
| 6 | Day 181-220 | 고급 | 트러블슈팅 |
| 7 | Day 221-265 | 고급 | 프로젝트 엔지니어링 |
| 8 | Day 266-315 | 전문가 | 신기술 및 고급 주제 |
| 9 | Day 316-365 | 전문가 | 리더십 및 관리 |

## 🚀 설정 방법

### 1. Gmail 앱 비밀번호 생성

1. Google 계정 > 보안 > 2단계 인증 활성화
2. 보안 > 앱 비밀번호 > 메일 선택 > 16자리 비밀번호 생성
3. 이 비밀번호를 `SENDER_PASSWORD`로 사용

### 2. GitHub Repository 설정

1. 이 코드를 GitHub에 Push
2. Repository > Settings > Secrets and variables > Actions
3. 다음 Secrets 추가:

| Secret Name | 설명 | 예시 |
|-------------|------|------|
| `SENDER_EMAIL` | 발신자 Gmail 주소 | your-email@gmail.com |
| `SENDER_PASSWORD` | Gmail 앱 비밀번호 | xxxx xxxx xxxx xxxx |
| `RECIPIENT_EMAIL` | 수신자 이메일 주소 | recipient@example.com |
| `START_DATE` | 학습 시작일 (선택) | 2025-02-01 |
| `USE_AI` | AI 보충 설명 사용 (선택) | true |
| `OPENAI_API_KEY` | OpenAI API 키 (선택) | sk-... |

### 3. 워크플로우 활성화

1. Repository > Actions 탭
2. "I understand my workflows, go ahead and enable them" 클릭
3. 매일 아침 8시(한국시간)에 자동 실행됨

### 4. 수동 테스트

1. Actions > "SWRO Daily Learning Email" 선택
2. "Run workflow" 클릭
3. 이메일 수신 확인

## 📁 프로젝트 구조

```
swro-daily-learning/
├── .github/
│   └── workflows/
│       └── daily-email.yml    # GitHub Actions 워크플로우
├── data/
│   └── curriculum.json        # 365일 커리큘럼 데이터
├── src/
│   ├── main.py               # 메인 스크립트
│   ├── email_sender.py       # 이메일 발송 모듈
│   └── content_generator.py  # AI 콘텐츠 생성 모듈
├── requirements.txt
└── README.md
```

## 🔧 로컬 실행 (테스트용)

```bash
# 환경 변수 설정
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="recipient@example.com"
export START_DATE="2025-02-01"
export USE_AI="false"  # AI 사용 시 true

# 실행
cd src
python main.py
```

## 📧 이메일 예시

![email-sample](https://via.placeholder.com/600x400?text=SWRO+Learning+Email+Sample)

매일 발송되는 학습 메일에는 다음 내용이 포함됩니다:

- 📖 오늘의 학습 주제
- 🎯 핵심 포인트
- 📚 전문 용어 설명
- 📐 관련 공식 및 계산
- 💡 실무 팁
- 📊 전체 진행률
- 🤖 AI 보충 설명 (선택)

## ⚙️ 커스터마이징

### 커리큘럼 수정

`data/curriculum.json` 파일을 수정하여 학습 내용을 커스터마이즈할 수 있습니다.

```json
{
  "day": 1,
  "title": "학습 주제",
  "content": "학습 내용 설명",
  "key_points": ["포인트1", "포인트2"],
  "technical_terms": {"용어": "설명"},
  "formula": "관련 공식",
  "practical_tip": "실무 팁"
}
```

### 발송 시간 변경

`.github/workflows/daily-email.yml`에서 cron 표현식 수정:

```yaml
schedule:
  - cron: '0 23 * * *'  # UTC 23:00 = KST 08:00
```

## 🔒 보안 참고사항

- Gmail 앱 비밀번호는 반드시 GitHub Secrets에 저장
- OpenAI API 키도 Secrets에 저장
- 코드에 비밀번호를 직접 입력하지 마세요

## 📝 라이선스

MIT License

## 🙋 문의

문의사항이 있으시면 Issue를 등록해 주세요.
