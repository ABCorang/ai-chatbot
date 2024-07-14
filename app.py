import streamlit as st
import google.generativeai as genai
import os
from langchain_google_genai import GoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

import datetime
import base64


model_name = st.sidebar.radio('モデルを選択してください',
                    ['gemini-1.5-flash-latest',
                     'gemini-1.5-pro', 
                    'gemini-1.5-flash-001'])

# 温度設定
temperature = st.sidebar.slider('temperature', 
                  min_value=0.0, 
                  max_value=1.0, 
                  value=1.0)

# モデルのインスタンス化
api_key=os.environ['GOOGLE_API_KEY']
llm = GoogleGenerativeAI(model=model_name, temperature=temperature, google_api_key=api_key)

# プロンプトテンプレートの設定
tempate_prompt = ChatPromptTemplate.from_messages([
    ('system', 'あなたは対話AIであり、ゆらゆることを詳細に解説でき、人間の質問を理解するため次の文脈に基づいて回答してください'),
    MessagesPlaceholder(variable_name='conversation_history'),
    ('human', '{input}')
])

# チェイン作成
chain = tempate_prompt | llm

strealimit_history = StreamlitChatMessageHistory()

chat_chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: strealimit_history,
    input_messages_key='input',
    history_messages_key='conversation_history',
)


st.title('AIチャット')

# チャット履歴の初期化
# if 'langchain_messages' not in st.session_state:
#     st.session_state.langchain_messages = []

# チャット履歴の表示
for message in st.session_state['langchain_messages']:
    if message.type == 'human':
        role = 'human'
    else:
        role = 'AI'
    
    with st.chat_message(role):
        st.markdown(message.content)

user_input = st.chat_input('メッセージを入力してください:')

# 送信ボタン
if user_input:     
    with st.spinner('AI is typing ...'):
        # AIレスポンスを生成
        ai_response = chat_chain_with_history.stream({'input': user_input}, config={'configurable':{'session_id': "any"}})
        st.write_stream(ai_response)

# チャット履歴クリアボタン
clear_btn = st.sidebar.button('チャット履歴をクリア')
if clear_btn:
    st.session_state['langchain_messages'] = []
    st.rerun()

def convert_chat_to_markdown(messages):
    md_content = "# Chat History\n\n"
    for message in messages:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        role = "Human" if message.type == "human" else "AI"
        md_content += f"## {role} ({timestamp})\n\n{message.content}\n\n"
    return md_content

def get_markdown_download_link(md_content, filename="chat_history.md"):
    b64 = base64.b64encode(md_content.encode()).decode()
    href = f'<a href="data:file/markdown;base64,{b64}" download="{filename}">Download Markdown File</a>'
    return href

# Markdown出力ボタン
export_md_btn = st.sidebar.button('チャット履歴をMarkdownに出力')
if export_md_btn:
    md_content = convert_chat_to_markdown(st.session_state['langchain_messages'])
    md_download_link = get_markdown_download_link(md_content)
    st.sidebar.markdown(md_download_link, unsafe_allow_html=True)