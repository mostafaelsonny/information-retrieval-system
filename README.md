# 🔍 Information Storage & Retrieval (IR) System

نظام متكامل لتخزين واسترجاع المعلومات مبني باستخدام **PySpark** و **Vector Space Model (VSM)**، ومصمم لمعالجة نصوص قطاع الأعمال (Business Corpus - 10 Documents) واسترجاعها بدقة فائقة عبر **Phrase Queries** و **Boolean Queries** وترتيبها باستخدام **Cosine Similarity Ranking**.

> ⏱️ **زمن الإنجاز:** سبرنت مكثف لمدة **6 ساعات** (6-Hour Sprint).  
> 👥 **فريق العمل:** 5 مهندسين بتطوير متوازي وتكامل تسلسلي مركزي بقيادة مصطفى (@mostafaelsonny).  
> 📋 **لوحة متابعة المهام:** [Trello Board — IR 6-Hour Sprint](https://trello.com/b/6b0233e1cccc215d1c4831a8)  
> 📚 **الإجابات المفاهيمية (Part C):** [docs/CONCEPTUAL_QUESTIONS.md](docs/CONCEPTUAL_QUESTIONS.md)

---

## 👋 عضو جديد في الفريق؟ ابدأ من هنا!
إذا كنت تنضم للمشروع لأول مرة، اتبع هذا المسار المباشر لتبدأ فوراً بدون أي ارتباك:
1. **[docs/START_HERE.md](docs/START_HERE.md):** مدخل مبسط يشرح ما هو نظام الـ IR، والمشكلة التي نحلها، وكيف ترتبط القطع ببعضها.
2. **[docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md):** دليلك لإنشاء Branch، وتحديث كودك، وتشغيل الاختبارات، وفتح Pull Request احترافي.
3. **[docs/DATA_CONTRACTS.md](docs/DATA_CONTRACTS.md):** عقود البيانات الرسمية الصارمة (Single Source of Truth) — اقرأها قبل كتابة سطر كود واحد!
4. **[docs/CONCEPTUAL_QUESTIONS.md](docs/CONCEPTUAL_QUESTIONS.md):** التوثيق النظري والمفاهيمي لجميع الأسئلة الستة المعتمدة في المقرر.
5. **دليلك الشخصي وفقاً لدورك في الفريق:**
   - [Monzer (Data Processing & PySpark)](docs/members/MONZER.md)
   - [Ebrahim (Information Statistics)](docs/members/EBRAHIM.md)
   - [Rovan (Vector Space & Normalization)](docs/members/ROVAN.md)
   - [Febronia (Retrieval & Ranking)](docs/members/FEBRONIA.md)
   - [Mostafa (Team Leader & Integration)](docs/members/MOSTAFA.md)
6. **كارت مهمتك على Trello:** يحتوي على الوصف الدقيق، والمدخلات والمخرجات، ومعايير القبول (Acceptance Criteria).

---

## 💡 فكرة المشروع ببساطة (Zero-Knowledge Guide)
نظام استرجاع وتخزين المعلومات (IR) مثل محرك بحث مصغر:
1. **قراءة النصوص (Document Ingestion):** نقرأ 10 مستندات نصية في مجال الأعمال، ونحول كلماتها إلى حروف صغيرة ونزيل علامات الترقيم **دون حذف الكلمات الشائعة (No Stop Words) ودون اشتقاق (No Stemming)** وفقاً لمعايير المقرر.
2. **الفهرس الموقعي (Positional Index via PySpark):** نبني فهرساً موزعاً لا يسجل فقط وجود الكلمة في المستند، بل يسجل **رقم موقع الكلمة داخل المستند (1-based index)**. هذا الفهرس الموقعي هو السر الذي يُمكّننا من البحث عن عبارات دقيقة متتالية مثل `"customer service"`.
3. **إحصائيات الكلمات (Term Statistics):**
   - **Raw TF:** كم مرة تكررت الكلمة في المستند؟
   - **Weighted TF ($WTF$):** تخميد التكرار لوغاريتمياً ($1 + \log_{10}(TF)$) حتى لا تطغى كلمة متكررة عشوائياً.
   - **Document Frequency ($DF$):** في كم مستند ظهرت الكلمة؟
   - **Inverse Document Frequency ($IDF$):** وزن ندرة الكلمة ($\log_{10}(10/DF)$). الكلمات النادرة تأخذ وزناً تمييزياً أعلى.
4. **الفضاء المتجهي ومصفوفة TF-IDF:**
   - وزن الكلمة في المستند: $TF\text{-}IDF = WTF \times IDF$.
   - **تطبيع الطول الإقليدي ($L_2$ Normalization):** جعل طول متجه كل مستند مساوياً بالضبط لـ $1.0000$ لضمان العدالة وعدم تحيز النظام للمستندات الطويلة.
5. **محرك الاسترجاع والترتيب (Retrieval & Ranking):**
   - **Phrase Search:** التأكد من تتابع الكلمات وراء بعضها بفارق موقعي $+1$.
   - **Boolean Logic:** تقاطع القوائم لـ `AND` ($A \cap B$)، والفرق والاستبعاد لـ `AND NOT` ($A - B$).
   - **Cosine Similarity:** حساب حاصل الضرب النقطي (Dot Product) بين متجه الاستعلام ومتجهات المستندات المطابقة، وترتيب المستندات تنازلياً من الأكثر تطابقاً إلى الأقل.

---

## 🛠️ التقنيات المستخدمة (Tech Stack)

| المكون | التقنية المعتمدة | الاستخدام |
|---|---|---|
| **اللغة الأساسية** | Python 3.11 / 3.12 | لغة المعالجة والتنفيذ |
| **المعالجة الموزعة** | Apache Spark (PySpark 3.4+) | بناء الفهرس الموقعي الضخم بشكل متوازي |
| **الحسابات الرياضية** | NumPy / Math | مصفوفات TF-IDF وحسابات معيار $L_2$ |
| **الاختبارات وضمان الجودة** | Pytest 7.4+ | اختبارات المطابقة الصارمة وعقود البيانات |
| **التنسيق والعرض** | Built-in Formatter | إخراج الجداول وحفظ تقارير Part A و Part B |
| **إدارة المشروع والنسخ** | Git, GitHub, Trello | حوكمة الكود، والـ Rulesets، وتتبع المهام |

---

## 🏗️ البنية المعمارية للمستودع (Repository Structure)

```text
information-retrieval-system/
├── data/                       # مستندات الأعمال العشرة (d1.txt إلى d10.txt)
├── src/                        # الكود المصدري للمشروع
│   ├── preprocessing/          # قراءة الملفات وتقطيع الكلمات مع المواقع
│   │   ├── document_loader.py  # Member 2: قراءة المستندات
│   │   └── tokenizer.py        # Member 2: تقطيع الكلمات وترقيمها (1-based)
│   ├── indexing/               # بناء الفهرس عبر PySpark
│   │   └── positional_index.py # Member 2: PySpark Positional Inverted Index
│   ├── statistics/             # حسابات إحصائيات الكلمات
│   │   └── term_statistics.py  # Member 3: Raw TF, WTF, DF, IDF
│   ├── vectorization/          # نموذج الفضاء المتجهي والتطبيع
│   │   ├── tfidf.py            # Member 4: مصفوفة TF-IDF
│   │   └── normalization.py    # Member 4: أطوال المستندات وتطبيع L2 ومتجهات الاستعلام
│   ├── retrieval/              # محركات الاسترجاع اللفظي والمنطقي
│   │   ├── phrase_query.py     # Member 5: مطابقة العبارات المتتالية
│   │   └── boolean_query.py    # Member 5: عمليات AND و AND NOT
│   ├── ranking/                # محركات حساب التشابه والترتيب
│   │   ├── similarity.py       # Member 5: حساب تشابه جيب التمام (Cosine Similarity)
│   │   └── ranking.py          # Member 5: فرز وترتيب المستندات تنازلياً
│   ├── output/                 # منسق ومُصدر التقارير
│   │   └── display.py          # Member 1: طباعة وتصدير الجداول والمصفوفات
│   ├── contracts.py            # Single Source of Truth: عقود البيانات المعتمدة
│   └── main.py                 # خط المعالجة المتكامل الموحد (Orchestrator)
├── tests/                      # حزمة الاختبارات الشاملة
│   ├── test_contracts.py       # التحقق الآلي من الـ Data Contracts
│   ├── test_ground_truth.py    # التحقق الشامل من مخرجات Part A و Part B المرجعية
│   ├── test_preprocessing.py   # اختبارات قراءة النصوص والـ Tokenizer
│   ├── test_term_statistics.py # اختبارات TF و WTF و DF و IDF
│   ├── test_tfidf.py           # اختبارات مصفوفة TF-IDF
│   ├── test_normalization.py   # اختبارات أطوال المستندات وتطبيع L2
│   ├── test_phrase_query.py    # اختبارات مطابقة العبارات
│   ├── test_boolean_query.py   # اختبارات العمليات البوليانية
│   └── test_ranking.py         # اختبارات درجات التشابه والترتيب
├── docs/                       # التوثيق الفني وأدلة الأعضاء
│   ├── CONCEPTUAL_QUESTIONS.md # إجابات الأسئلة المفاهيمية الستة (Part C)
│   ├── DATA_CONTRACTS.md       # مواصفات عقود البيانات
│   ├── GIT_WORKFLOW.md         # دليل الـ Git ومسار التطوير
│   ├── PROJECT_REQUIREMENTS.md # المتطلبات الأكاديمية الرسمية
│   └── members/                # الأدلة الشخصية لكل عضو
├── results/                    # المخرجات النهائية المحفوظة (Part A & Part B)
│   ├── part_a_tables.txt       # جداول الإحصاءات ومصفوفات TF-IDF والتطبيع
│   └── part_b_results.txt      # نتائج الاستعلامات ودرجات التشابه والترتيب
├── .github/                    # حوكمة GitHub: Templates, Rulesets, CI
├── requirements.txt            # المكتبات والاعتماديات
├── Makefile                    # اختصارات التشغيل السريع
├── pytest.ini                  # إعدادات بيئة الاختبار
├── CONTRIBUTING.md             # دليل المساهمة وقواعد الـ Git
└── README.md                   # واجهة المشروع والتوثيق التأسيسي
```

---

## ⚡ التشغيل السريع (Quick Start)

### 1. تجهيز بيئة العمل (Virtual Environment)
```bash
# إنشاء وتفعيل البيئة الافتراضية
python -m venv .venv

# على ويندوز (PowerShell):
.venv\Scripts\Activate.ps1
# أو على لينكس / ماك / Git Bash:
source .venv/bin/activate

# تثبيت المكتبات
pip install -r requirements.txt
```

### 2. تشغيل خط المعالجة المتكامل بأمر واحد
```bash
python src/main.py
# أو عبر Makefile:
make run
```

### 3. تشغيل حزمة الاختبارات الشاملة
```bash
pytest tests/
# أو عبر Makefile:
make test
```

---

## 👥 توزيع المهام والمسؤوليات (Team Roster)

| العضو | الدور الهندسي | الملفات المسؤولة عنها |
|---|---|---|
| **مصطفى (Mostafa)** | قائد الفريق ومهندس التكامل (Team Lead & Orchestration) | `src/main.py`, `src/contracts.py`, `src/output/display.py`, وحوكمة Git |
| **منذر (Monzer)** | معالجة البيانات والفهرس الموقعي (Data Processing & PySpark) | `src/preprocessing/`, `src/indexing/positional_index.py` |
| **إبراهيم (Ebrahim)** | مهندس الإحصائيات الرياضية (Term Statistics) | `src/statistics/term_statistics.py` (TF, WTF, DF, IDF) |
| **روان (Rovan)** | مهندس المتجهات والتطبيع (Vector Space & Normalization) | `src/vectorization/tfidf.py`, `normalization.py` |
| **فيبرونيا (Febronia)** | مهندس الاسترجاع والترتيب (Retrieval & Ranking Engine) | `src/retrieval/`, `src/ranking/` |

---

## 🎯 القيم المرجعية للاختبار والتحقق (Ground Truth Benchmarks)
تتطابق مخرجات المنظومة بنسبة 100% مع هذه النتائج المرجعية المعتمدة في تقرير المقرر:

| الاستعلام (Query) | نوع الاستعلام | المستندات المتطابقة | درجات التشابه المحسوبة (Cosine Similarity) | الترتيب النهائي (Ranked) |
|---|---|---|---|---|
| `"customer service"` | Phrase Query | `['d1', 'd2', 'd5', 'd10']` | $d1: 1.0000$<br>$d2: 0.6147$<br>$d5: 0.4159$<br>$d10: 0.2875$ | **1. d1**<br>2. d2<br>3. d5<br>4. d10 |
| `"sales growth"` | Phrase Query | `['d3', 'd5', 'd7', 'd8']` | $d5: 0.4847$<br>$d3: 0.4395$<br>$d8: 0.3240$<br>$d7: 0.3067$ | **1. d5**<br>2. d3<br>3. d8<br>4. d7 |
| `"customer service" AND "sales growth"` | Boolean AND | `['d5']` (التقاطع) | $d5: 0.6376$ | **1. d5** |
| `"customer service" AND NOT "sales growth"` | Boolean AND NOT | `['d1', 'd2', 'd10']` (الاستبعاد) | $d1: 1.0000$<br>$d2: 0.6147$<br>$d10: 0.2875$ | **1. d1**<br>2. d2<br>3. d10 |

> 📌 **ملاحظة أكاديمية هامة:** في استعلام `AND NOT`، تم بناء متجه الاستعلام حصرياً من كلمات العبارة الإيجابية الأولى (`customer`, `service`) لأن العبارة الثانية تعمل كفلتر استبعاد سلبي فقط.

---

## 🛡️ قواعد العمل والحوكمة (Rules of Engagement)
1. **ممنوع الـ Push المباشر نهائياً على `main`:** كل عمل يمر عبر Feature Branch مخصص و Pull Request رسمي لمراجعته بدقة.
2. **عقود البيانات خط أحمر (Contracts are Locked):** التزام تام بمواصفات `src/contracts.py` لمنع أي كسر في التكامل.
3. **المراجعة والدمج حصرية للقائد مصطفى (@mostafaelsonny):** القائد هو المسؤول الحصري عن تدقيق الكود والاعتماد.
4. **التطوير المتوازي وتغطية الاختبارات:** تم بناء المنظومة باستخدام Mock Data متوافقة تتيح العمل المتزامن لكافة الأعضاء.
5. **جودة الكود:** خلو الكود من أي أخطاء، تغطية شاملة باختبارات Pytest، وتوثيق دقيق لجميع الدوال والمعادلات.

---

دليل المساهمة التفصيلي: [CONTRIBUTING.md](CONTRIBUTING.md) • الإجابات المفاهيمية: [docs/CONCEPTUAL_QUESTIONS.md](docs/CONCEPTUAL_QUESTIONS.md)
