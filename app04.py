# 구글의 생성형 AI(Gemini)를 이용한 관상 웹앱을 구현 합니다.

import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- 1. 기본 설정 및 API 키 연결 ---
st.set_page_config(page_title="관상가 양반", page_icon="🧙‍♂️")

# 비밀 금고(secrets.toml)에서 API 키를 꺼내옵니다.
# 만약 에러가 난다면 5-C 단계를 다시 확인해주세요.
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("API 키가 없습니다. .streamlit/secrets.toml 파일을 확인해주세요!")

# --- 2. 화면 구성 ---
st.title("운명을 읽어주는 AI 관상가 🧙‍♂️")
st.markdown("### 당신의 얼굴에 숨겨진 운명을 봅니다.")
st.write("---") # 구분선

# --- 3. 이미지 입력 (카메라 or 파일) ---
camera_image = st.camera_input("📸 카메라로 바로 찍기")
uploaded_file = st.file_uploader("📂 앨범에서 사진 선택", type=['jpg', 'jpeg', 'png'])

final_image = None

# 우선순위: 카메라 > 파일 업로드
if camera_image:
    final_image = camera_image
    st.success("카메라 사진이 확인되었습니다.")
elif uploaded_file:
    final_image = uploaded_file
    st.success("앨범 사진이 확인되었습니다.")

# --- 4. 분석 로직 ---
if final_image:
    # 이미지를 화면에 표시
    img = Image.open(final_image)
    st.image(img, caption='관상을 볼 얼굴', use_container_width=True)

    # 버튼을 누르면 분석 시작
    if st.button("🔮 관상 보기 (운명 확인)"):
        with st.spinner("하늘의 기운을 읽고 있습니다... 잠시만 기다리시오..."):
            try:
                # 1) 사용할 모델 선택 (Gemini 1.5 Flash가 빠르고 쌉니다)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # 2) AI에게 시킬 명령(프롬프트) 작성
                prompt = """
                당신은 조선 시대부터 전해져 내려오는 전설적인 관상가입니다. 
                이 사진의 인물을 보고 다음 내용을 바탕으로 관상을 아주 상세하고 재미있게 봐주세요.
                말투는 사극 톤("~하오", "~이오")을 사용하세요.
                
                1. 전체적인 인상과 초년/중년/말년 운
                2. 재물운과 성격의 장단점
                3. 연애운 혹은 대인관계
                4. 조심해야 할 점과 행운의 조언
                
                좋은 말만 하지 말고, 따끔한 조언도 섞어서 아주 신비롭게 말해주세요.
                """
                
                # 3) AI에게 이미지와 명령 전달
                response = model.generate_content([prompt, img])
                
                # 4) 결과 출력
                st.write("---")
                st.subheader("📜 관상 결과")
                st.write(response.text)
                st.balloons() # 풍선 효과 팡팡!

            except Exception as e:
                st.error(f"에러가 발생했소. 사진을 다시 찍어보시오. (내용: {e})")
else:
    st.info("얼굴이 잘 나온 사진을 준비하시오.")