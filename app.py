"""
🧠 스마트 퀴즈 앱 - Streamlit Cloud 배포용
"""
import streamlit as st
from quiz_app_mobile import MobileQuizApp

def main():
    # 페이지 설정
    st.set_page_config(
        page_title="스마트 퀴즈 📱",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"  # 모바일에서 사이드바 기본 닫힌 상태
    )
    
    # 모바일 퀴즈 앱 실행
    app = MobileQuizApp()
    app.run()

if __name__ == "__main__":
    main() 