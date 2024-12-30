import streamlit as st
import requests
from kanjobunseki import analyze_sentiment

#タイトル
st.title('ご意見投稿フォーム')
st.caption('日々の業務のあれこれを上司へ匿名投稿するフォームです')

#入力内容が完了するまでリロードされないようにwith句を使う
with st.form(key='iken_form', clear_on_submit=True):
    #役職ラジオボックス 第一引数でタイトル。第二引数でボタン名
    yakusyoku = st.radio(
        '投稿したい役職を選択してください',
        ('社長','事業部長','部長','課長','GL')
    )

    #入力ボックス
    comment = st.text_area('投稿したい内容を入力してください', value=None, height=150, max_chars=1000)

    #送信ボタン
    submit_btn = st.form_submit_button('投稿')
    if submit_btn:
        #ここで感情分析する
        if __name__ == '__main__':
            sentiment_scores, predicted_sentiment = analyze_sentiment(comment)

        #本番url = "https://pythonapi-egwh.onrender.com/postdata/"
        #テストurl = "https://altxfastapi-test.onrender.com/postdata/"        
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
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            st.success(f'投稿完了しました！')
            st.text(f'投稿内容確認')
            st.text(f'{comment}')
        else:
            st.error('エラーが発生しました。再度お試しください。')
            print(f'エラー: {response.status_code} - {response.text}')