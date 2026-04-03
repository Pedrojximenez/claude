# GraphRAG実装評価メモ
## Angels Phase 6後半〜7初期 技術選定

**作成日**: 2026-04-03  
**対象フェーズ**: Phase 6後半〜Phase 7初期  
**評価者**: レザード（[gods]メール報告）

---

## 1. LightRAG 技術概要

### 1.1 概要

**HKUDS/LightRAG** (GitHub 14K+ stars, 論文: arXiv:2410.05779)

LightRAGは香港大学が開発したGraph+VectorハイブリッドRAGフレームワーク。  
Microsoft GraphRAGの「高コスト・高精度」に対し、**「低コスト・高速・十分な精度」**を実現するアーキテクチャ。

---

### 1.2 Dual-Level Retrieval（二層検索）

```
ドキュメント
    │
    ▼
[チャンク分割] ── 1200トークン/チャンク
    │
    ▼
[LLMによるエンティティ抽出] ── entities + relationships + keywords
    │
    ├──► [低レベル（Low-Level）検索]
    │        └─ 具体的エンティティ・固有名詞・事実
    │             例: "〇〇キャラの属性", "特定イベントの詳細"
    │
    └──► [高レベル（High-Level）検索]
             └─ テーマ・概念・広域的トピック
                  例: "Angels全体の世界観", "Phase間の大きな流れ"
```

| レイヤー | 対象 | 用途 |
|---------|------|------|
| Low-Level | 具体的エンティティ、固有名詞 | ピンポイント質問への回答 |
| High-Level | テーマ、キーワード、概念 | 俯瞰的・分析的回答 |
| Hybrid | 両者の組み合わせ | バランス重視の汎用クエリ |
| Naive | ベクトル検索のみ（グラフ不使用） | 低コスト・シンプルな検索 |

---

### 1.3 インクリメンタル更新メカニズム

**LightRAGの最大の実用優位性はここにある。**

```python
# 新規ドキュメント追加 ── 既存グラフの再構築は不要
rag.insert("新しいドキュメントテキスト")

# 内部処理フロー
1. 新規ドキュメントのみチャンク化
2. LLMで新規エンティティ・関係を抽出
3. 重複検出: 既存エンティティと照合
4. マージ: fragments > 6 の場合LLMで要約統合
5. グラフ・ベクトルDBに差分追加
```

**重複除去ロジック**:
- エンティティ名の正規化 + ベクトル類似度でマッチング
- デフォルト閾値6以上のフラグメントが存在する場合、LLMで統合要約
- 既存ノード/エッジへの属性マージ（上書きではなく蓄積）

Microsoft GraphRAGは**全文書の再インデックスが必要**なのに対し、LightRAGは**差分更新が可能**。

---

### 1.4 対応バックエンド

#### グラフストレージ

| バックエンド | 状態 | 用途 |
|------------|------|------|
| NetworkX | 標準（デフォルト） | 開発・小規模（メモリ内） |
| **Neo4j** | 公式サポート | 本番向け高性能グラフDB |
| ArangoDB | サポート | マルチモデルDB |
| TigerGraph | サポート | 大規模分散グラフ |
| Apache AGE | サポート | PostgreSQL拡張グラフ |

#### ベクトルストレージ

| バックエンド | 状態 | 用途 |
|------------|------|------|
| NanoVectorDB | 標準（デフォルト） | 軽量・開発用 |
| **pgvector** | 公式サポート | PostgreSQL拡張（★Angels環境に適合） |
| Milvus | サポート | 大規模ベクトル検索 |
| Qdrant | サポート | 高速ベクトルDB |
| Chroma | サポート | 軽量OSS |
| Weaviate | サポート | マルチモーダル対応 |
| Redis | サポート | インメモリ高速 |

#### KVストレージ（キャッシュ/メタデータ）

| バックエンド | 状態 |
|------------|------|
| JsonKVStorage | デフォルト（ファイルベース） |
| PGKVStorage | PostgreSQL |
| RedisKVStorage | Redis |
| MongoKVStorage | MongoDB |

**→ pgvector単体でVector+KV両方をカバー可能。Angels既存Docker環境と直接接続可。**

---

### 1.5 Ollama / ローカルLLMでのエンティティ抽出

```python
from lightrag import LightRAG
from lightrag.llm.ollama import ollama_model_complete, ollama_embed

rag = LightRAG(
    working_dir="./rag_storage",
    llm_model_func=ollama_model_complete,
    llm_model_name="qwen2.5:32b",          # 推奨: 32B以上
    llm_model_kwargs={
        "host": "http://localhost:11434",
        "options": {"num_ctx": 32768}       # 推奨: 32K以上
    },
    embedding_func=ollama_embed,
    embedding_model_name="nomic-embed-text",
    embedding_dim=768,
)
```

**Ollamaサポート状況**:
- エンティティ抽出: ✅ 動作確認済み
- エンベディング: ✅ nomic-embed-text, mxbai-embed-large等
- 推奨モデル: `qwen2.5:32b` または `llama3.1:70b`（最低32B推奨）
- コンテキスト長: 最低32K、推奨64K

---

## 2. Microsoft GraphRAG との比較表

### 2.1 機能・性能比較

| 評価軸 | LightRAG | Microsoft GraphRAG |
|-------|---------|-------------------|
| **アーキテクチャ** | Graph + Vector ハイブリッド | 純粋グラフ + コミュニティ階層 |
| **インデックス方式** | チャンク単位 + エンティティ抽出 | コミュニティ検出（Leiden法） |
| **検索モード** | Low/High/Hybrid/Naive | Local Search / Global Search |
| **Community Summary** | ❌ なし | ✅ 階層的コミュニティ要約あり |
| **インクリメンタル更新** | ✅ 完全対応（差分追加） | ❌ 要再インデックス（一部改善中） |
| **ローカルLLM対応** | ✅ Ollama完全対応 | △ 設定複雑・要カスタマイズ |
| **セットアップ難易度** | 低（pip install lightrag-hku） | 高（複数コンポーネント） |

### 2.2 インデックスコスト比較

```
同規模ドキュメント（例: 1000チャンク）でのAPI呼び出し概算

LightRAG:
  - エンティティ抽出: 1000回 × チャンク
  - マージ/要約: 条件次第（少数）
  → 推定コスト: $2〜5（GPT-4o-mini基準）
  → クエリ時トークン消費: ~100トークン/クエリ

Microsoft GraphRAG（標準）:
  - エンティティ抽出: 1000回
  - コミュニティ要約: 階層ごとに数百〜数千回
  - グローバルサーチ時: map-reduceで追加呼び出し
  → 推定コスト: $20〜100（同基準）
  → クエリ時トークン消費: ~610,000トークン/クエリ（グローバル検索時）

Microsoft LazyGraphRAG（コスト最適化版、2024年リリース）:
  - インデックスコスト: 標準GraphRAGの0.1%（コミュニティ要約を事前生成しない）
  - クエリコスト: 標準の1/700
  - 品質: グローバルクエリでGraphRAGと同等
  → Angels規模ならLazyGraphRAGも選択肢に入るが、pgvector非対応は変わらない

※ローカルLLM使用時は両者ともAPIコスト≒$0
  ただしGPU/時間コストはLightRAGが大幅に少ない（コミュニティ要約不要のため）
```

### 2.3 クエリ品質（ベンチマーク）

LightRAGの原論文（arXiv:2410.05779）での評価:

| 評価指標 | LightRAG | NaiveRAG | GraphRAG |
|---------|---------|---------|---------|
| **Comprehensiveness（網羅性）** | 38.36% win | 比較基準 | 24.65% win |
| **Diversity（多様性）** | 32.12% win | 比較基準 | 18.09% win |
| **Empowerment（実用性）** | 24.89% win | 比較基準 | 17.80% win |
| **Overall** | **LightRAG優位** | - | LightRAGと拮抗〜優位 |

※Win率 = LightRAGが相手より優れていた比率（GPT-4o評価）

### 2.4 Angels環境向け詳細比較

| 観点 | LightRAG | Microsoft GraphRAG | 判定 |
|-----|---------|-------------------|------|
| **更新容易性** | ✅ append-only差分マージ | △ v1.0で改善、ただしコミュニティ再要約あり | LightRAG |
| **ローカル動作** | ✅ Ollama完全対応 | △ 要設定 | LightRAG |
| **pgvector接続** | ✅ 公式サポート | ❌ 非対応 | LightRAG |
| **クエリトークン消費** | ✅ ~100トークン/クエリ | ❌ ~610,000トークン/クエリ（標準） | LightRAG |
| **Community Summary** | ❌ なし | ✅ 強力（LazyGraphRAGでは遅延生成） | GraphRAG |
| **大規模文書への適性** | ○ 中〜大規模 | ◎ 超大規模 | GraphRAG |
| **小〜中規模知識ベース** | ◎ 最適 | △ オーバースペック | LightRAG |
| **実装コスト** | ✅ 低 | ❌ 高 | LightRAG |

---

## 3. gods/Angels環境への適合性評価

### 3.1 gods_shared（YAML tagged .md files）との相性

**gods_sharedのファイル構造（想定）**:
```yaml
---
tags: [angels, phase6, character, レザード]
date: 2026-04-03
---
# キャラクター情報 ...
```

**LightRAGとの相性評価**: ★★★★☆

```
✅ 適合ポイント:
- テキストベースのMarkdownファイルを直接ingest可能
- YAMLフロントマターはチャンク処理時に自然に含まれる
- タグ情報がエンティティとして自動抽出される可能性
- ファイル単位のインクリメンタル更新と相性が良い

⚠️ 注意点:
- YAMLフロントマターの構造的意味はLLMが解釈
- タグの明示的なインデックス化には前処理推奨
- ファイル変更検知は別途実装が必要

推奨前処理:
  1. YAMLフロントマターを解析してメタデータ抽出
  2. タグをエンティティとして明示的にテキストに埋め込み
  3. ファイル変更時にrag.insert()で差分更新
```

### 3.2 pgvector（既存Docker）との接続

**接続設定例**:
```python
from lightrag import LightRAG
from lightrag.kg.postgres_impl import PostgreSQLDB

# 既存pgvector Dockerに接続
POSTGRES_CONFIG = {
    "host": "localhost",      # または Docker network内のホスト名
    "port": 5432,
    "user": "postgres",
    "password": "password",
    "database": "angels_rag",
}

rag = LightRAG(
    working_dir="./lightrag_storage",
    kv_storage="PGKVStorage",
    vector_storage="PGVectorStorage",
    graph_storage="NetworkXStorage",   # または Neo4jStorage
    addon_params={"storage_params": POSTGRES_CONFIG}
)
```

**適合性**: ★★★★★

```
✅ 完全対応:
- PGVectorStorage: 公式実装済み
- PGKVStorage: 公式実装済み
- pgvector拡張が有効なPostgreSQLで動作
- 既存Dockerに新規DB作成のみで接続可

必要条件:
  - PostgreSQL 14+
  - pgvector拡張インストール済み（既存環境なら対応済み想定）
  - lightrag-hku[postgres] のインストール
```

### 3.3 Ollama/ローカルLLMでのエンティティ抽出

**適合性**: ★★★★☆

```
✅ 動作確認済みモデル（Ollama）:
- qwen2.5:32b     ← 推奨（中国語・日本語エンティティ抽出が優秀）
- llama3.1:70b    ← 英語テキスト向け
- qwen2.5:14b     ← 軽量オプション（品質は32B比で低下）
- mistral-nemo    ← 実験的

⚠️ 日本語テキスト（gods_shared）への注意:
- qwen2.5:32bは日本語エンティティ抽出に最も適している
- プロンプトを日本語化するカスタマイズが品質向上に有効
- エンティティ名の正規化（漢字・カナの表記揺れ）に注意

GPU要件（32Bモデル）:
- VRAM: 24GB以上推奨（Q4量子化で約20GB）
- または RTX 3090/4090 × 1枚
```

---

## 4. 推奨評価: 採用候補比較

### 4.1 候補一覧

| システム | 主な特徴 | Angels適合度 |
|---------|---------|------------|
| **LightRAG** | Graph+Vector, 差分更新, pgvector対応 | ★★★★★ |
| **Microsoft GraphRAG** | コミュニティ要約, 大規模向け, 高コスト | ★★★☆☆ |
| **Graphiti (Zep AI)** | エピソード記憶, 時系列グラフ, Agent向け | ★★★☆☆ |
| **Mem0** | 個人記憶層, シンプルAPI, スケール限定 | ★★☆☆☆ |

### 4.2 Graphiti 評価

```
特徴:
- エピソード的記憶（時系列イベントのグラフ化）
- Bi-temporal tracking（知識の有効期間管理）
- Agent向け設計（会話履歴から自動的に知識グラフ構築）

Angels適合性:
✅ フェーズ進行に伴うキャラクター状態変化の追跡に有効
✅ "いつ何が変わったか"の時系列管理
❌ 静的ドキュメント（gods_shared .md）の一括インデックスには不向き
❌ pgvector非対応（Neo4j必須）

結論: サブシステムとして将来検討。メインRAGには採用しない。
```

### 4.3 Mem0 評価

```
特徴:
- 会話・ユーザー記憶に特化したシンプルAPI（GitHub 41K+ stars）
- managed serviceあり（mem0.ai）
- ベクトル+グラフ+キーバリューの三層構造
- AWS Agent SDKの公式メモリプロバイダー（2025年）
- Q3 2025: 1.86億APIコール（Q1比5.3倍成長）

Angels適合性:
✅ AIキャラクターの「記憶」機能として将来活用の余地
❌ 知識ベース構築（RAG）用途には設計が合わない
❌ 大量ドキュメントのインデックスには不向き
❌ 時系列追跡なし（Graphitiと異なり事実を上書き）
❌ 競合する事実の解決はLLM依存で精度が不安定

結論: Phase 8以降のキャラクター記憶機能で別途検討。今回は対象外。
```

---

## 5. 最終推奨

### 推奨: **LightRAG** を採用

```
推奨理由（優先順位順）:

1. pgvector既存環境に直接接続可能
   → 新規インフラ不要、移行コスト最小

2. インクリメンタル更新による運用コスト削減
   → gods_sharedのYAML .mdファイルを随時追加可能
   → Phase進行に伴う知識ベース拡張が容易

3. Ollamaによる完全ローカル動作
   → API費用ゼロ、プライバシー保護
   → qwen2.5:32bで日本語エンティティ抽出に対応

4. dual-level retrieval
   → キャラクター固有情報（Low-Level）と世界観・テーマ（High-Level）
     の両方に対応し、Angels特有の多層的クエリに適応

5. 実装・運用コストが最も低い
   → Microsoft GraphRAGの1/10以下のインデックスコスト
   → セットアップ工数が最小
```

### 実装見積もり

#### Phase 6後半（基盤構築）

| タスク | 工数 | 優先度 |
|-------|------|-------|
| LightRAG + pgvector接続確認 | 0.5日 | 高 |
| gods_sharedファイル前処理スクリプト作成 | 1日 | 高 |
| Ollamaモデル選定・エンティティ抽出テスト | 1日 | 高 |
| 初期インデックス構築（既存.mdファイル） | 0.5日 | 高 |
| 検索品質評価（代表クエリ10件） | 0.5日 | 中 |
| **Phase 6後半 合計** | **3.5日** | |

#### Phase 7初期（統合・運用）

| タスク | 工数 | 優先度 |
|-------|------|-------|
| Angels APIへの組み込み | 2日 | 高 |
| 差分更新パイプライン構築 | 1日 | 高 |
| 日本語エンティティ抽出チューニング | 1.5日 | 中 |
| キャッシュ・パフォーマンス最適化 | 1日 | 中 |
| モニタリング・ログ整備 | 0.5日 | 低 |
| **Phase 7初期 合計** | **6日** | |

**総工数見積もり: 約9〜10日**

---

## 6. 技術スタック構成（推奨）

```
[Angels アプリ層]
       │
       ▼
[LightRAG API]
  ├── LLM: Ollama (qwen2.5:32b)
  ├── Embedding: Ollama (nomic-embed-text)
  ├── Graph: NetworkX (→ 将来 Neo4j へ移行可)
  └── Vector + KV: pgvector (既存Docker)
       │
       ▼
[PostgreSQL + pgvector]
  ├── vector_chunks テーブル
  ├── vector_entities テーブル
  ├── vector_relationships テーブル
  └── kv_store テーブル
```

---

## 7. リスクと緩和策

| リスク | 影響度 | 緩和策 |
|-------|-------|-------|
| qwen2.5:32bのVRAM不足 | 高 | Q4量子化使用 / 14Bモデルへのフォールバック |
| 日本語エンティティ抽出精度 | 中 | プロンプトの日本語化 / 抽出結果の人手検証 |
| グラフの肥大化（Phase進行で増加） | 中 | 定期的なエンティティマージ / 不要データ削除 |
| pgvector接続設定の複雑化 | 低 | 公式実装ドキュメントに沿った設定で解決可 |
| Community Summary の欠如 | 低 | High-Level検索で代替。不足時はGraphRAG併用検討 |

---

## 参考リンク

- [HKUDS/LightRAG GitHub](https://github.com/HKUDS/LightRAG)
- [LightRAG 原論文 (arXiv:2410.05779)](https://arxiv.org/abs/2410.05779)
- [LightRAG 公式ドキュメント](https://lightrag.github.io/)
- [Microsoft GraphRAG GitHub](https://github.com/microsoft/graphrag)
- [LazyGraphRAG — Microsoft Research Blog](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/)
- [Graphiti (Zep AI) GitHub](https://github.com/getzep/graphiti)
- [Mem0 GitHub](https://github.com/mem0ai/mem0)
- [pgvector GitHub](https://github.com/pgvector/pgvector)

---

*本ドキュメントはAngels Phase 6後半〜7初期のGraphRAG実装判断のための技術評価メモです。*  
*最終実装決定前に、実環境でのPoC（概念実証）を推奨します。*
