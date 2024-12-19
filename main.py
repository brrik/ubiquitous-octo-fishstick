import streamlit as st
import requests

#タイトル
st.title('ご意見投稿フォーム')
st.caption('日々の業務のあれこれを上司へ匿名投稿するフォームです')

#入力内容が完了するまでリロードされないようにwith句を使う
with st.form(key='iken_form', clear_on_submit=True):
    #役職ラジオボックス 第一引数でタイトル。第二引数でボタン名
    yakusyoku = st.radio(
        '投稿したい役職を選択してください',
        ('社長','事業部長','部長','課長','GL','その他')
    )

    #入力ボックス
    comment = st.text_area('投稿したい内容を入力してください', value=None, height=150, max_chars=1000)

    #送信ボタン
    submit_btn = st.form_submit_button('投稿')
    if submit_btn:
        st.text(f'投稿完了しました！')
        st.text(f'投稿内容確認')
        st.text(f'{comment}')

        url = "https://pythonapi-egwh.onrender.com/postdata/"
        data = {
            "roll": yakusyoku,
            "data": comment
        }

        response = requests.post(url, json=data)

        #役職、投稿内容、レスポンス確認用[200]で成功　消しても良い
        print(f'選択された役職: {yakusyoku}')
        print(f'投稿された内容: {comment}')
        print(response)