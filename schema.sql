-- データベースの作成（既に存在する場合はスキップ）
-- CREATE DATABASE sneaker_db;

-- 既存のテーブルを削除（存在する場合）
DROP TABLE IF EXISTS sneakers;
DROP TABLE IF EXISTS brands;

-- ブランドテーブルの作成
CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    logo_image_url VARCHAR(255),
    category VARCHAR(50),
    established_year INTEGER,
    headquarters VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- スニーカーテーブルの作成
CREATE TABLE sneakers (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER REFERENCES brands(id),
    model_name VARCHAR(100) NOT NULL,
    description TEXT,
    thumbnail_url VARCHAR(255),
    price INTEGER,
    release_date DATE,
    color VARCHAR(50),
    size_range VARCHAR(50),
    material TEXT,
    features TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- サンプルデータの挿入（ブランド）
INSERT INTO brands (name, description, logo_image_url, category, established_year, headquarters) VALUES
('ブランドA', '伝統と革新を融合させた、日本を代表するスニーカーブランド。職人の技と最新技術が生み出す、最高峰のクオリティ。', '/images/brand-logo-a.png', 'fashion', 1985, '東京都渋谷区'),
('ブランドB', 'ストリートカルチャーから生まれた、若者に支持される革新的なブランド。独自のデザイン哲学で、新しい価値を創造し続ける。', '/images/brand-logo-b.png', 'street', 1995, '東京都原宿'),
('ブランドC', 'サステナビリティを重視した、環境に優しい素材とデザインを追求するブランド。ミニマルで洗練されたスタイルが特徴。', '/images/brand-logo-c.png', 'sustainable', 2005, '東京都代官山');

-- サンプルデータの挿入（スニーカー）
INSERT INTO sneakers (brand_id, model_name, description, thumbnail_url, price, release_date, color, size_range, material, features) VALUES
(1, 'モデルX', '最高峰のクオリティを追求した、ブランドAの代表作。職人の手作業による細部へのこだわりが光る一足。', '/images/sneaker-brand-a-model-x.jpeg', 25000, '2024-01-15', 'ホワイト/ネイビー', '24.0-29.0cm', '本革/メッシュ', ARRAY['クッション性', '通気性', '耐久性']),
(1, 'モデルY', 'クラシカルなデザインに現代的な要素を加えた、新定番モデル。', '/images/sneaker-brand-a-model-y.jpeg', 28000, '2024-02-01', 'ブラック/レッド', '24.0-29.0cm', '本革/スエード', ARRAY['クッション性', 'スタイリッシュ']),
(2, 'ストリートZ', 'ストリートシーンで圧倒的な人気を誇る、ブランドBの看板モデル。', '/images/sneaker-brand-b-model-z.jpeg', 22000, '2024-01-20', 'グレー/オレンジ', '24.0-29.0cm', '合成皮革/メッシュ', ARRAY['軽量性', 'フィット感']),
(2, 'アーバンW', '都会的なライフスタイルに合わせた、洗練されたデザイン。', '/images/sneaker-brand-b-model-w.jpeg', 24000, '2024-02-10', 'ネイビー/ホワイト', '24.0-29.0cm', '本革/メッシュ', ARRAY['クッション性', 'スタイリッシュ']),
(3, 'エコV', '環境に配慮した素材を使用した、サステナブルなスニーカー。', '/images/sneaker-brand-c-model-v.jpeg', 26000, '2024-01-25', 'ベージュ/グリーン', '24.0-29.0cm', 'リサイクル素材', ARRAY['エコフレンドリー', '軽量性']),
(3, 'ミニマルU', '必要最小限のデザインで、最大の快適性を実現。', '/images/sneaker-brand-c-model-u.jpeg', 23000, '2024-02-15', 'ホワイト/ブラック', '24.0-29.0cm', '合成素材', ARRAY['ミニマルデザイン', 'フィット感']);

-- インデックスの作成
CREATE INDEX idx_sneakers_brand_id ON sneakers(brand_id);
CREATE INDEX idx_sneakers_release_date ON sneakers(release_date);
CREATE INDEX idx_brands_category ON brands(category);
