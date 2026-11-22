# 👤 دليل المهندسة: روان (Rovan)
**الدور:** Vectorization & Normalization Engineer  
**الفرع المخصص:** `feature/rovan-vectorization`  
**كروت Trello:** IR-07, IR-08, IR-09

---

### 🎯 المهام المطلوبة منك:
1. **`src/vectorization/tfidf.py`:**
   - حساب مصفوفة TF-IDF بالضرب المباشر: $TF\text{-}IDF(t, d) = WTF(t, d) \times IDF(t)$.
2. **`src/vectorization/normalization.py`:**
   - **`calculate_document_lengths(tfidf_matrix, doc_ids)`:**
     - حساب الطول الإقليدي لكل مستند: $|D| = \sqrt{\sum (TF\text{-}IDF)^2}$.
   - **`normalize_tfidf(tfidf_matrix, document_lengths)`:**
     - قسمة وزن كل كلمة على طول المستند.
     - **الحماية من القسمة على صفر:** إذا كان طول المستند $0.0$، اجعل القيمة المعايرة $0.0$.
   - **`vectorize_query(query_terms, idf)`:**
     - حساب تكرارات كلمات الاستعلام، ثم $WTF = 1 + \log_{10}(TF)$، ثم ضربها في $IDF$.
     - تطبيع متجه الاستعلام ليصبح طوله مساوياً لـ $1.0000$.

### 🔍 الاختبار الذهبي:
تحققي من أن كل مستند غير صفري يمتلك طول متجه معاير يساوي **1.0000** بالضبط:
```python
sum_sq = sum(normalized_tfidf[t][doc_id] ** 2 for t in normalized_tfidf)
assert math.isclose(math.sqrt(sum_sq), 1.0, abs_tol=1e-5)
```
