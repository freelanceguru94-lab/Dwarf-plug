---
name: AI Product Images
description: Status of AI-generated product images and their mapping in IMG object
---

## Generated (in imgs/)
- hero_flower.png — hero section BG decoration (opacity 0.18, right side)
- prod_concentrate_new.png → IMG.concentrate
- prod_hash_new.png → IMG.hash_resin, IMG.hash_dark
- prod_oils_new.png → IMG.tincture
- prod_preroll_new.png → IMG.preroll
- prod_seeds_new.png → IMG.seeds, IMG.seeds2

## Missing (failed generation)
- prod_edibles.png → still using catalog/gummies.jpg etc.
- prod_vape_new.png → still using imgs/catalog/vape.jpg

**Why:** Async batch generation job had 2 failures. Fallback to catalog/ stock photos for edibles and vapes.
