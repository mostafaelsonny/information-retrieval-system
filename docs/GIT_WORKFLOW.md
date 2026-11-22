# 🌿 دليل سير العمل على Git و GitHub (Git Workflow)

> هذا الدليل يعطيك الأوامر المباشرة خطوة بخطوة للعمل اليومي على المستودع دون أي تعارضات أو أخطاء.

---

## 1. إعداد البيئة للمرة الأولى (Initial Setup)
```bash
# 1. استنساخ المستودع
git clone https://github.com/mostafaelsonny/information-retrieval-system.git
cd information-retrieval-system

# 2. إنشاء وتفعيل البيئة الافتراضية
python -m venv .venv

# على ويندوز (PowerShell):
.venv\Scripts\Activate.ps1
# أو على Git Bash / macOS / Linux:
source .venv/bin/activate

# 3. تثبيت المتطلبات
pip install -r requirements.txt
```

---

## 2. بدء مهمة جديدة على Branch مخصص
**قاعدة ذهبية:** لا تكتب أي كود أبداً وأنت على فرع `main` أو `develop`!

```bash
# 1. الانتقال إلى develop والتأكد من أحدث التحديثات
git checkout develop
git pull origin develop

# 2. إنشاء فرعك المخصص وفقاً لاسم المهمة في Trello
# مثال لمنذر:
git checkout -b feature/monzer-preprocessing-indexing

# مثال لإبراهيم:
git checkout -b feature/ebrahim-statistics

# مثال لروان:
git checkout -b feature/rovan-vectorization

# مثال لفيبرونيا:
git checkout -b feature/febronia-retrieval-ranking
```

---

## 3. كتابة الكود والـ Commits المنتظمة
احرص على كتابة رسائل Commit واضحة ترتبط برقم التاسك في Trello:
```bash
# فحص الملفات المعدلة
git status

# إضافة الملفات
git add src/preprocessing/tokenizer.py tests/test_tokenizer.py

# كتابة الـ Commit
git commit -m "IR-03: implement 1-based tokenization with positional tuples"
```

---

## 4. فحص واختبار الكود قبل الرفع
قبل أن تدفع أي كود إلى GitHub، شغل هذه الأوامر وتأكد من نجاحها جميعاً محلياً:
```bash
# 1. التحقق من مطابقة عقود البيانات
python src/contracts.py

# 2. تشغيل حزمة الاختبارات الشاملة
pytest tests/
```

---

## 5. رفع الفرع وفتح الـ Pull Request
```bash
# رفع الفرع إلى GitHub
git push -u origin feature/<your-branch-name>
```

ثم ادخل على GitHub:
1. ستجد إشعاراً يقول: `feature/... had recent pushes 1 minute ago`. اضغط على **Compare & pull request**.
2. تأكد أن الفرع المستهدف (Base branch) هو **`develop`** (وليس `main`).
3. سيظهر لك نموذج الـ PR الجاهز (`.github/pull_request_template.md`). املأ جميع الحقول وعلم على بنود الـ Checklist.
4. اضغط على **Create pull request**.
5. انقل كارت المهمة في Trello إلى قائمة `In Review (PR Review)`.
6. انتظر مراجعة القائد مصطفى (@mostafaelsonny) للـ PR وموافقته واعتماده.
