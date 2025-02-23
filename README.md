<style>
  body {
    direction: ltr; /* Set default direction to LTR */
  }
  .rtl {
    direction: rtl; /* For RTL content */
    text-align: right;
  }
  .ltr {
    direction: ltr;
    text-align: left;
  }
</style>

<p class="rtl">هذا نص باللغة العربية في اتجاه من اليمين إلى اليسار.</p>
<p class="ltr">This is an English text in left-to-right direction.</p>
<pre class="ltr"><code>console.log('This is code block in LTR');</code></pre>
<div class="rtl">
هذا نص باللغة العربية في اتجاه من اليمين إلى اليسار.
</div>

<div class="ltr">
This is an English text in left-to-right direction.
</div>

```javascript
console.log('This is code block in LTR');
```
### Bonus Tip:
If you don't like writing `<div>` tags everywhere, you can also use a `dir` attribute:
```markdown
<p dir="rtl">هذا نص باللغة العربية في اتجاه من اليمين إلى اليسار.</p>

<p dir="ltr">This is an English text in left-to-right direction.</p>
```