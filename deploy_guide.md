# 🚀 스마트 퀴즈 앱 온라인 배포 가이드

## 📋 개요
Streamlit Cloud를 사용하여 무료로 온라인 배포하는 방법을 안내합니다.

## 🔧 준비사항

### 1. GitHub 계정 및 레포지토리 생성
1. **GitHub 계정** 생성 (없다면)
2. **새 레포지토리** 생성
   - 레포지토리 이름: `smart-quiz-app` (원하는 이름)
   - Public으로 설정
   - README.md 포함하여 생성

### 2. 파일 업로드
다음 파일들을 GitHub 레포지토리에 업로드하세요:

```
smart-quiz-app/
├── app.py                    # 메인 애플리케이션 파일
├── requirements_deploy.txt   # 패키지 의존성
└── README.md                # 설명 파일
```

### 3. Google Service Account 설정

#### 3.1 Google Cloud Console 설정
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성
3. "API 및 서비스" > "라이브러리" > "Google Sheets API" 활성화
4. "사용자 인증 정보" > "사용자 인증 정보 만들기" > "서비스 계정"
5. 서비스 계정 생성 후 JSON 키 다운로드

#### 3.2 구글 시트 공유
1. 학습용 구글 시트 생성 (A열: 질문, B열: 답)
2. JSON 키 파일에서 `client_email` 값 복사
3. 구글 시트를 해당 이메일과 공유 (보기 권한)

## 🌐 Streamlit Cloud 배포

### 1. Streamlit Cloud 가입
1. [share.streamlit.io](https://share.streamlit.io/) 접속
2. GitHub 계정으로 로그인
3. "New app" 클릭

### 2. 앱 설정
- **Repository**: 방금 생성한 GitHub 레포지토리 선택
- **Branch**: main (기본값)
- **Main file path**: app.py
- **App URL**: 원하는 URL 입력 (예: smart-quiz-app)

### 3. Secrets 설정
"Advanced settings" > "Secrets" 섹션에서 다음과 같이 설정:

```toml
[google_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"

# OpenAI API 키 (선택사항)
openai_api_key = "your-openai-api-key"
```

**주의**: JSON 키 파일의 내용을 위 형식으로 변환해서 입력하세요.

### 4. 배포 실행
"Deploy!" 버튼 클릭하면 자동으로 배포됩니다.

## 📱 사용 방법

### 1. 앱 접속
배포 완료 후 제공되는 URL로 접속
(예: `https://your-app-name.streamlit.app/`)

### 2. 구글 시트 연결
1. 사이드바에서 "Google Sheets" 섹션 열기
2. 구글 시트 ID 입력 (URL에서 `/d/` 뒤의 긴 문자열)
3. "데이터 로드" 버튼 클릭

### 3. 퀴즈 진행
- **새 질문 시작** → 퀴즈 시작
- **질문 카드 클릭** → 답 보기
- **외운 정도 선택** → 학습 효율 최적화
- **AI 설명** → 추가 설명 (OpenAI API 키 필요)

## 🎯 모바일 최적화 기능

- **반응형 디자인**: 모든 화면 크기 지원
- **터치 친화적**: 큰 버튼과 카드형 UI
- **빠른 로딩**: 최적화된 CSS와 애니메이션
- **컴팩트한 레이아웃**: 모바일 화면에 최적화

## 🔄 업데이트 방법

1. GitHub 레포지토리에서 파일 수정
2. 커밋 후 푸시
3. Streamlit Cloud에서 자동으로 재배포

## 🆓 무료 사용 한도

Streamlit Cloud 무료 계정:
- **1개 앱** 동시 실행
- **1GB RAM**
- **1 CPU 코어**
- **무제한 사용자**

일반적인 퀴즈 앱 사용에는 충분합니다!

## 📞 지원

문제가 발생하면:
1. Streamlit Cloud 로그 확인
2. GitHub 레포지토리의 Issues 탭 활용
3. Streamlit 커뮤니티 포럼 참조

## 🎉 배포 완료!

축하합니다! 이제 언제 어디서든 스마트폰이나 컴퓨터로 퀴즈 앱을 사용할 수 있습니다! 📚✨ 