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

# スニーカー一覧取得API
@app.route('/api/sneakers')
def get_sneakers():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # クエリパラメータの取得
        brand_id = request.args.get('brand_id')
        category = request.args.get('category')
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)

        # 基本のSQLクエリ
        sql_query = """
            SELECT
                s.id,
                s.model_name,
                s.description,
                s.thumbnail_url,
                s.price,
                s.release_date,
                b.name as brand_name,
                b.logo_image_url
            FROM sneakers s
            JOIN brands b ON s.brand_id = b.id
            WHERE 1=1
        """
        params = []

        # フィルター条件の追加
        if brand_id:
            sql_query += " AND s.brand_id = %s"
            params.append(brand_id)
        if category:
            sql_query += " AND b.category = %s"
            params.append(category)

        # ページネーション
        sql_query += " ORDER BY s.release_date DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        cur.execute(sql_query, tuple(params))
        sneakers = cur.fetchall()

        # 総件数の取得
        count_query = """
            SELECT COUNT(*) as total
            FROM sneakers s
            JOIN brands b ON s.brand_id = b.id
            WHERE 1=1
        """
        count_params = []
        if brand_id:
            count_query += " AND s.brand_id = %s"
            count_params.append(brand_id)
        if category:
            count_query += " AND b.category = %s"
            count_params.append(category)

        cur.execute(count_query, tuple(count_params))
        total = cur.fetchone()['total']

        cur.close()
        conn.close()

        return jsonify({
            "sneakers": sneakers,
            "total": total,
            "limit": limit,
            "offset": offset
        })

    except Exception as e:
        print(f"データベースエラー: {e}")
        return jsonify({"error": "データベースエラーが発生しました。"}), 500

# スニーカー詳細取得API
@app.route('/api/sneakers/<int:sneaker_id>')
def get_sneaker_detail(sneaker_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        sql_query = """
            SELECT
                s.*,
                b.name as brand_name,
                b.description as brand_description,
                b.logo_image_url,
                b.category as brand_category
            FROM sneakers s
            JOIN brands b ON s.brand_id = b.id
            WHERE s.id = %s
        """

        cur.execute(sql_query, (sneaker_id,))
        sneaker = cur.fetchone()

        if not sneaker:
            return jsonify({"error": "スニーカーが見つかりません。"}), 404

        # 関連スニーカーの取得
        related_query = """
            SELECT
                s.id,
                s.model_name,
                s.thumbnail_url,
                s.price
            FROM sneakers s
            WHERE s.brand_id = %s AND s.id != %s
            ORDER BY s.release_date DESC
            LIMIT 4
        """

        cur.execute(related_query, (sneaker['brand_id'], sneaker_id))
        related_sneakers = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({
            "sneaker": sneaker,
            "related_sneakers": related_sneakers
        })

    except Exception as e:
        print(f"データベースエラー: {e}")
        return jsonify({"error": "データベースエラーが発生しました。"}), 500

# ブランド一覧取得API
@app.route('/api/brands')
def get_brands():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        category = request.args.get('category')

        sql_query = """
            SELECT
                id,
                name,
                description,
                logo_image_url,
                category,
                established_year,
                headquarters
            FROM brands
            WHERE 1=1
        """
        params = []

        if category:
            sql_query += " AND category = %s"
            params.append(category)

        sql_query += " ORDER BY name ASC"

        cur.execute(sql_query, tuple(params))
        brands = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({"brands": brands})

    except Exception as e:
        print(f"データベースエラー: {e}")
        return jsonify({"error": "データベースエラーが発生しました。"}), 500

# 新着スニーカー取得API
@app.route('/api/sneakers/new')
def get_new_sneakers():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        limit = request.args.get('limit', 8, type=int)

        sql_query = """
            SELECT
                s.id,
                s.model_name,
                s.description,
                s.thumbnail_url,
                s.price,
                s.release_date,
                b.name as brand_name,
                b.logo_image_url
            FROM sneakers s
            JOIN brands b ON s.brand_id = b.id
            ORDER BY s.release_date DESC
            LIMIT %s
        """

        cur.execute(sql_query, (limit,))
        new_sneakers = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({"new_sneakers": new_sneakers})

    except Exception as e:
        print(f"データベースエラー: {e}")
        return jsonify({"error": "データベースエラーが発生しました。"}), 500

if __name__ == '__main__':
    app.run(debug=True)
