# ZTE Certificate Generator — Loading Page Redesign

## Context

- **Project:** zte_certificate_generator (Streamlit app)
- **URL:** https://zte-certificate-generator.streamlit.app/
- **Issue:** The current `st.spinner("Generating certificate...")` is ugly and generic
- **Date:** 2026-04-25

## Design Language

### Minimalista Clean

**Colors:**
- Background: `#0d0d0d`
- Surface: `#171717`
- Text primary: `#ffffff`
- Text secondary: `#a1a1a1`
- Accent success: `#22c55e`
- Border subtle: `rgba(255,255,255,0.08)`

**Typography:**
- Font: Inter (Google Fonts)
- Heading: 600 weight
- Body: 400 weight

**Motion:**
- Loading ring: 1.2s per rotation, ease-in-out
- Success transition: 400ms ease-out
- Staggered content reveal: 80ms delay between elements

## Loading State

- Centered ring spinner with gradient (gray → white)
- Text below: "Gerando certificado..." in secondary color
- No other elements visible — focused attention

## Success State

1. Ring freezes, turns green (#22c55e)
2. Checkmark appears in center (scale + fade-in, 300ms)
3. Certificate box fades in below (delay 200ms)
4. Details in collapsed expander (not cluttering)

## Components

### LoadingSpinner
- 48px ring, 3px stroke
- Gradient: conic-gradient with transparent gaps
- Smooth rotation

### SuccessCheckmark
- 48px container
- Ring turns green
- Checkmark SVG scales from 0.8 → 1.0, opacity 0 → 1

### CertificateCard
- Background: #171717
- Border: 1px solid rgba(255,255,255,0.08)
- Padding: 1.5rem
- Border-radius: 12px

### DetailsExpander
- Streamlit expander, collapsed by default
- Shows MAC addresses, board type, payload structure

## Changes to Original

- Remove `st.spinner` completely
- Replace with custom HTML/CSS spinner in loading state
- Style the success/error boxes to match new design language
- Use `Inter` font instead of `Courier Prime`
