# 📜 وثيقة عقود البيانات الموحدة (Unified Data Contracts)

> **الحالة:** معتمدة ومقفلة رسمياً (Approved & Locked)  
> **الملف البرمجي المنفذ:** `src/contracts.py`

عقود البيانات هي الاتفاق الهندسي الصارم الذي يحدد أسماء الحقول ومفاتيح الـ Dictionaries وأنواعها الرياضية والبرمجية بين من ينتج البيانات ومن يستهلكها.

---

### 1. Documents Contract (منذر → الجميع)
```python
documents: dict[str, str] = {
    "d1": "customer service",
    "d2": "customer service improves customer satisfaction",
    "d3": "sales growth strategy improves revenue",
    "d4": "customer relationship management drives sales",
    "d5": "customer service accelerates sales growth",
    "d6": "market expansion strategy drives revenue",
    "d7": "sales growth requires market research",
    "d8": "customer retention increases sales growth",
    "d9": "innovative marketing strategy improves satisfaction",
    "d10": "customer service excellence builds trust"
}
```

---

### 2. Positional Inverted Index Contract (منذر → إبراهيم، فيبرونيا، مصطفى)
* **القاعدة:** الترقيم الموقعي داخل قائمة المستند يبدأ من **1** (1-based position) ومواقع الكلمات مرتبة تصاعدياً.
```python
positional_index: dict[str, dict[str, list[int]]] = {
    "customer": {
        "d1": [1],
        "d2": [1, 4],
        "d4": [1],
        "d5": [1, 6],
        "d8": [1],
        "d10": [1, 4]
    },
    "service": {
        "d1": [2],
        "d2": [2],
        "d5": [2, 7],
        "d10": [2]
    }
}
```

---

### 3. Term Statistics Contracts (إبراهيم → روان، مصطفى)
* **Raw TF:** عدد التكرارات في كل مستند.
* **Weighted TF ($WTF$):** $1 + \log_{10}(TF)$ عندما $TF > 0$ وإلا $0.0$.
* **Document Frequency ($DF$):** عدد المستندات الفريدة التي ظهرت فيها الكلمة.
* **Inverse Document Frequency ($IDF$):** $\log_{10}(10 / DF)$ لقاعدة بيانات من 10 مستندات.

```python
raw_tf: dict[str, dict[str, int]] = {
    "customer": {"d1": 1, "d2": 2, "d4": 1, "d5": 2, "d8": 1, "d10": 2}
}

weighted_tf: dict[str, dict[str, float]] = {
    "customer": {"d1": 1.0000, "d2": 1.3010, "d4": 1.0000, "d5": 1.3010, "d8": 1.0000, "d10": 1.3010}
}

df: dict[str, int] = {
    "customer": 6,
    "service": 4,
    "sales": 4,
    "growth": 4
}

idf: dict[str, float] = {
    "customer": 0.2218,  # log10(10 / 6)
    "service": 0.3979,   # log10(10 / 4)
    "sales": 0.3979,     # log10(10 / 4)
    "growth": 0.3979     # log10(10 / 4)
}
```

---

### 4. TF-IDF & Normalization Contracts (روان → فيبرونيا، مصطفى)
* $TF\text{-}IDF = WTF \times IDF$.
* طول المستند: $|D| = \sqrt{\sum (TF\text{-}IDF)^2}$.
* التطبيع: $Normalized = TF\text{-}IDF / |D|$.
* **معيار الجودة:** طول كل متجه مستند معيار يساوي **1.0000** بالضبط ($\pm 10^{-6}$).

```python
tfidf_matrix: dict[str, dict[str, float]] = {
    "customer": {"d1": 0.2218, "d2": 0.2886}
}

document_lengths: dict[str, float] = {
    "d1": 0.4556,
    "d2": 0.6842
}

normalized_tfidf: dict[str, dict[str, float]] = {
    "customer": {"d1": 0.4868, "d2": 0.4218}
}

# متجه الاستعلام المعاير بطول 1.0:
query_vector: dict[str, float] = {
    "customer": 0.4868,
    "service": 0.8735
}
```

---

### 5. Retrieval & Ranking Contracts (فيبرونيا → مصطفى)
```python
# نتائج البحث اللفظي:
phrase_results: dict[str, dict[str, list[int]]] = {
    "customer service": {
        "d1": [1],
        "d2": [1],
        "d5": [1, 6],
        "d10": [1]
    }
}

# نتائج العمليات البوليانية:
boolean_results: dict[str, list[str]] = {
    "customer service AND sales growth": ["d5"],
    "customer service AND NOT sales growth": ["d1", "d2", "d10"]
}

# نتائج درجات تشابه جيب التمام والترتيب:
similarity_scores: dict[str, dict[str, float]] = {
    "customer service": {
        "d1": 1.0000,
        "d2": 0.6147,
        "d5": 0.4159,
        "d10": 0.2875
    }
}

ranked_results: dict[str, list[tuple[str, float]]] = {
    "customer service": [
        ("d1", 1.0000),
        ("d2", 0.6147),
        ("d5", 0.4159),
        ("d10", 0.2875)
    ]
}
```
