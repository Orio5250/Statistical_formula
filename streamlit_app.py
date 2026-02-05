import streamlit as st
import pandas as pd

st.set_page_config(page_title="統計学クイズ", layout="centered")

# CSVの読み込み
@st.cache_data
def load_data():
    # 上記のCSVを 'quiz_data.csv' として保存している前提
    return pd.read_csv('quiz_data.csv')

df = load_data()

# セッション状態の初期化
if 'idx' not in st.session_state:
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.show_ans = False

st.title("📊 統計学マスタークイズ")
st.write("回帰分析・判別分析の数式をマスターしましょう。")

if st.session_state.idx < len(df):
    row = df.iloc[st.session_state.idx]
    
    st.subheader(f"問題 {st.session_state.idx + 1}")
    st.markdown(row['question'])
    
    # 選択肢の表示
    options = [row['option1'], row['option2'], row['option3'], row['option4']]
    
    with st.form(key='quiz_form'):
        answer = st.radio("正しい数式を選んでください", options)
        submit = st.form_submit_button("回答を確定する")
        
    if submit:
        st.session_state.show_ans = True
        if answer == row['answer']:
            st.session_state.score += 1
            st.success("✨ 正解です！")
        else:
            st.error(f"❌ 不正解... 正解は: {row['answer']}")
        st.info(f"💡 解説: {row['explanation']}")

    if st.session_state.show_ans:
        if st.button("次の問題へ"):
            st.session_state.idx += 1
            st.session_state.show_ans = False
            st.rerun()

else:
    st.balloons()
    st.header("全問終了！")
    st.metric("あなたのスコア", f"{st.session_state.score} / {len(df)}")
    if st.button("最初から解き直す"):
        st.session_state.idx = 0
        st.session_state.score = 0
        st.rerun()
