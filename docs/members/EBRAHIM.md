# 👤 دليل المهندس: إبراهيم (Ebrahim)
**الدور:** Information Statistics Engineer  
**الفرع المخصص:** `feature/ebrahim-statistics`  
**كروت Trello:** IR-05, IR-06

---

### 🎯 المهام المطلوبة منك داخل `src/statistics/term_statistics.py`:
1. **`calculate_raw_tf(positional_index)`:**
   - حساب عدد تكرارات الكلمة في كل مستند عبر حساب طول قائمة المواقع: `len(positions)`.
2. **`calculate_weighted_tf(raw_tf)`:**
   - تطبيق دالة التخميد اللوغاريتمي باستخدام `math.log10`:
     $$WTF = 1.0 + \log_{10}(TF) \quad \text{عندما } TF > 0 \text{ وإلا } 0.0$$
3. **`calculate_df(positional_index)`:**
   - حساب عدد المستندات الفريدة التي ظهرت فيها الكلمة: `len(postings.keys())`.
4. **`calculate_idf(df, total_documents=10)`:**
   - حساب الوزن العكسي:
     $$IDF = \log_{10}\left(\frac{total\_documents}{DF}\right)$$

### ⚠️ تحذيرات هامة:
* استخدم `math.log10` للأساس 10 وليس `math.log` الطبيعي!
* لا تقرب الأرقام داخلياً؛ احتفظ بالدقة الكاملة في الـ Dictionary.
* ابدأ فوراً باستخدام الـ Mock Data من `src/contracts.py` دون انتظار منذر.
