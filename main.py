import streamlit as st
import requests
import time
from kanjobunseki import analyze_sentiment

#タイトル
st.title('ご意見投稿フォーム')
st.caption('日々の業務のあれこれを上司へ匿名投稿するフォームです')

import streamlit as st
import requests

# セッションステート初期化
if "posting" not in st.session_state:
    st.session_state.posting = False

def post_with_retry(url, data, max_retries=5, wait_seconds=30):
    """
    スリープ中のRenderに対して、指定回数リトライしながらPOSTする関数
    """
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(url, json=data, timeout=10)
            if response.status_code == 200:
                return response
            else:
                print(f"[{attempt}回目] ステータスコード: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[{attempt}回目] 接続エラー: {e}")

        time.sleep(wait_seconds)

    raise Exception("Renderが起動せずタイムアウトしました。後でもう一度お試しください。")

def post_comment(yakusyoku, comment):
    # 感情分析 & POST送信をspinner内で実行
    with st.spinner("送信中です。少々お待ちください..."):
        sentiment_scores, predicted_sentiment = analyze_sentiment(comment)

        url = "https://pythonapi-egwh.onrender.com/postdata/"
        data = {
            "roll": yakusyoku,
            "data": comment,
            "sentiment": predicted_sentiment,
            "sentiment_score_spnegative": sentiment_scores['非常にネガティブ'],
            "sentiment_score_negative": sentiment_scores['ネガティブ'],
            "sentiment_score_neutral": sentiment_scores['ニュートラル'],
            "sentiment_score_positive": sentiment_scores['ポジティブ'],
            "sentiment_score_sppositive": sentiment_scores['非常にポジティブ']
        }

        response = post_with_retry(url, data, max_retries=10)

        response = requests.post(url, json=data)

    return response, sentiment_scores, predicted_sentiment

# フォームUI
with st.form(key='iken_form', clear_on_submit=True):
    yakusyoku = st.radio(
        '投稿したい役職を選択してください',
        ('社長', '事業部長', '部長', '課長', 'GL')
    )
    comment = st.text_area('投稿したい内容を入力してください', value=None, height=150, max_chars=1000)

    # 読み込み中はボタンを非活性化
    if st.session_state.posting:
        submit_btn = st.form_submit_button('投稿中...', disabled=True)
    else:
        submit_btn = st.form_submit_button('投稿')

    if submit_btn:
        st.session_state.posting = True  # 投稿中フラグON

        # 投稿処理（spinnerつき）
        response, sentiment_scores, predicted_sentiment = post_comment(yakusyoku, comment)

        if response.status_code == 200:
            st.success('✅ 投稿完了しました！')
            st.text('投稿内容確認')
            st.text(comment)
        else:
            st.error('❌ エラーが発生しました。再度お試しください。')
            print(f'エラー: {response.status_code} - {response.text}')

        st.session_state.posting = False  # 投稿完了後OFF
