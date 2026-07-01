# Graphic Calculator - ماشین حساب گرافیکی

یک برنامه ماشین حساب اندرویدی زیبا و قدرتمند با فلاتر (Dart) که دارای رابط کاربری گرافیکی و انیمیشن‌های جذاب است.

## ویژگی‌ها

- ✅ طراحی مدرن و زیبا با تم تاریک/روشن
- ✅ عملیات ریاضی کامل (+, -, *, /, %)
- ✅ پشتیبانی از اعداد اعشاری
- ✅ حافظه موقت (Memory)
- ✅ گرافیک و انیمیشن‌های سیال
- ✅ رابط کاربری واکنش‌گرا
- ✅ سازگار با تمام اندازه‌های صفحه نمایش

## ساختار پروژه

```
graphic_calculator/
├── android/          # کد Native اندروید
├── ios/              # کد Native iOS
├── lib/              # کد اصلی Dart
│   ├── main.dart     # نقطه ورود برنامه
│   ├── app/          # تنظیمات اصلی برنامه
│   ├── screens/      # صفحه‌ها
│   ├── widgets/      # ویجت‌های سفارشی
│   └── utils/        # توابع کمکی
├── test/             # تست‌ها
├── assets/           # فایل‌های استاتیک
├── pubspec.yaml      # وابستگی‌ها
└── .github/
    └── workflows/    # GitHub Actions
        └── build.yml # workflow ساخت APK
```

## پیش نیازها

- Flutter SDK (نسخه 3.0 یا بالاتر)
- Dart SDK (نسخه 3.0 یا بالاتر)
- Android Studio یا VS Code
- یک دستگاه اندرویدی یا شبیه‌ساز

## نصب و اجرا

```bash
# رفتن به پوشه پروژه
cd graphic_calculator

# دریافت وابستگی‌ها
flutter pub get

# اجرا روی دستگاه
flutter run

# ساخت APK
flutter build apk --release
```

## ساخت APK خودکار با GitHub Actions

این پروژه دارای یک workflow خودکار است که با هر push به شاخه `main`، APK را ساخته و در بخش Releases GitHub قرار می‌دهد.

## contributed

- [Mistral Vibe](https://github.com/mistralai) - ایجاد کننده اولیه

## لایسنس

MIT License
