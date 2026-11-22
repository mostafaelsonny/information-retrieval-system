# 📘 دليل المساهمة والحوكمة البرمجية (Contribution Guide)

> هذا الدليل يوضح القواعد الصارمة لإدارة الأكواد والـ Git Workflow في سبرنت الـ 6 ساعات. الالتزام بهذه القواعد إجباري لجميع أعضاء الفريق دون استثناء.

---

## 🛡️ سياسة حماية المستودع (Repository Protection Policy)
* فرعا **`main`** و **`develop`** محميان عبر **GitHub Rulesets**.
* **ممنوع منعاً باتاً الـ Push المباشر** على `main` أو `develop`.
* **ممنوع الـ Force Push** أو حذف أي فرع أساسي.
* **الموافقة والدمج حصرية للقائد مصطفى (@mostafaelsonny)**: لا يمكن لأي عضو دمج الـ PR الخاص به ذاتياً؛ مصطفى هو الـ Code Owner والمراجع الوحيد المخول بالـ Merge.

---

## 🌿 هيكل الفروع (Branching Strategy)
```text
main          النسخة النهائية المستقرة المعتمدة للتسليم (Release)
│
└── develop   فرع التجميع والتكامل المستمر (Integration Hub)
     ├── feature/monzer-preprocessing-indexing   (منذر: Loader, Tokenizer, Spark Index)
     ├── feature/ebrahim-statistics              (إبراهيم: TF, WTF, DF, IDF)
     ├── feature/rovan-vectorization             (روان: TF-IDF Matrix, Normalization)
     └── feature/febronia-retrieval-ranking      (فيبرونيا: Phrase, Boolean, Cosine Sim)
```

---

## 🔄 دورة حياة تنفيذ المهمة (Step-by-Step Workflow)
1. **استلام المهمة:** افتح كارت مهمتك في لوحة [Trello](https://trello.com/b/6b0233e1cccc215d1c4831a8) وانقله من `Sprint - To Do` إلى `In Progress`.
2. **إنشاء الفرع:** تأكد من تحديث فرع `develop` ثم انشئ فرعك الخاص:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/<your-assigned-branch>
   ```
3. **التطوير المتوازي باستخدام Mock Data:**
   * لا تنتظر زميلك! استورد بيانات الـ Mock من `src/contracts.py` واكتب دوالك واختبرها فوراً.
4. **الالتزام برسائل الـ Commit الواضحة والموجزة:**
   ```bash
   git commit -m "IR-04: implement pyspark positional index with 1-based indexing"
   ```
5. **تشغيل الاختبارات المحلية قبل فتح الـ PR:**
   ```bash
   pytest tests/
   python src/contracts.py
   ```
6. **فتح الـ Pull Request:**
   * افتح الـ PR موجهًا إلى فرع **`develop`** (وليس `main`).
   * املأ نموذج الـ PR بالكامل (`.github/pull_request_template.md`).
   * علّم على كافة بنود الـ Checklist.
7. **نقل الكارت في Trello:** انقل الكارت إلى قائمة `In Review (PR Review)`.
8. **المراجعة والدمج:** انتظر مراجعة مصطفى (@mostafaelsonny). إذا طُلب منك تعديل، قم به في نفس الفرع واعمل push؛ سيتم تحديث الـ PR تلقائياً.

---

## 📋 معايير مراجعة القائد مصطفى (The 5 Quality Gates)
لن يتم دمج أي PR إلا بعد التحقق من هذه النقاط الخمس:
1. **المتطلبات (Requirements):** هل الكود ينفذ المطلوب في كارت Trello بدقة دون زيادة أو نقصان؟
2. **التوافق مع العقد (Data Contracts):** هل أسماء الحقول ومفاتيح الـ Dictionaries مطابقة بالحرف لـ `src/contracts.py`؟
3. **الدقة الرياضية (Math & Logic):** هل الترقيم 1-based؟ هل اللوغاريتم $\log_{10}$؟ هل تم التحقق من أطوال المتجهات $L_2 = 1.0000$؟
4. **الاختبارات (Tests):** هل توجد Unit Tests تغطي الحالات الطبيعية والاستثنائية وهل تمر بنجاح؟
5. **سلامة التكامل (Clean Integration):** هل يمكن استدعاء الكود ودمجه في `src/main.py` دون أي تعارضات أو كراش؟

---

## 🔀 الترتيب التسلسلي الصارم للدمج (Merge Protocol - Hour 4)
في الساعة الرابعة (ساعة التكامل)، يتم دمج الفروع في `develop` بالترتيب التسلسلي التالي حصراً:
1. `feature/monzer-preprocessing-indexing` (الطبقة التأسيسية: قراءة وفهرسة).
2. `feature/ebrahim-statistics` (الطبقة الإحصائية: حسابات TF, WTF, DF, IDF).
3. `feature/rovan-vectorization` (طبقة المتجهات: مصفوفة TF-IDF وأطوال المستندات والتطبيع).
4. `feature/febronia-retrieval-ranking` (طبقة الاسترجاع: محرك الاستعلامات اللفظية والبوليانية والترتيب).
5. تجربة خط المعالجة الشامل `python src/main.py`.
6. بعد اجتياز كافة اختبارات الـ Ground Truth، **مصطفى فقط** يقوم بفتح PR لدمج `develop` إلى `main` واعتماد النسخة النهائية للتسليم!

---

## 🎯 معايير اكتمال المهمة (Definition of Done)
تعتبر أي مهمة "مكتملة ومقبولة" فقط عند استيفاء الآتي:
- [ ] الكود اجتاز المراجعة وتم دمجه بنجاح في فرع `develop`.
- [ ] تم التحقق من سلامة المخرجات عبر `src/contracts.py`.
- [ ] اجتياز كافة الـ Unit Tests التابعة للمهمة.
- [ ] صاحب المهمة قادر على شرح كل سطر كود فيها بثقة أثناء مناقشة المشروع.
- [ ] نقل كارت المهمة إلى قائمة `Done / Accepted` في Trello.
