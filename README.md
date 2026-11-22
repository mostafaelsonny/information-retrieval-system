# 🔍 Information Storage & Retrieval (IR) System

نظام متكامل لتخزين واسترجاع المعلومات مبني باستخدام **PySpark** و **Vector Space Model (VSM)**، ومصمم لمعالجة نصوص قطاع الأعمال (Business Corpus - 10 Documents) واسترجاعها بدقة فائقة عبر **Phrase Queries** و **Boolean Queries** وترتيبها باستخدام **Cosine Similarity Ranking**.

> ⏱️ **زمن الإنجاز:** سبرنت مكثف لمدة **6 ساعات** (6-Hour Sprint).  
> 👥 **فريق العمل:** 5 مهندسين بتطوير متوازي وتكامل تسلسلي مركزي بقيادة مصطفى (@mostafaelsonny).  
> 📋 **لوحة متابعة المهام:** [Trello Board — IR 6-Hour Sprint](https://trello.com/b/6b0233e1cccc215d1c4831a8)

---

## 👋 عضو جديد في الفريق؟ ابدأ من هنا!
إذا كنت تنضم للمشروع لأول مرة، اتبع هذا المسار المباشر لتبدأ فوراً بدون أي ارتباك:
1. **[docs/START_HERE.md](docs/START_HERE.md):** مدخل مبسط يشرح ما هو نظام الـ IR، والمشكلة التي نحلها، وكيف ترتبط القطع ببعضها.
2. **[docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md):** دليلك لإنشاء Branch، وتحديث كودك، وتشغيل الاختبارات، وفتح Pull Request احترافي.
3. **[docs/DATA_CONTRACTS.md](docs/DATA_CONTRACTS.md):** عقود البيانات الرسمية الصارمة (Single Source of Truth) — اقرأها قبل كتابة سطر كود واحد!
4. **دليلك الشخصي وفقاً لدورك في الفريق:**
   - [Monzer (Data Processing & PySpark)](docs/members/MONZER.md)
   - [Ebrahim (Information Statistics)](docs/members/EBRAHIM.md)
   - [Rovan (Vector Space & Normalization)](docs/members/ROVAN.md)
   - [Febronia (Retrieval & Ranking)](docs/members/FEBRONIA.md)
   - [Mostafa (Team Leader & Integration)](docs/members/MOSTAFA.md)
5. **كارت مهمتك على Trello:** يحتوي على الوصف الدقيق، والمدخلات والمخرجات، ومعايير القبول (Acceptance Criteria).

---

## 💡 فكرة المشروع ببساطة (Zero-Knowledge Guide)
نظام استرجاع وتخزين المعلومات (IR) مثل محرك بحث مصغر:
1. **قراءة النصوص (Document Ingestion):** نقرأ 10 مستندات نصية في مجال الأعمال، ونحول كلماتها إلى حروف صغيرة ونزيل علامات الترقيم **دون حذف الكلمات الشائعة (No Stop Words) ودون اشتقاق (No Stemming)**.
2. **الفهرس الموقعي (Positional Index via PySpark):** نبني فهرساً موزعاً لا يسجل فقط وجود الكلمة في المستند، بل يسجل **رقم موقع الكلمة داخل المستند (1-based)**. هذا الفهرس الموقعي هو السر الذي يُمكّننا من البحث عن عبارات دقيقة متتالية مثل `"customer service"`.
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
   - **Boolean Logic:** تقاطع القوائم لـ `AND`، والفرق والاستبعاد لـ `AND NOT`.
   - **Cosine Similarity:** حساب حاصل الضرب النقطي (Dot Product) بين متجه الاستعلام ومتجهات المستندات المطابقة، وترتيب المستندات تنازلياً من الأكثر تطابقاً إلى الأقل.

---

## 🛠️ التقنيات المستخدمة (Tech Stack)

| المكون | التقنية المعتمدة | الاستخدام |
|---|---|---|
| **اللغة الأساسية** | Python 3.11 / 3.12 | لغة المعالجة والتنفيذ |
| **المعالجة الموزعة** | Apache Spark (PySpark 3.4+) | بناء الفهرس الموقعي الضخم بشكل متوازي |
| **الحسابات الرياضية** | NumPy / Math | مصفوفات TF-IDF وحسابات معيار $L_2$ |
| **الاختبارات وضمان الجودة** | Pytest 7.4+ | اختبارات المطابقة الصارمة وعقود البيانات |
| **التنسيق والعرض** | Tabulate / Built-in Formatter | إخراج الجداول وحفظ تقارير Part A و Part B |
| **إدارة المشروع والنسخ** | Git, GitHub, Trello | حوكمة الكود، والـ Rulesets، وتتبع المهام |

---

## 🏗️ البنية المعمارية للمستودع (Repository Structure)

```text
information-retrieval-system/
├── data/                       # مستندات الأعمال العشرة (d1.txt إلى d10.txt)
├── src/                        # الكود المصدري للمشروع
│   ├── preprocessing/          # قراءة الملفات وتقطيع الكلمات مع المواقع
│   │   ├── document_loader.py  # Member 2: قراءة المستندات وتنظيفها
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
│   └── test_ground_truth.py    # مطابقة مخرجات الاستعلامات الأربعة المرجعية
├── docs/                       # التوثيق الفني وأدلة الأعضاء
├── results/                    # المخرجات النهائية المحفوظة (Part A & Part B)
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
يجب أن تتطابق مخرجات المنظومة بدقة 100% مع هذه النتائج المرجعية:

| الاستعلام (Query) | نوع الاستعلام | المستندات المتطابقة (Matching Documents) | المتصدر في الترتيب (Top Ranked) |
|---|---|---|---|
| `"customer service"` | Phrase Query | `['d1', 'd2', 'd5', 'd10']` | **d1** |
| `"sales growth"` | Phrase Query | `['d3', 'd5', 'd7', 'd8']` | **d5 / d8** |
| `"customer service" AND "sales growth"` | Boolean AND | `['d5']` (التقاطع Intersection) | **d5** |
| `"customer service" AND NOT "sales growth"` | Boolean AND NOT | `['d1', 'd2', 'd10']` (الاستبعاد Difference) | **d1** |

---

## 🛡️ قواعد العمل والحوكمة (Rules of Engagement)
1. **ممنوع الـ Push المباشر نهائياً على `main` أو `develop`:** كل عمل يمر عبر Feature Branch مخصص و Pull Request رسمي.
2. **عقود البيانات خط أحمر (Contracts are Locked):** ممنوع تغيير أي مسمى مفتاح أو دالة دون موافقة القائد مصطفى.
3. **المراجعة والدمج حصرية للقائد مصطفى (@mostafaelsonny):** القائد هو المسؤول الوحيد عن مراجعة الـ PR والموافقة عليه ودمجه.
4. **تطوير متوازي دون انتظار (Parallel Execution):** كل عضو يمتلك بيانات Mock مطابقة للعقد في الكارت الخاص به، ويبدأ التطوير فوراً من الدقيقة الأولى.
5. **ممنوع دمج أي كود دون اختبارات:** يجب أن تجتاز جميع الدوال اختبارات الـ Unit Tests وتتوافق مع `src/contracts.py`.

---

دليل المساهمة التفصيلي: [CONTRIBUTING.md](CONTRIBUTING.md) • غرفة العمليات والمتابعة: [index.html](index.html)
