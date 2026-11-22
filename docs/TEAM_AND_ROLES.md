# 👥 توزيع أدوار ومسؤوليات الفريق (Team Matrix)

| العضو | الدور الفني | فرع العمل (Branch) | ملفات الكود المسؤولة |
|---|---|---|---|
| **مصطفى (Mostafa)** | Team Leader & Integration Engineer | `main` / `develop` | `src/main.py`, `src/contracts.py`, `src/output/display.py`, وحوكمة المستودع |
| **منذر (Monzer)** | Data Processing & Indexing Engineer | `feature/monzer-preprocessing-indexing` | `src/preprocessing/document_loader.py`, `tokenizer.py`, `src/indexing/positional_index.py` |
| **إبراهيم (Ebrahim)** | Information Statistics Engineer | `feature/ebrahim-statistics` | `src/statistics/term_statistics.py` |
| **روان (Rovan)** | Vector Space & Normalization Engineer | `feature/rovan-vectorization` | `src/vectorization/tfidf.py`, `src/vectorization/normalization.py` |
| **فيبرونيا (Febronia)** | Retrieval & Ranking Engineer | `feature/febronia-retrieval-ranking` | `src/retrieval/phrase_query.py`, `boolean_query.py`, `src/ranking/similarity.py`, `ranking.py` |

---

## 🧭 ما الذي ينتظره كل عضو ومَن ينتجه؟
* **إبراهيم** ينتظر `positional_index` من **منذر** (يستخدم Mock Data في الساعة الأولى والثانية).
* **روان** تنتظر `weighted_tf` و `idf` من **إبراهيم** (تستخدم Mock Data في الساعة الأولى والثانية).
* **فيبرونيا** تنتظر `positional_index` من **منذر** للبحث اللفظي، وتنتظر `norm_tfidf` من **روان** لحساب درجات التشابه والترتيب.
* **مصطفى** يدمج جميع الوحدات في الساعة الرابعة بالتسلسل الصارم دون أي تعارضات.
