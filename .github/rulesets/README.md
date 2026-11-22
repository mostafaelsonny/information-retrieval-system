# Rulesets (حماية فرعي main و develop)

الملفان `protect-main.json` و `protect-develop.json` يفرضان القواعد الصارمة لحماية المستودع البرمجي:

| إعداد GitHub | الحالة | في الـ JSON |
|---|---|---|
| Ruleset Name | Protect Main Branch / Protect Develop Branch | `name` |
| Enforcement Status | Active | `"enforcement": "active"` |
| Target Branches | `main` / `develop` | `conditions.ref_name.include` |
| Require a pull request before merging | **مفعّل إجبارياً** | قاعدة `pull_request` |
| Require approvals | **1 موافقة من مصطفى** | `required_approving_review_count: 1` |
| Require Code Owner review | **مفعّل (Mostafa عبر CODEOWNERS)** | `require_code_owner_review: true` |
| Dismiss stale approvals | **مفعّل عند أي commit جديد** | `dismiss_stale_reviews_on_push: true` |
| Require conversation resolution | **مفعّل (حل كل التعليقات)** | `required_review_thread_resolution: true` |
| Block force pushes | **مفعّل (ممنوع force push)** | قاعدة `non_fast_forward` |
| Restrict deletions | **مفعّل (ممنوع حذف الفرع)** | `deletion` |
| Bypass list | **Admin role فقط (Mostafa)** بنمط `pull_request` | `bypass_actors` |

---

## كيفية التطبيق التلقائي:
يتم تطبيق القواعد تلقائياً عبر الاسكريبت:
- على لينكس/ماك/Git Bash: `./scripts/setup_github.sh`
- على ويندوز PowerShell: `.\scripts\setup_github.ps1`

## كيفية التطبيق يدوياً من واجهة GitHub:
1. ادخل على `Settings` في الـ Repository.
2. اختر من القائمة الجانبية: `Rules` ← `Rulesets`.
3. اضغط على `New ruleset` ثم `Import a ruleset`.
4. اختر ملف `protect-main.json` ثم احفظ، وكرر نفس الخطوة مع `protect-develop.json`.
