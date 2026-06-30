# ماشین حساب پیشرفته - Advanced Calculator

یک ماشین حساب کامل و پیشرفته با قابلیت‌های مختلف برای ویندوز و اندروید.

## ✨ ویژگی‌ها

- **حالت‌های مختلف:** عادی، علمی، برنامه‌نویس، ماتریس
- **عملیات پایه:** جمع، تفریق، ضرب، تقسیم
- **توابع علمی:** سینوس، کوسینوس، تانژانت، لگاریتم، ریشه، توان
- **حافظه:** ذخیره، فراخوانی، جمع و تفریق حافظه
- **پشتیبانی از کیبورد**
- **رابط کاربری زیبا** با تم تاریک

## 📦 نصب و اجرا

### برای ویندوز (EXE)

1. فایل `calculator-win.exe` رو از قسمت [Releases](https://github.com/AnishtayiN/mashinhesab/releases) دانلود کنید
2. فایل رو اجرا کنید

### برای اندروید (APK)

1. فایل `calculator-android.apk` رو از قسمت [Releases](https://github.com/AnishtayiN/mashinhesab/releases) دانلود کنید
2. فایل رو روی گوشی اندروید نصب کنید

## 🚀 ساخت خودکار

این پروژه به صورت خودکار توسط GitHub Actions ساخته می‌شود:
- **Windows EXE:** از PyInstaller استفاده می‌شود
- **Android APK:** از Buildozer استفاده می‌شود

### شروع ساخت دستی

1. **Push به branch اصلی:**
   ```bash
   git push origin main
   ```

2. **ایجاد Tag جدید:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **اجرای دستی از GitHub Actions**

## 📁 ساختار پروژه

```
mashinhesab/
├── calculator.py      # کد اصلی ماشین حساب (PyQt6 - ویندوز)
├── main.py            # ورودی اصلی برای اندروید (Kivy)
├── buildozer.spec      # تنظیمات Buildozer برای اندروید
├── calculator.spec     # تنظیمات PyInstaller برای ویندوز
├── requirements.txt    # وابستگی‌های Python برای ویندوز
└── .github/
    └── workflows/
        ├── build_windows.yml
        └── build_android.yml
```

## 🔧 توسعه

### پیشنیازها

- Python 3.10 یا بالاتر
- برای ویندوز:
  ```bash
  pip install -r requirements.txt
  python calculator.py
  ```

- برای اندروید:
  ```bash
  pip install buildozer kivy
  buildozer android debug
  ```

### ساخت EXE برای ویندوز

```bash
pip install pyinstaller
pyinstaller calculator.spec --clean --noconfirm
```

## 🤝 مشارکت

جهت مشارکت، Pull Request ارسال کنید یا Issues گزارش دهید.

## 📜 لایسنس

MIT License

---

**ساخت:** برای [AnishtayiN](https://github.com/AnishtayiN)
**آدرس GitHub:** [https://github.com/AnishtayiN/mashinhesab](https://github.com/AnishtayiN/mashinhesab)
