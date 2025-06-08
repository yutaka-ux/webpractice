# app.py

from flask import Flask, render_template, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# データベース接続情報 (あなたの環境に合わせて変更してください)
DB_HOST = "localhost"
DB_NAME = "sneaker_db"
DB_USER = "dubianyu" # あなたのユーザー名に設定
DB_PASSWORD = "z2543xy" # あなたのPostgreSQLパスワードに設定

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn

# ルートパス (index.htmlを表示)
@app.route('/')
def index():
    return render_template('index.html')

# brands/index.html に対応するエンドポイント
@app.route('/brands/index.html')
def brands_page():
    return render_template('brands/index.html')

# ブランド詳細ページへのルーティング (例: brands/brand-a.html)
@app.route('/brands/<brand_name>.html')
def brand_detail_page(brand_name):
    return render_template(f'brands/{brand_name}.html')

# 検索APIエンドポイント
@app.route('/api/search_sneakers')
def search_sneakers():
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()

    sneakers = []
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        sql_query = """
            SELECT
                s.model_name,
                s.description AS model_description,
                s.thumbnail_url,
                b.name AS brand_name,
                b.description AS brand_description,
                b.logo_image_url,
                b.category AS brand_category
            FROM
                sneakers s
            JOIN
                brands b ON s.brand_id = b.id
            WHERE
                LOWER(s.model_name) LIKE %s OR LOWER(s.description) LIKE %s OR LOWER(b.name) LIKE %s
        """
        params = [f"%{query.lower()}%", f"%{query.lower()}%", f"%{query.lower()}%"]

        if category:
            sql_query += " AND b.category = %s"
            params.append(category)

        cur.execute(sql_query, tuple(params))
        sneakers = cur.fetchall()

        cur.close()
        conn.close()
    except Exception as e:
        print(f"データベースエラー: {e}")
        return jsonify({"error": "データベースエラーが発生しました。"})

    return jsonify(sneakers)

if __name__ == '__main__':
    app.run(debug=True)
