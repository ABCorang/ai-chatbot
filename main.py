import streamlit as st
import google.generativeai as genai
import os

# Gemini APIの設定
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest')

# Streamlitアプリケーションの基本構造
st.title('AIチャットアシスタント')

# チャット履歴の初期化
if 'messages' not in st.session_state:
    st.session_state.messages = []




# チャット履歴の表示
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input('メッセージを入力してください:')

# 送信ボタン
if user_input:
    # ユーザーメッセージを追加
    st.session_state.messages.append({'role': 'user', 'content': user_input})
        
    with st.spinner("LLM is typing ..."):

        # AIレスポンスを生成
        model_response = model.generate_content(user_input)
    
        # AIレスポンスを追加
    st.session_state.messages.append({'role': 'assistant', 'content': model_response.text})
    st.session_state.user_input = "" # テキストボックスをクリア


    # チャット履歴を更新
    st.rerun()