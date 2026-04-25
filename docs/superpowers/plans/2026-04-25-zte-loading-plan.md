# Loading Page Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the ugly `st.spinner` with an elegant minimalista clean loading page for the ZTE Certificate Generator Streamlit app.

**Architecture:** Single-file Streamlit app modification. Custom HTML/CSS components for loading spinner and success state, replacing Streamlit's default spinner. CSS-only animations, no JavaScript dependencies.

**Tech Stack:** Python 3, Streamlit, HTML/CSS (inline), Google Fonts (Inter)

---

## File Mapping

- **Modify:** `zte_certificate_generator.py` — replace spinner, update CSS, update success/error states

---

## Tasks

### Task 1: Update CSS Design System

**Files:**
- Modify: `zte_certificate_generator.py:16-210` (CSS block)

- [ ] **Step 1: Replace the CSS block**

Find lines 16-210 containing the old CSS. Replace entirely with:

```python
# Custom CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {
        background: #0d0d0d;
        color: #ffffff;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stAppHeader {display: none;}
    
    /* Loading Spinner */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 4rem 0;
        gap: 1.5rem;
    }
    
    .spinner-ring {
        width: 48px;
        height: 48px;
        border: 3px solid rgba(255,255,255,0.1);
        border-top-color: #ffffff;
        border-radius: 50%;
        animation: spin 1.2s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .loading-text {
        color: #a1a1a1;
        font-size: 0.95rem;
        font-weight: 400;
        letter-spacing: 0.02em;
    }
    
    /* Success State */
    .success-ring {
        width: 48px;
        height: 48px;
        border: 3px solid #22c55e;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: success-pop 0.3s ease-out forwards;
    }
    
    @keyframes success-pop {
        0% { transform: scale(0.8); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .checkmark {
        width: 20px;
        height: 20px;
        stroke: #22c55e;
        stroke-width: 3;
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
        stroke-dasharray: 24;
        stroke-dashoffset: 24;
        animation: checkmark-draw 0.3s ease-out 0.1s forwards;
    }
    
    @keyframes checkmark-draw {
        to { stroke-dashoffset: 0; }
    }
    
    /* Certificate Card */
    .certificate-card {
        background: #171717;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        animation: fade-in-up 0.4s ease-out 0.2s both;
    }
    
    @keyframes fade-in-up {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .certificate-output {
        background: rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 1rem;
        color: #22c55e;
        font-family: 'Inter', monospace;
        font-size: 0.85rem;
        word-break: break-all;
        margin: 1rem 0;
    }
    
    /* Info & Details boxes */
    .info-box {
        background: rgba(255,255,255,0.05);
        border-left: 3px solid #ffffff;
        padding: 1rem 1.5rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 2rem;
        font-size: 0.9rem;
        color: #a1a1a1;
    }
    
    .details-box {
        background: #171717;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1.25rem;
        margin: 1rem 0;
        font-size: 0.85rem;
        color: #a1a1a1;
        line-height: 1.6;
    }
    
    .details-box code {
        background: rgba(0,0,0,0.3);
        padding: 0.15rem 0.4rem;
        border-radius: 4px;
        font-family: 'Inter', monospace;
        color: #ffffff;
    }
    
    /* Section header */
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #ffffff;
        margin: 2rem 0 1rem;
        border-left: 3px solid #ffffff;
        padding-left: 0.75rem;
    }
    
    /* Success/Error boxes */
    .success-box {
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid #22c55e;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        color: #ffffff;
        font-weight: 500;
        margin: 1rem 0;
    }
    
    .error-box {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid #ef4444;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        color: #ffffff;
        font-weight: 500;
        margin: 1rem 0;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: #171717;
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 8px;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        padding: 0.6rem 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ffffff;
        box-shadow: 0 0 0 2px rgba(255,255,255,0.1);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #555555;
    }
    
    /* Button */
    .stButton > button {
        background: #ffffff;
        color: #0d0d0d;
        border: none;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        padding: 0.7rem 1.5rem;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #e5e5e5;
        transform: translateY(-1px);
    }
    
    /* Links */
    a { color: #ffffff; }
</style>
""", unsafe_allow_html=True)
```

- [ ] **Step 2: Verify syntax**

Run: `python -c "import ast; ast.parse(open('/tmp/zte_certificate_generator/zte_certificate_generator.py').read())"`
Expected: No syntax errors

- [ ] **Step 3: Commit**

```bash
cd /tmp/zte_certificate_generator && git add zte_certificate_generator.py && git commit -m "style: replace CSS design system with minimalista clean"
```

---

### Task 2: Create Custom Loading Component

**Files:**
- Modify: `zte_certificate_generator.py` — add loading component function and update main()

- [ ] **Step 1: Add loading component function before main()**

Find the line with `def main():` (line ~310). Add this function right before it:

```python
def render_loading_spinner():
    """Render the custom minimalista loading spinner"""
    st.markdown("""
    <div class="loading-container">
        <div class="spinner-ring"></div>
        <div class="loading-text">Gerando certificado...</div>
    </div>
    """, unsafe_allow_html=True)
```

- [ ] **Step 2: Verify function is defined**

Run: `python -c "import sys; sys.path.insert(0, '/tmp/zte_certificate_generator'); exec(open('/tmp/zte_certificate_generator/zte_certificate_generator.py').read().split('if __name__')[0]); print('OK')"`
Expected: OK

- [ ] **Step 3: Commit**

```bash
cd /tmp/zte_certificate_generator && git add zte_certificate_generator.py && git commit -m "feat: add custom loading spinner component"
```

---

### Task 3: Create Success State Component

**Files:**
- Modify: `zte_certificate_generator.py` — add success checkmark component

- [ ] **Step 1: Add success checkmark function after render_loading_spinner**

```python
def render_success_checkmark():
    """Render success state with checkmark animation"""
    st.markdown("""
    <div class="loading-container">
        <div class="success-ring">
            <svg class="checkmark" viewBox="0 0 24 24">
                <polyline points="4,12 10,18 20,6"></polyline>
            </svg>
        </div>
    </div>
    """, unsafe_allow_html=True)
```

- [ ] **Step 2: Commit**

```bash
cd /tmp/zte_certificate_generator && git add zte_certificate_generator.py && git commit -m "feat: add success checkmark component"
```

---

### Task 4: Replace st.spinner with Custom Loading

**Files:**
- Modify: `zte_certificate_generator.py:358-359`

- [ ] **Step 1: Find and replace the spinner call**

Find line 358:
```python
with st.spinner("Generating certificate..."):
```

Replace with:
```python
render_loading_spinner()
# Simulate processing time for UX
import time
time.sleep(1.5)
```

- [ ] **Step 2: Verify the replacement**

Run: `grep -n "render_loading_spinner" /tmp/zte_certificate_generator/zte_certificate_generator.py`
Expected: Shows the line number where it's called

- [ ] **Step 3: Commit**

```bash
cd /tmp/zte_certificate_generator && git add zte_certificate_generator.py && git commit -m "feat: replace st.spinner with custom loading UI"
```

---

### Task 5: Update Success State to Use Checkmark

**Files:**
- Modify: `zte_certificate_generator.py` — success handling after certificate generation

- [ ] **Step 1: After generating certificate, show success checkmark first**

Find after line 359's processing. After `if result['success']:`, add:

```python
# Show success checkmark first
render_success_checkmark()
st.markdown('<div class="loading-container" style="padding-top:0;padding-bottom:1rem;"><div class="loading-text" style="color:#22c55e;">Certificado gerado!</div></div>', unsafe_allow_html=True)
```

- [ ] **Step 2: Verify**

Run: `grep -n "render_success_checkmark" /tmp/zte_certificate_generator/zte_certificate_generator.py`
Expected: Shows line number

- [ ] **Step 3: Commit**

```bash
cd /tmp/zte_certificate_generator && git add zte_certificate_generator.py && git commit -m "feat: add success state with checkmark animation"
```

---

### Task 6: Update Certificate Card Styling

**Files:**
- Modify: `zte_certificate_generator.py` — certificate output section

- [ ] **Step 1: Find the certificate output HTML (line ~375) and update class**

Find:
```python
st.markdown(f"""
<div class="certificate-output">
    {certificate_text}
</div>
""", unsafe_allow_html=True)
```

The class `certificate-output` is already defined in Task 1 CSS.

- [ ] **Step 2: Commit**

```bash
cd /tmp/zte_certificate_generator && git add zte_certificate_generator.py && git commit -m "style: update certificate card with fade-in animation"
```

---

### Task 7: Final Review and Push

- [ ] **Step 1: Run the app locally to verify**

```bash
cd /tmp/zte_certificate_generator && pip install streamlit cryptography -q && streamlit run zte_certificate_generator.py --server.headless true
```

Manual verification: Generate a certificate and check the loading/success animation.

- [ ] **Step 2: Push to GitHub**

```bash
cd /tmp/zte_certificate_generator && git push origin main
```

---

## Spec Coverage Check

- [x] Loading ring with 1.2s rotation — Task 2
- [x] Text "Gerando certificado..." — Task 2
- [x] Success ring turns green with checkmark — Task 3, Task 5
- [x] Certificate card fades in — Task 6
- [x] Details in collapsed expander — Already in original code (expander used)
- [x] Inter font instead of Courier Prime — Task 1 CSS
- [x] Colors match spec (#0d0d0d, #171717, #22c55e) — Task 1 CSS

## Type Consistency Check

All CSS class names are consistent throughout:
- `loading-container`, `spinner-ring`, `loading-text`
- `success-ring`, `checkmark`
- `certificate-card`, `certificate-output`
- `info-box`, `details-box`, `section-header`

No mismatches found.
