# python -m pip install flask
# pip install openai==0.28



from flask import Flask, request, render_template_string
import openai

app = Flask(__name__)

# OpenAI APIキーの設定（環境変数や設定ファイルで管理することを推奨）
openai.api_key = "APIキーを入れる場所"

# 利用するモデル名（例："gpt-4"、"gpt-3.5-turbo"など）
MODEL_NAME = "gpt-4"

# HTMLテンプレート（個人情報登録フォーム）
form_template = '''
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>個人情報登録</title>
  </head>
  <body>
    <h1>個人情報登録フォーム</h1>
    <form action="/search" method="post">
      名前: <input type="text" name="name" required><br>
      年齢: <input type="number" name="age" required><br>
      住所: <input type="text" name="address" required><br>
      職業: <input type="text" name="occupation" required><br>
      年収 (円): <input type="number" name="income" required><br>
      家族構成: <input type="text" name="family_structure" placeholder="例：両親、妻、子供等" required><br>
      家族の名前と年齢 (例: 太郎:30, 花子:28): <input type="text" name="family_details" required><br>
      家族の年収 (円): <input type="number" name="family_income" required><br>
      <input type="submit" value="登録">
    </form>
  </body>
</html>
'''

# HTMLテンプレート（検索結果表示用）
result_template = '''
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>補助金提案結果</title>
  </head>
  <body>
    <h1>補助金提案結果</h1>
    <pre>{{ result }}</pre>
    <br>
    <a href="/">戻る</a>
  </body>
</html>
'''

@app.route("/", methods=["GET"])
def index():
    return render_template_string(form_template)

@app.route("/search", methods=["POST"])
def search():
    # フォームから個人情報を取得
    user_data = {
        "名前": request.form.get("name"),
        "年齢": request.form.get("age"),
        "住所": request.form.get("address"),
        "職業": request.form.get("occupation"),
        "年収": request.form.get("income"),
        "家族構成": request.form.get("family_structure"),
        "家族の名前と年齢": request.form.get("family_details"),
        "家族の年収": request.form.get("family_income")
    }
    
    # ChatGPTへの問い合わせ用プロンプトを作成
    prompt = f"""
ユーザーの登録情報は以下の通りです：
名前: {user_data['名前']}
年齢: {user_data['年齢']}
住所: {user_data['住所']}
職業: {user_data['職業']}
年収: {user_data['年収']}
家族構成: {user_data['家族構成']}
家族の名前と年齢: {user_data['家族の名前と年齢']}
家族の年収: {user_data['家族の年収']}

この情報に基づいて、以下の4つの観点から、ユーザーが受給可能なまたは受給の可能性がある東京都の補助金・助成金を提案してください。

1. 現在受給可能な補助金
2. ユーザーがいくつかの質問に答えることで受給可能な補助金
3. ユーザーやお子さんの年齢・学年が変化した場合に将来受給可能な補助金
4. ユーザーやご家族の年収が変化した場合に受給可能な補助金

それぞれの補助金候補について、補助金名とその理由を簡潔に説明してください。
    """
    
    try:
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=600
        )
        suggestion = response["choices"][0]["message"]["content"]
    except Exception as e:
        suggestion = f"補助金提案の生成中にエラーが発生しました: {e}"
    
    return render_template_string(result_template, result=suggestion)

if __name__ == "__main__":
    # アプリケーションをデバッグモードで実行（本番環境ではオフにする）
    app.run(debug=True, port=5000)