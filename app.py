import streamlit as st
import google.generativeai as genai
import os

# Gemini APIの設定
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

model_name = st.sidebar.radio('モデルを選択してください',
                    ['gemini-1.5-pro-latest', 
                    'gemini-1.5-flash-latest',
                    'gemini-1.5-flash-001'])

# 温度設定
temperature = st.sidebar.slider('temperature', 
                  min_value=0.0, 
                  max_value=1.0, 
                  value=0.5)
# 生成設定
generation_config = {
    'temperature': temperature
}

# モデルのインスタンス化
def get_model(model_name, generation_config):
    return genai.GenerativeModel(model_name, generation_config=generation_config)


st.title('AIチャットアシスタント')

# チャット履歴の初期化
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []




# チャット履歴の表示
for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input('メッセージを入力してください:')

# 送信ボタン
if user_input:
    # ユーザーメッセージを追加
    st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        
    with st.spinner('LLM is typing ...'):
        # 関数からモデルを取得
        model = get_model(model_name, generation_config)
        # AIレスポンスを生成
        ai_response = model.generate_content(user_input)

    # AIレスポンスを追加
    st.session_state.chat_history.append({'role': 'assistant', 'content': ai_response.text})
    # チャット履歴を更新
    st.rerun()

# チャット履歴クリアボタン
clear_btn = st.sidebar.button('チャット履歴をクリア')
if clear_btn:
    st.session_state.chat_history = []
    st.rerun()


