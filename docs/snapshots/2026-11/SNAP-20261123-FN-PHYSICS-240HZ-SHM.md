# SNAP-20261123: اكتمال منظومة FN Physics Engine (240Hz Two-Way SHM) وحوكمة دورة التشغيل

- **التاريخ:** 2026-11-23
- **المسار والفرع:** `PATH-02: Knowledge Management` -> `BR05: Gemini Session Tree Snapshots`
- **النطاق المستهدف:** `D:\projects\fn_physics_engine` و `D:\terminals\config\master_profile.ps1` و `D:\Lua`
- **البيئة التشغيلية:** `FN-WORKSTATION` (Windows 11 Pro, MSYS2 UCRT64 GCC 16.2.0, Python 3.12 `D:\envs\rl_py_env`, Isolated `D:\`)

---

## 1. ملخص الإنجاز الهندسي (Executive Summary)
تم إغلاق حلقة الربط ثنائي الاتجاه بتردد **240Hz** بين نواة المحرك الفيزيائي المكتوبة بلغة **C++20** وجسر **Python SHM** عبر مقطع الذاكرة المشتركة `Local\FN_PHYSICS_SHM` (48 bytes)، مع استكمال حوكمة دورة التشغيل والإيقاف (`rl-live` و `rl-stop`)، وعكس وصلة الربط الرمزية لسكربتات **Logitech G HUB Lua (`v9.4.0`)**، وتطهير مستودع `fn_physics_engine` من الملفات الثنائية والمكررة.

## 2. المكونات المنجزة والموثقة (Verified Artifacts)
1. **توحيد بناء C++20 (`CMakePresets.json`):**
   - اعتماد سلسلة أدوات `MSYS2 UCRT64` (`D:/Tools/msys64/ucrt64/bin/g++.exe` GCC 16.2.0) ومولد `Ninja` بـ 12 خيط معالجة.
   - تفعيل رايات التحسين القصوى (`-O3 -march=native -DNDEBUG`) لإنتاج `build\ucrt64-release\fn_physics_engine.exe` مع استبعاد مخرجات البناء في `.gitignore`.
2. **البروتوكول الثنائي للذاكرة المشتركة (`Local\FN_PHYSICS_SHM` - 48 Bytes):**
   - **قناة الإرسال (`TX@0` — 32 bytes):** تخطيط `<6fi?3x` لنقل إحداثيات الفيزياء (`x, y, z, pitch, yaw, roll`) وعداد الإطارات (`frame_count`) وحالة النشاط (`is_active`) من C++ إلى بايثون.
   - **قناة الاستقبال (`RX@32` — 16 bytes):** تخطيط `<ffi??2x` لإرسال أوامر التحكم (`throttle, steer, cmd_seq, boost_active, jump_active`) من بايثون إلى C++ بمعدل `~240Hz` (`4.166ms`).
   - توحيد جسر بايثون في الجذر (`pyrocketsim_shm_bridge.py`) وحذف النسخة القديمة المكررة `src/pyrocketsim_shm_bridge.py`.
3. **حوكمة الطرفية واختصاري `rl-live` و `rl-stop` (`D:\terminals\config\master_profile.ps1`):**
   - إضافة دالة `rl-live` المشفرة بترميز `UTF-16LE Base64` (`-EncodedCommand`) لتجاوز قيود تحليل `wt.exe` (`0x80070002`) وتشغيل لوحتي المراقبة المتوازيتين بكلمة واحدة.
   - إضافة دالة `rl-stop` المرافقة لإيقاف `fn_physics_engine.exe` و `pyrocketsim_shm_bridge.py` فوراً وتحرير مقطع `Local\FN_PHYSICS_SHM` بضغطة واحدة.
4. **عكس وصلة Lua وتنظيم الماكرو المعتمد (`v9.4.0`):**
   - تحويل `D:\projects\fn_physics_engine\lua` إلى مجلد حقيقي متتبع في Git، وربط `D:\Lua` به كوصلة `Junction` لخدمة **Logitech G HUB** لحظياً.
   - تثبيت النسخة النهائية `lua/FN_PRO_v9.4.0_FINAL.lua` (218 سطراً، `Pace=1.04`, `WALL_DASH=9`, `DEADZONE=0.05`) وعزل المسودات والنسخ السابقة داخل `lua/archive/`.
5. **تطهير شجرة المستودع (`fn_physics_engine` Repository Hygiene):**
   - تحديث `.gitignore` لاستبعاد `*.dll` و `__pycache__/` و `*.pyc`، وفك تتبّع `fn_shm.dll` و `core/lua54.dll` وملفات الكاش، وحذف النسخ المكررة في الجذر (`RL_Master_Engine.lua` و `TAInput.ini`).

## 3. معايير التحقق والحالة النهائية (Verification Status)
- **مستودع `fn_physics_engine`:** نظيف ومتزامن بالكامل مع `origin/main` دون أي ملفات ثنائية أو وصلات مكسورة.
- **دورة التشغيل والإيقاف:** `rl-live` للإطلاق المتوازي `240Hz`، `rlpush -LaunchGame` لتشغيل **Rocket League** بعد تفريغ `VRAM` عبر `yusra-stop`، و `rl-stop` للإغلاق النظيف.
