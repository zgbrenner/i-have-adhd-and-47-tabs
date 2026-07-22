# Starter discussion copy

Run the **Seed community discussions** workflow after GitHub Discussions is enabled. The workflow creates these posts once and skips titles that already exist:

1. **Welcome to I Have ADHD and 47 Tabs**
2. **Share the AI answer that made you install this**
3. **Which platform are you using it with?**
4. **Which language should we translate next?**

The workflow uses the default `announcements`, `show-and-tell`, `general`, and `ideas` categories. If a category was renamed or removed, recreate it or adjust `.github/workflows/seed-discussions.yml`.
