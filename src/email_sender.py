#!/usr/bin/env python3
"""
Gmail SMTP를 이용한 이메일 발송 모듈
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


class EmailSender:
    """Gmail SMTP를 통한 이메일 발송 클래스"""

    def __init__(self, sender_email: str, sender_password: str):
        """
        Args:
            sender_email: 발신자 Gmail 주소
            sender_password: Gmail 앱 비밀번호 (2단계 인증 필요)
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_html_email(self, to_email: str, subject: str, html_content: str,
                        text_content: str = None) -> bool:
        """
        HTML 이메일 발송

        Args:
            to_email: 수신자 이메일 주소
            subject: 이메일 제목
            html_content: HTML 본문
            text_content: 텍스트 본문 (선택적, 없으면 간단한 텍스트 생성)

        Returns:
            bool: 발송 성공 여부
        """
        try:
            # 메시지 구성
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"SWRO Learning <{self.sender_email}>"
            msg["To"] = to_email
            msg["Date"] = formatdate(localtime=True)

            # 텍스트 버전 (HTML을 지원하지 않는 클라이언트용)
            if text_content is None:
                text_content = "이 이메일은 HTML 형식입니다. HTML을 지원하는 이메일 클라이언트에서 확인해 주세요."

            part1 = MIMEText(text_content, "plain", "utf-8")
            part2 = MIMEText(html_content, "html", "utf-8")

            msg.attach(part1)
            msg.attach(part2)

            # SMTP 연결 및 발송
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, to_email, msg.as_string())

            print(f"📧 이메일 발송 완료: {to_email}")
            return True

        except smtplib.SMTPAuthenticationError:
            print("❌ 인증 실패: Gmail 앱 비밀번호를 확인해 주세요.")
            print("   (Gmail 2단계 인증 활성화 후 앱 비밀번호 생성 필요)")
            return False

        except smtplib.SMTPException as e:
            print(f"❌ SMTP 에러: {e}")
            return False

        except Exception as e:
            print(f"❌ 이메일 발송 실패: {e}")
            return False

    def send_test_email(self, to_email: str) -> bool:
        """테스트 이메일 발송"""
        subject = "[SWRO 학습] 테스트 메일"
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .box { background: #e8f4fd; padding: 20px; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="box">
        <h1>🎉 테스트 성공!</h1>
        <p>SWRO 학습 메일 시스템이 정상적으로 설정되었습니다.</p>
        <p>내일부터 매일 아침 학습 메일이 발송됩니다.</p>
    </div>
</body>
</html>
"""
        return self.send_html_email(to_email, subject, html_content)


if __name__ == "__main__":
    import os

    # 환경 변수에서 설정 로드
    sender = os.environ.get("SENDER_EMAIL")
    password = os.environ.get("SENDER_PASSWORD")
    recipient = os.environ.get("RECIPIENT_EMAIL")

    if all([sender, password, recipient]):
        email_sender = EmailSender(sender, password)
        email_sender.send_test_email(recipient)
    else:
        print("환경 변수를 설정해 주세요:")
        print("  export SENDER_EMAIL='your-gmail@gmail.com'")
        print("  export SENDER_PASSWORD='your-app-password'")
        print("  export RECIPIENT_EMAIL='recipient@example.com'")
