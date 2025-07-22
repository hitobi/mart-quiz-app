import streamlit as st
import pandas as pd
import random
import json

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import openai
from typing import Dict, List, Tuple
import os

# Google Sheets API 스코프
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# 모바일 최적화 CSS
def load_mobile_css():
    st.markdown("""
    <style>
    /* 모바일 최적화 스타일 */
    .main .block-container {
        padding: 1rem;
        max-width: 100%;
    }
    
    /* 사이드바 모바일 최적화 */
    .css-1d391kg {
        padding-top: 1rem;
    }
    
    /* 버튼 크기 최적화 */
    .stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0.5rem 0;
        border-radius: 12px;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* 질문 카드 스타일 */
    .question-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .question-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
    }
    
    /* 답 카드 스타일 */
    .answer-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(17, 153, 142, 0.3);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* 설명 카드 스타일 */
    .explanation-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #8b4513;
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        box-shadow: 0 6px 24px rgba(252, 182, 159, 0.3);
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* 메모리 레벨 버튼 */
    .memory-low { background: linear-gradient(135deg, #ff6b6b, #ee5a52); }
    .memory-mid { background: linear-gradient(135deg, #feca57, #ff9ff3); }
    .memory-high { background: linear-gradient(135deg, #48dbfb, #0abde3); }
    
    /* 통계 카드 */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 0.5rem;
    }
    
    /* 헤더 스타일 */
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 2rem;
    }
    
    /* 모바일에서 텍스트 크기 조정 */
    @media (max-width: 768px) {
        .question-card, .answer-card {
            padding: 1.5rem;
            font-size: 1.1rem;
        }
        
        .main-header {
            font-size: 2rem;
        }
        
        .stButton > button {
            height: 2.5rem;
            font-size: 1rem;
        }
    }
    
    /* 터치 피드백 */
    .question-card:active,
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* 로딩 애니메이션 */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)

class MobileQuizApp:
    def __init__(self):
        self.initialize_session_state()
        load_mobile_css()
        
    def initialize_session_state(self):
        """세션 상태 초기화"""
        if 'questions_data' not in st.session_state:
            st.session_state.questions_data = []
        if 'current_question' not in st.session_state:
            st.session_state.current_question = None
        if 'show_answer' not in st.session_state:
            st.session_state.show_answer = False
        if 'memory_levels' not in st.session_state:
            st.session_state.memory_levels = {}
        if 'google_sheets_service' not in st.session_state:
            st.session_state.google_sheets_service = None
        if 'show_explanation' not in st.session_state:
            st.session_state.show_explanation = False
        if 'explanation_text' not in st.session_state:
            st.session_state.explanation_text = ""
            
    def authenticate_google_sheets(self):
        """Google Sheets API 인증 (Streamlit Secrets 사용)"""
        try:
            # Streamlit secrets에서 Google 서비스 계정 정보 가져오기
            google_credentials = st.secrets["google_service_account"]
            credentials_dict = dict(google_credentials)
            
            # 서비스 계정 인증
            creds = service_account.Credentials.from_service_account_info(
                credentials_dict, scopes=SCOPES)
            
            service = build('sheets', 'v4', credentials=creds)
            st.session_state.google_sheets_service = service
            return service
            
        except Exception as e:
            st.error(f"Google Sheets 인증 실패: {str(e)}")
            st.error("관리자에게 문의하세요.")
            return None
    
    def load_questions_from_sheets(self, spreadsheet_id: str, range_name: str = 'A:B'):
        """Google Sheets에서 질문과 답 로드"""
        if not st.session_state.google_sheets_service:
            st.error("Google Sheets 서비스가 인증되지 않았습니다.")
            return []
            
        try:
            sheet = st.session_state.google_sheets_service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=spreadsheet_id, 
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            if not values:
                st.error("시트에 데이터가 없습니다.")
                return []
            
            questions_data = []
            for i, row in enumerate(values[1:], 1):  # 첫 번째 행은 헤더로 건너뛰기
                if len(row) >= 2:
                    question_data = {
                        'id': i,
                        'question': row[0],
                        'answer': row[1],
                        'memory_level': st.session_state.memory_levels.get(i, '하')
                    }
                    questions_data.append(question_data)
            
            st.session_state.questions_data = questions_data
            return questions_data
            
        except HttpError as error:
            st.error(f"Google Sheets 데이터 로드 실패: {error}")
            return []
    
    def get_weighted_random_question(self) -> dict:
        """가중치 기반 랜덤 질문 선택"""
        if not st.session_state.questions_data:
            return None
        
        # 메모리 레벨에 따른 가중치 (하:3, 중:2, 상:1)
        weights = []
        for q in st.session_state.questions_data:
            memory_level = st.session_state.memory_levels.get(q['id'], '하')
            if memory_level == '하':
                weights.append(3)
            elif memory_level == '중':
                weights.append(2)
            else:  # '상'
                weights.append(1)
        
        # 가중치 기반 랜덤 선택
        selected_question = random.choices(st.session_state.questions_data, weights=weights, k=1)[0]
        return selected_question
    
    def get_chatgpt_explanation(self, question: str, answer: str) -> str:
        """ChatGPT API를 사용한 설명 생성"""
        try:
            # Streamlit secrets에서 OpenAI API 키 가져오기
            api_key = st.secrets.get("openai_api_key", "")
            if not api_key:
                return "OpenAI API 키가 설정되지 않았습니다. 관리자에게 문의하세요."
                
            client = openai.OpenAI(api_key=api_key)
            
            prompt = f"""다음 질문과 답에 대해 간단하고 이해하기 쉬운 설명을 한국어로 제공해주세요.

질문: {question}
답: {answer}

설명은 2-3문장으로 간단하게 작성해주세요."""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 도움이 되는 학습 보조 AI입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"설명 생성 중 오류가 발생했습니다: {str(e)}"
    
    def update_memory_level(self, question_id: int, level: str):
        """메모리 레벨 업데이트"""
        st.session_state.memory_levels[question_id] = level
        
        # questions_data의 해당 질문도 업데이트
        for q in st.session_state.questions_data:
            if q['id'] == question_id:
                q['memory_level'] = level
                break
    
    def run(self):
        """메인 앱 실행"""
        # 헤더
        st.markdown('<h1 class="main-header">🧠 스마트 퀴즈</h1>', unsafe_allow_html=True)
        
        # 모바일용 컴팩트 사이드바
        with st.sidebar:
            st.markdown("### ⚙️ 설정")
            
            # Google Sheets 설정 (접힌 상태로 시작)
            with st.expander("📊 Google Sheets", expanded=False):
                spreadsheet_id = st.text_input(
                    "스프레드시트 ID", 
                    help="Google Sheets URL의 ID 부분"
                )
                
                if st.button("🔄 데이터 로드", use_container_width=True):
                    if spreadsheet_id:
                        with st.spinner("로딩중..."):
                            service = self.authenticate_google_sheets()
                            if service:
                                questions = self.load_questions_from_sheets(spreadsheet_id)
                                if questions:
                                    st.success(f"✅ {len(questions)}개 로드완료!")
                                    st.rerun()
                                else:
                                    st.error("❌ 로드 실패")
                    else:
                        st.error("ID를 입력하세요")
        
        # 메인 컨텐츠
        if not st.session_state.questions_data:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 16px; margin: 2rem 0;">
                <h3>📋 시작하기</h3>
                <p>사이드바에서 Google Sheets를 설정하고<br>'데이터 로드' 버튼을 눌러주세요!</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin: 1rem 0;">
                <h4>📖 사용 방법:</h4>
                <ul>
                    <li><strong>Google Sheets 준비</strong>: A열에 질문, B열에 답</li>
                    <li><strong>공유 설정</strong>: 시트를 공개 또는 특정 계정과 공유</li>
                    <li><strong>스프레드시트 ID</strong>: URL에서 ID 부분 복사해서 입력</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            return
        
        # 통계 표시 (모바일용 컴팩트)
        col1, col2 = st.columns(2)
        with col1:
            total = len(st.session_state.questions_data)
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #667eea; margin: 0;">{total}</h3>
                <p style="margin: 0; color: #666;">전체 문제</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            levels = {'상': 0, '중': 0, '하': 0}
            for q in st.session_state.questions_data:
                levels[q.get('memory_level', '하')] += 1
            
            st.markdown(f"""
            <div class="metric-card">
                <p style="margin: 0; color: #666;">외운정도</p>
                <div style="display: flex; justify-content: space-around; margin-top: 0.5rem;">
                    <span style="color: #48dbfb;">🟢{levels['상']}</span>
                    <span style="color: #feca57;">🟡{levels['중']}</span>
                    <span style="color: #ff6b6b;">🔴{levels['하']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 새 질문 시작 또는 현재 질문 표시
        if st.session_state.current_question is None:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🎲 새 질문 시작", use_container_width=True, type="primary"):
                    st.session_state.current_question = self.get_weighted_random_question()
                    st.session_state.show_answer = False
                    st.session_state.show_explanation = False
                    st.rerun()
        else:
            # 현재 질문 표시
            current_q = st.session_state.current_question
            memory_level = st.session_state.memory_levels.get(current_q['id'], '하')
            
            # 메모리 레벨 표시
            level_colors = {'상': '🟢', '중': '🟡', '하': '🔴'}
            level_names = {'상': '잘 기억함', '중': '보통', '하': '복습 필요'}
            st.markdown(f"""
            <div style="text-align: center; margin: 1rem 0;">
                <span style="font-size: 1.2rem;">{level_colors[memory_level]} {level_names[memory_level]}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # 질문 카드
            if not st.session_state.show_answer:
                if st.button("", key="question_btn"):
                    st.session_state.show_answer = True
                    st.rerun()
                
                st.markdown(f"""
                <div class="question-card" onclick="window.parent.document.querySelector('[data-testid=\"stButton\"]').click()">
                    <h2 style="margin: 0; font-weight: 600;">❓ 질문</h2>
                    <p style="font-size: 1.3rem; margin: 1rem 0; line-height: 1.5;">{current_q['question']}</p>
                    <p style="opacity: 0.8; margin: 0;">👆 탭해서 답 보기</p>
                </div>
                """, unsafe_allow_html=True)
            
            # 답 표시
            if st.session_state.show_answer:
                st.markdown(f"""
                <div class="answer-card">
                    <h2 style="margin: 0; font-weight: 600;">✅ 답</h2>
                    <p style="font-size: 1.3rem; margin: 1rem 0; line-height: 1.5;">{current_q['answer']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # AI 설명 표시
                if st.session_state.show_explanation and st.session_state.explanation_text:
                    st.markdown(f"""
                    <div class="explanation-card">
                        <h4 style="margin: 0 0 1rem 0;">🤖 AI 설명</h4>
                        <p style="margin: 0; line-height: 1.6;">{st.session_state.explanation_text}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 액션 버튼들 (모바일 최적화)
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("💡 설명", use_container_width=True):
                        with st.spinner("AI가 설명을 생성중..."):
                            explanation = self.get_chatgpt_explanation(
                                current_q['question'], 
                                current_q['answer']
                            )
                            st.session_state.explanation_text = explanation
                            st.session_state.show_explanation = True
                            st.rerun()
                
                with col2:
                    if st.button("➡️ 다음", use_container_width=True, type="primary"):
                        st.session_state.current_question = self.get_weighted_random_question()
                        st.session_state.show_answer = False
                        st.session_state.show_explanation = False
                        st.session_state.explanation_text = ""
                        st.rerun()
                
                # 외운 정도 선택 (모바일 최적화)
                st.markdown("### 🎯 외운 정도를 선택하세요")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("🔴\n하\n(더 자주)", key="low", use_container_width=True):
                        self.update_memory_level(current_q['id'], '하')
                        st.success("🔴 복습 필요로 설정!")
                        st.rerun()
                
                with col2:
                    if st.button("🟡\n중\n(보통)", key="mid", use_container_width=True):
                        self.update_memory_level(current_q['id'], '중')
                        st.success("🟡 보통으로 설정!")
                        st.rerun()
                
                with col3:
                    if st.button("🟢\n상\n(덜 자주)", key="high", use_container_width=True):
                        self.update_memory_level(current_q['id'], '상')
                        st.success("🟢 잘 기억함으로 설정!")
                        st.rerun()

def main():
    st.set_page_config(
        page_title="스마트 퀴즈 📱",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"  # 모바일에서 사이드바 기본 닫힘
    )
    
    app = MobileQuizApp()
    app.run()

if __name__ == "__main__":
    main() 