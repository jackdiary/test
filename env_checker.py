import os
from dotenv import load_dotenv

def check_env_file():
    """seed.env 파일 형식과 API 키 유효성 확인"""
    try:
        # seed.env 파일 로드
        load_dotenv('seed.env')
        
        # OpenAI API 키 확인
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            print("❌ 오류: OPENAI_API_KEY가 seed.env 파일에 설정되지 않았습니다.")
            print("📋 올바른 seed.env 파일 형식:")
            print("OPENAI_API_KEY=sk-your-actual-api-key-here")
            return False
        
        if not api_key.startswith('sk-'):
            print("❌ 오류: OpenAI API 키 형식이 올바르지 않습니다.")
            print("🔑 API 키는 'sk-'로 시작해야 합니다.")
            return False
        
        print(f"✅ API 키가 올바르게 설정되었습니다: {api_key[:10]}...")
        print("🚀 챗봇을 시작할 준비가 완료되었습니다!")
        return True
        
    except FileNotFoundError:
        print("❌ 오류: seed.env 파일을 찾을 수 없습니다.")
        print("📋 seed.env 파일을 생성하고 다음 형식으로 작성하세요:")
        print("OPENAI_API_KEY=sk-your-actual-api-key-here")
        return False
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    check_env_file()
