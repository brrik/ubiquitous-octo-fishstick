import torch
from transformers import BertTokenizer, BertForSequenceClassification
from janome.tokenizer import Tokenizer  # Janomeのインポート

def analyze_sentiment(text):
    # Janomeの設定（日本語テキストを分かち書き）
    tokenizer = Tokenizer()  # Janomeのトークナイザーをインスタンス化
    
    # Janomeで分かち書き
    wakati_text = ' '.join([token.surface for token in tokenizer.tokenize(text)])
    
    # 日本語感情分析用のモデルとトークナイザーの準備
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    tokenizer_bert = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name)

    # トークナイズ
    inputs = tokenizer_bert(wakati_text, return_tensors='pt', truncation=True, padding=True)

    # 推論
    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=-1)

    # ラベル（感情のクラス）とその確率
    labels = ['非常にネガティブ', 'ネガティブ', 'ニュートラル', 'ポジティブ', '非常にポジティブ']
    result = {label: prob.item() for label, prob in zip(labels, probabilities[0])}
    
    # 最も確率が高い感情を予測
    predicted_class = torch.argmax(probabilities, dim=-1)
    predicted_label = labels[predicted_class.item()]

    return result, predicted_label

if __name__ == '__main__':
    # 分析する日本語のテキスト
    texts = [
        "今日はとてもいい日だ",
    ]

    for text in texts:
        sentiment_scores, predicted_sentiment = analyze_sentiment(text)
        print(f"テキスト: {text}")
        print(f"感情スコア: {sentiment_scores}")
        print(f"予測された感情: {predicted_sentiment}")
        print("-" * 30)
