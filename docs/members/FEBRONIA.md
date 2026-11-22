# 👤 دليل المهندسة: فيبرونيا (Febronia)
**الدور:** Retrieval & Ranking Engineer  
**الفرع المخصص:** `feature/febronia-retrieval-ranking`  
**كروت Trello:** IR-10, IR-11, IR-12

---

### 🎯 المهام المطلوبة منك:
1. **`src/retrieval/phrase_query.py`:**
   - البحث عن العبارة الدقيقة عبر فحص تتابع المواقع:
     - إذا كانت العبارة كلمة واحدة: إرجاع كل المستندات التي ظهرت فيها.
     - إذا كانت كلمتين: التأكد من وجود موقع في الكلمة الثانية يساوي موقع الكلمة الأولى زائد 1 ($pos_2 = pos_1 + 1$).
2. **`src/retrieval/boolean_query.py`:**
   - `execute_boolean_query(docs_p1, docs_p2, operator)`:
     - `AND`: إرجاع تقاطع المستندات (المستندات المشتركة فقط: `set(docs_p1) & set(docs_p2)`).
     - `AND NOT`: إرجاع المستندات الموجودة في القائمة الأولى وغير موجودة في الثانية (`set(docs_p1) - set(docs_p2)`).
3. **`src/ranking/similarity.py`:**
   - حساب تشابه جيب التمام كحاصل الضرب النقطي (Dot Product) بين متجه الاستعلام المعاير ومتجه المستند المعاير:
     $$Sim(Q, D) = \sum_{t \in Q} (W_{t, Q} \times W_{t, D})$$
4. **`src/ranking/ranking.py`:**
   - فرز المستندات تنازلياً حسب درجة التشابه.

### 🎯 مطابقة الـ Ground Truth:
- `"customer service"` يجب أن ترجع: `d1, d2, d5, d10` والمستند المتصدر هو `d1`.
- `"sales growth"` يجب أن ترجع: `d3, d5, d7, d8`.
- `AND` يرجع: `d5` فقط.
- `AND NOT` يرجع: `d1, d2, d10` (استبعاد d5).
- **قاعدة هامة في AND NOT:** متجه الاستعلام يُبنى من كلمات العبارة الأولى فقط!
