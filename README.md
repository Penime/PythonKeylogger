<!-- language: rtl -->

# PythonKeylogger
פרוייקט זה הוא Keylogger שנכתב בשפת Python.

## תכונות

- לכידת הקשות מקלדת
- שמירת נתונים לקובץ
- שליחת נתונים לשרת
- שמירת נתונים בשרת

## דרישות מערכת

- Python 3.x

## התקנה

1. קלון את הריפו:

   ```shell
   git clone https://github.com/Penime/PythonKeylogger.git
   ```

2. כנס לתיקיית הפרויקט:

   ```shell
   cd PythonKeylogger
   ```

3. צור סביבה וירטואלית (*אופציונלי*):

   1. וודא שאתה בתיקיית `PythonKeylogger`

   2. הרץ פקודה:
      ```shell
      python -m venv .venv
      ```

4. התקן את התלויות:

   ```shell
   pip install -r requirements.txt
   ```

## שימוש

1. הפעל את השרת בתוך תקיית `server` על ידי:
   ```shell
   python run.py
   ```

2. להפעלת ה-Keylogger, רץ את הסקריפט הראשי `main.py` בתיקיית `key_logger`:

   ```shell
   python main.py
   ```

## אזהרה

השימוש ב-Keylogger עלול להפר זכויות פרטיות והחוק. יש להשתמש בו רק לצרכים חוקיים ובהתאם לחוקים המקומיים שלך.
