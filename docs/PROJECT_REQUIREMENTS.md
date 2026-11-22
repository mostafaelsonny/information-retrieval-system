# 📋 متطلبات المشروع والمخرجات المتوقعة (Project Requirements)

> ملخص متطلبات مقرر استرجاع وتخزين المعلومات (Fall 2026) لمجموعة بيانات الأعمال (Business Dataset - 10 Docs).

---

## 🗂️ Part A: Indexing & Term Weighting Matrix
1. **Document Loading & Preprocessing:**
   - قراءة النصوص العشرة وتوحيد الحروف الصغيرة وتنظيف الرموز.
   - منع الـ Stop Words Removal ومنع الـ Stemming.
2. **Positional Inverted Index (PySpark):**
   - بناء فهرس موضعي برقم الموقع لكل كلمة في كل مستند (1-based position).
3. **Term Statistics:**
   - Raw TF: تكرار الكلمات في كل مستند.
   - Weighted TF ($WTF$): $1 + \log_{10}(TF)$ عندما $TF > 0$ وإلا $0.0$.
   - Document Frequency ($DF$): عدد المستندات المحتوية على الكلمة.
   - Inverse Document Frequency ($IDF$): $\log_{10}(10 / DF)$.
4. **TF-IDF & Euclidean Length Normalization:**
   - $TF\text{-}IDF = WTF \times IDF$.
   - طول المستند: $|D| = \sqrt{\sum (TF\text{-}IDF)^2}$.
   - التطبيع: قسمة الأوزان على طول المستند لجعل طول المتجه $1.0000$.

---

## 🔍 Part B: Retrieval, Matching & Ranking
1. **Phrase Query Execution:**
   - الاستعلام 1: `"customer service"` (المتطابق: `d1, d2, d5, d10`).
   - الاستعلام 2: `"sales growth"` (المتطابق: `d3, d5, d7, d8`).
2. **Boolean Query Execution:**
   - الاستعلام 3: `"customer service" AND "sales growth"` (المتطابق: `d5`).
   - الاستعلام 4: `"customer service" AND NOT "sales growth"` (المتطابق: `d1, d2, d10`).
3. **Vector Space Model Querying & Cosine Ranking:**
   - بناء متجهات الاستعلام وتطبيعها.
   - حساب تشابه جيب التمام: $Sim(Q, D) = Q \cdot D$.
   - ترتيب المستندات تنازلياً لكل استعلام من الاستعلامات الأربعة.

---

## 📝 Part C: Conceptual Questions & Documentation
1. ما الذي توفره الفهارس الموضعية وتعجز عنه الفهارس غير الموضعية؟
2. العلاقة العكسية بين تردد المستند (DF) والوزن التمييزي (IDF).
3. تأثير تكرار الكلمات (TF) على ترتيب المستندات ولماذا نستخدم التخميد اللوغاريتمي.
4. دور TF-IDF وأهمية تطبيع الأطوال $L_2$ في حماية النظام من انحياز المستندات الطويلة.
5. كيف يحول تشابه جيب التمام الزاوية بين المتجهات إلى درجة ترتيب دلالي دقيقة.
6. الفرق في التنفيذ الرياضي والموقعي بين استعلام AND واستعلام AND NOT.
