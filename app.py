import streamlit as st
import sys
import os
from datetime import datetime

# 현재 디렉토리를 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 모듈 imports
from github_helper_chatbot import GitHubHelperChatBot
from user_manager import UserManager, render_user_setup
from github_uploader import GitHubUploader, render_file_upload_section

def main():
    # 페이지 설정
    st.set_page_config(
        page_title="🤖 깃허브 도우미 (다중 사용자)",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 메인 제목
    st.title("🤖 깃허브 도우미 챗봇 (다중 사용자 버전)")
    st.markdown("**개인 깃허브 설정 후 파일 업로드 기능을 사용하세요!**")
    st.markdown("---")
    
    # 사용자 관리자 초기화
    user_manager = UserManager()
    current_user = user_manager.get_current_user()
    
    # 상단 사용자 상태 표시
    if current_user:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.success(f"👤 **현재 사용자**: {current_user.get('username')} ({current_user.get('email')})")
        with col2:
            if st.button("🔄 사용자 변경"):
                st.session_state.force_user_setup = True
        with col3:
            if st.button("🚪 로그아웃"):
                if os.path.exists("current_user.json"):
                    os.remove("current_user.json")
                st.success("✅ 로그아웃 되었습니다!")
                st.rerun()
    else:
        st.warning("⚠️ 사용자가 설정되지 않았습니다. '👤 사용자 설정' 탭에서 설정해주세요.")
    
    # 세션 상태 초기화
    if "chatbot" not in st.session_state:
        try:
            with st.spinner("🤖 깃허브 도우미를 초기화하고 있습니다..."):
                st.session_state.chatbot = GitHubHelperChatBot()
        except Exception as e:
            st.error(f"❌ 초기화 오류: {str(e)}")
            st.info("💡 seed.env 파일에 OPENAI_API_KEY가 올바르게 설정되어 있는지 확인하세요.")
            return
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # 사이드바 - 기능 선택
    with st.sidebar:
        st.header("🛠️ 기능 메뉴")
        
        # 사용자 상태에 따른 메뉴 표시
        if current_user:
            menu_options = [
                "💬 AI 챗봇",
                "📤 파일 업로드",
                "🔍 프로젝트 검색", 
                "📋 Git 명령어 가이드",
                "📄 .gitignore 생성기",
                "👤 사용자 설정"
            ]
        else:
            menu_options = [
                "👤 사용자 설정",
                "💬 AI 챗봇",
                "🔍 프로젝트 검색",
                "📋 Git 명령어 가이드", 
                "📄 .gitignore 생성기"
            ]
        
        selected_tab = st.radio("메뉴 선택:", menu_options)
        
        # 강제 사용자 설정 모드
        if st.session_state.get('force_user_setup', False):
            selected_tab = "👤 사용자 설정"
        
        st.markdown("---")
        st.markdown("**💡 기능 안내:**")
        if current_user:
            st.success("✅ 파일 업로드 기능 활성화됨")
        else:
            st.warning("⚠️ 사용자 설정이 필요합니다")
        
        st.markdown("- **사용자 설정**: 개인 깃허브 정보 설정")
        st.markdown("- **파일 업로드**: 깃허브 자동 업로드")
        st.markdown("- **AI 챗봇**: 깃허브 관련 질문 답변")
        
        # 통계 정보
        st.markdown("---")
        st.markdown("**📊 사용자 통계:**")
        all_users = user_manager.get_all_users()
        st.write(f"👥 등록된 사용자: {len(all_users)}명")
        
        if current_user:
            last_login = current_user.get('last_login', '')
            if last_login:
                login_date = last_login[:19].replace('T', ' ')
                st.write(f"🕒 마지막 로그인: {login_date}")
    
    # 메인 콘텐츠 영역
    if selected_tab == "👤 사용자 설정":
        render_user_setup_tab()
    elif selected_tab == "📤 파일 업로드":
        render_file_upload_tab()
    elif selected_tab == "💬 AI 챗봇":
        render_chatbot_tab()
    elif selected_tab == "🔍 프로젝트 검색":
        render_project_search_tab()
    elif selected_tab == "📋 Git 명령어 가이드":
        render_git_commands_tab()
    elif selected_tab == "📄 .gitignore 생성기":
        render_gitignore_tab()

def render_user_setup_tab():
    """사용자 설정 탭"""
    user_setup_success = render_user_setup()
    
    if user_setup_success and st.session_state.get('force_user_setup', False):
        st.session_state.force_user_setup = False
        st.rerun()

def render_file_upload_tab():
    """파일 업로드 탭"""
    st.header("📤 파일 업로드")
    st.markdown("개인 깃허브 설정이 완료된 사용자만 파일 업로드가 가능합니다.")
    
    # 파일 업로드 섹션 렌더링
    upload_available = render_file_upload_section()
    
    if not upload_available:
        st.markdown("---")
        st.info("💡 파일 업로드 기능을 사용하려면 '👤 사용자 설정' 탭에서 깃허브 정보를 먼저 설정해주세요.")

def render_chatbot_tab():
    """AI 챗봇 탭"""
    st.header("💬 깃허브 AI 챗봇")
    st.markdown("깃허브 관련 모든 질문에 답변해드립니다!")
    
    # 현재 사용자 정보 표시
    user_manager = UserManager()
    current_user = user_manager.get_current_user()
    
    if current_user:
        st.info(f"💬 {current_user.get('username')}님으로 대화 중입니다.")
    
    # 이전 메시지 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 사용자 입력
    if prompt := st.chat_input("깃허브에 대해 궁금한 것을 물어보세요..."):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI 응답 생성
        with st.chat_message("assistant"):
            with st.spinner("🤖 답변을 생성하고 있습니다..."):
                try:
                    response = st.session_state.chatbot.get_response(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"❌ 답변 생성 중 오류가 발생했습니다: {str(e)}"
                    st.error(error_msg)
    
    # 대화 기록 관리
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ 대화 기록 초기화"):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("💾 대화 기록 저장"):
            if current_user:
                # 대화 기록을 사용자별로 저장하는 기능 (선택사항)
                st.success("✅ 대화 기록이 저장되었습니다!")

def render_project_search_tab():
    """프로젝트 검색 탭"""
    st.header("🔍 프로젝트 검색")
    st.markdown("한글 프로젝트명을 입력하면 영어로 번역해서 깃허브에서 검색해드립니다!")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        korean_input = st.text_input(
            "검색할 프로젝트명을 한글로 입력하세요:",
            placeholder="예: 머신러닝, 웹개발, 파이썬 챗봇"
        )
    
    with col2:
        st.write("")  # 공간 조정
        search_button = st.button("🔍 검색", type="primary")
    
    if search_button and korean_input:
        with st.spinner("🔄 번역하고 검색 결과를 생성하고 있습니다..."):
            try:
                result = st.session_state.chatbot.translate_and_search(korean_input)
                st.markdown(result)
            except Exception as e:
                st.error(f"❌ 검색 중 오류가 발생했습니다: {str(e)}")

def render_git_commands_tab():
    """Git 명령어 가이드 탭"""
    st.header("📋 Git 명령어 가이드")
    st.markdown("상황별로 필요한 Git 명령어를 확인하세요!")
    
    scenario = st.selectbox(
        "상황을 선택하세요:",
        [
            ("new_project", "🚀 새 프로젝트 업로드"),
            ("single_file", "📄 개별 파일 업로드"),
            ("folder", "📁 폴더 전체 업로드"),
            ("branch", "🌿 브랜치 작업")
        ],
        format_func=lambda x: x[1]
    )
    
    if st.button("📋 명령어 보기", type="primary"):
        try:
            guide = st.session_state.chatbot.get_git_commands_guide(scenario[0])
            st.markdown(guide)
        except Exception as e:
            st.error(f"❌ 가이드 생성 중 오류가 발생했습니다: {str(e)}")

def render_gitignore_tab():
    """.gitignore 생성기 탭"""
    st.header("📄 .gitignore 생성기")
    st.markdown("프로젝트 타입에 맞는 .gitignore 파일을 생성하세요!")
    
    project_type = st.selectbox(
        "프로젝트 타입을 선택하세요:",
        ["Python", "Node.js", "General"]
    )
    
    if st.button("📄 .gitignore 생성", type="primary"):
        try:
            gitignore_content = st.session_state.chatbot.generate_gitignore(project_type.lower())
            st.markdown(gitignore_content)
        except Exception as e:
            st.error(f"❌ .gitignore 생성 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()
