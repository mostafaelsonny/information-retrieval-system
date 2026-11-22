# 👤 دليل المهندس: منذر (Monzer)
**الدور:** Data Processing & PySpark Indexing Engineer  
**الفرع المخصص:** `feature/monzer-preprocessing-indexing`  
**كروت Trello:** IR-03, IR-04

---

### 🎯 المهام المطلوبة منك:
1. **`src/preprocessing/document_loader.py`:**
   - قراءة الـ 10 ملفات النصية من مجلد `data/` (`d1.txt` إلى `d10.txt`).
   - تنظيف النصوص: تحويلها إلى lowercase، إزالة الرموز وعلامات الترقيم، والإبقاء على المسافات.
   - **قاعدة صارمة:** لا تقم بإزالة الـ Stop Words ولا تقم بالـ Stemming!
2. **`src/preprocessing/tokenizer.py`:**
   - تقطيع النص إلى كلمات وحساب موقع كل كلمة بدءاً من **1** (1-based position).
   - إخراج قائمة من الـ Tuples: `[("customer", 1), ("service", 2), ...]`.
3. **`src/indexing/positional_index.py` (PySpark):**
   - تهيئة `SparkSession.builder.master("local[2]").appName("PositionalIndex").getOrCreate()`.
   - استخدام RDDs أو DataFrames لتقسيم الكلمات والمواقع وتجميعها.
   - إخراج قاموس بايثون يطابق العقد: `dict[str, dict[str, list[int]]]`.

### 🧪 كيف تختبر كودك قبل فتح PR؟
```bash
pytest tests/test_loader.py tests/test_tokenizer.py tests/test_indexing.py
```
تأكد أن:
- `pos_index["customer"]["d1"] == [1]`
- `pos_index["service"]["d1"] == [2]`
- المواقع كلها أعداد صحيحة $\ge 1$.
