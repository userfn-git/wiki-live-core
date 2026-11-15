# FN | WikiLife Core - المرجع الشخصي والجذع المعرفي (Yusra Trunk)

> **المالك والمطور الرئيسي:** `userfn-git` (FN) | **الفرع المركزي المعتمد:** `main` | **بيئة العمل:** `FN-WORKSTATION (Win11 Pro / Python 3.12 / C++20 / GCP)`

---

## 1. هويتي البرمجية ونواة النظام (Personal Core)
هذا المستودع هو المركز الشخصي الموحد لإدارة مشاريعي البرمجية، محركات الإدخال والأتمتة، والتوثيق المعرفي السحابي بإشراف **يسرى** على المسار المحلي `D:\projects\wiki-live-core`.

## 2. بيئة التشغيل والعتاد المعتمد (System Stack)
- **النظام المحلي:** Windows 11 Pro 64-bit | PowerShell & MSYS2 Bash
- **لغات التطوير:** Python 3.12, C++20, Lua, REST APIs
- **البنية السحابية:** Google Cloud (Cloud Run, Firestore, Cloud Functions) & GitHub SSH (`ED25519`)

## 3. خريطة المسارات الأربعة والفروع الـ 12
| المسار | الفروع | المهمة الخاصة بـ FN |
|---|---|---|
| **PATH-01: البنية والتحكم** | `BR01`..`BR03` | قفل الجذع `main`، محرك `Blob/Tree/Commit`، وتأمين `SSH` |
| **PATH-02: إدارة المعرفة** | `BR04`..`BR06` | قرارات `ADR-0001..0012`، أرشفة `Snapshots`، وصياغة يسرى |
| **PATH-03: التطوير والبرمجة** | `BR07`..`BR09` | فروع `Git-flow`، محولات السحابة، وفحص `GitHub Actions` |
| **PATH-04: النشر والإحاطة** | `BR10`..`BR12` | بيانات `JSON-LD`، معايير `NPOV`، ومقاييس `FN Telemetry` |

## 4. اختصاراتي السريعة (Quick Commands)
- فحص النظام: `python tests/verify_all.py`
- لوحة التحكم: `start chrome D:\projects\wiki-live-core\docs\dashboard.html`

---
> **[MUTUAL-LOCK]:** Synchronized with [Gemini.md](./Gemini.md) on branch main.
