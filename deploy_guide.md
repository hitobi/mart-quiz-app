# 🚀 스마트 퀴즈 앱 배포 가이드 (완전 자동화 버전)

## 📋 개요
이 가이드는 Streamlit Cloud에서 **모든 설정을 자동화**하여 사용자가 별도 입력 없이 바로 퀴즈를 이용할 수 있도록 하는 방법을 설명합니다.

## 🔧 1단계: Streamlit Cloud Secrets 설정

Streamlit Cloud → 앱 → **⚙️ Settings** → **🔐 Secrets**에서 아래 내용을 **전체 복사**해서 붙여넣으세요:

```toml
# Google Service Account 인증 정보
[google_service_account]
type = "service_account"
project_id = "inner-deck-466504-v0"
private_key_id = "f8074e583f2579fc02467282abfa489dd408b94d"
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCM5OJRxD7idgvS\neKp85E1QjTMFp2uVwXnFewOJL8RoGiq6o5lfJu5jREfsLkUYdgUZtHQSq3StF6PQ\nkuO7j18OD//QL+LSS+DevHRYvCldM5pGstA4xiXpGmXMb2Jjh/domGCBs0VviXLV\n4bTZ1knSSTHPxFFk1oFLNuzedngAW55Cre1aIIVxxGWMPBUHkoeLpTwgvGhhVPAx\nN1zKpTLoVEYu/MPUTSH7fXYmlOEdH1U7deEBxprQG4fUzho8J4pi4nQwXYt4lr2T\nsnOfBYQ7DCQQCB3+VIOGbxRuju3Sklf6lTZ5UsiviC5EHe8M08KUJJ5+lsH8ZnB2\n4l30H9nPAgMBAAECggEAOjuTqvXwg8sEgd4roOj/Z46kiu6ykbfgq5V3VakvhVNj\nW7aoemJt3wtmqqBJIJ4O55vk6Z6B39TIeTls9KWCRR6pvZM9LWv9KjI76D0E36en\nWRco5n5HRvwJHSDgSoD06f8ozBKbXUky9GGQTQS7iDWGZ/gdKA9cawjth9jxKjwW\noJ4qNYhQ6iozJq1BFl1EhWj6QQqGlkQ2eRfE/3W7BlYS7Uq8kVpw3DSTp9Yjd4zv\nQ+FrRNtXmR6vEbN5qiO9BiBsZnrm6k4Qsy1lFAw5atQN94AcMnMHo4vjuLl9Vao5\nPKzcPGwiPBUwMIMvTb6tFDGV0cEZR2Pmy9+6rffvwQKBgQDGF0GwE9zSUmZJ9kC/\nhLSkpXKwzH/Ofb+23XE8AP/0ZZDHaQWq3TIPDb5YVvuXz2/G0kbzlwkWss/C7ZIm\nFLxSFGlAZ7sf+8RrZOsTt+CwOt8JoFhFzQ80nqeh96OyburaF2/hKtz7VXCiCovH\nQpBY9mlzJ8TtGLOpjiKxris64QKBgQC2FSE6aeY5jKYVdAx6/PYSlStHkw9OTTgM\neEMWtfFSBF/GYVpOaPPoKByp/n8pLENc14vDcTygyz+6DMJTMnkEU8CZjaXRia9B\n9mSgu5c1o4X2uZyzF4YkNatibgYBldfpCNhWJ4cjeiLsmY+82jUYjk9rAev94iWM\nazvuCU/arwKBgESmGqWivIxG8hv/s0CsBM5qZ+zNch1lhuMgqvVYg1t3N01kIAqu\nzYJaCPUkb9yUjvAgP2Z7mTK8lTPAkT2RQhJP8InZaQgUgGWXe8BBoSRxwonbf7vw\n7KwXr5B5+ckEl28tYCBwclTHr1j4vqg3cT7jZnf5+E0SmnDQSUW6TlEBAoGBAKh5\nbpBc8h+nqvjIss+NhaX2DeChCpV5z3WCRRkbadlooLGu3F8Wry/NBZCpIUGYag/a\nhMBm4yEoTqO4MInIdr7xO5EYxifWTKos8Djkuelwj4CVh48SIhUY76YYhUgsPGWr\nwHgfBORnmy7ue1fTUzOQYZ1yXsg/2lxN0FrUlOWTAoGAXlWx+5uCM2h9S1Crxcrb\nBbxKWNtyyTLom4Eh7bkQWEtFbeU2IxeCxZU8eaOOxZ6jBxYpqcqkMTxXq8mZ3L/d\nUb2hqglzNQLBPahVqU87nVSIUCJarjyUZ98JPxIiYS9k35zbpRJIi+q9/429Dig+\nhAerxI62K9sP12heyw4+d1k=\n-----END PRIVATE KEY-----\n"
client_email = "quiz-app-service@inner-deck-466504-v0.iam.gserviceaccount.com"
client_id = "104288279989230642040"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/quiz-app-service%40inner-deck-466504-v0.iam.gserviceaccount.com"
universe_domain = "googleapis.com"

# 스프레드시트 ID (자동 로드용)
spreadsheet_id = "여기에_본인의_구글시트_ID"

# OpenAI API 키 (AI 설명 기능용)
openai_api_key = "여기에_OpenAI_API_키"
```

## 🔑 2단계: 설정값 교체

위 템플릿에서 **2개 값만** 본인 것으로 교체하세요:

### 📊 스프레드시트 ID
```toml
spreadsheet_id = "1ABC...XYZ"  # 본인의 구글시트 ID
```

### 🤖 OpenAI API 키 (선택사항)
```toml
openai_api_key = "sk-..."  # 본인의 OpenAI API 키
```

## 📋 3단계: 구글 시트 공유 설정

구글 시트를 서비스 계정과 공유하세요:
1. 구글 시트 열기
2. **공유** 버튼 클릭  
3. 이메일: `quiz-app-service@inner-deck-466504-v0.iam.gserviceaccount.com`
4. 권한: **편집자** 또는 **보기 권한자**

## 🎯 완료!

이제 **Streamlit Cloud**에서:
- ✅ **자동으로** 데이터 로드
- ✅ **설정 입력** 불필요  
- ✅ **바로 퀴즈** 시작 가능
- ✅ **AI 설명** 자동 작동

## 🔄 동작 방식

### 🌐 웹 (Streamlit Cloud)
1. 앱 접속
2. 자동으로 데이터 로드
3. 바로 "새 질문 시작" 클릭
4. 퀴즈 진행

### 💻 로컬 개발
1. 사이드바에서 수동 설정
2. credentials.json 파일 필요
3. 개발/테스트용

## 📞 문제 해결

**데이터 로드 실패 시:**
- Secrets 설정 확인
- 스프레드시트 공유 확인  
- 스프레드시트 ID 확인

**AI 설명 안 됨:**
- OpenAI API 키 확인
- API 키 유효성 확인 