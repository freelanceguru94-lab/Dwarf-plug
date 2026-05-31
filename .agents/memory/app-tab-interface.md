---
name: App Tab Interface
description: Bottom nav tab structure for the Dwarf Plug site — Home/Shop/Cart/Order pages
---

## Rule
The site is structured as a mobile app with 4 tab pages (#page-home, #page-shop, #page-cart, #page-order). Only the active page has `class="active"` (display:block). Switching is handled by `switchTab(tab)`.

## How it works
- `switchTab(tab)` toggles `.active` on `.app-page` divs and `.bnav-btn` elements
- Shop page renders lazily: `_shopInit` flag prevents duplicate `renderCatalog()`/`renderCatNav()` calls
- Cart page mirrors `#cart-rows` innerHTML to `#cp-cart-rows` via `updateCartSummary()`
- Bottom nav badge `#bnav-cart-badge` is updated alongside `#hdr-cart-num`
- Flash timer is perpetual (no dismiss, no sessionStorage check)
- Header cart icon calls `switchTab('cart')`, CTA button calls `switchTab('shop')`
- `resetOrder()` calls `switchTab('home')` instead of scrollTo

**Why:** Converting from scroll-based to tab-based navigation to match a mobile app UX pattern requested by the user.

**How to apply:** Any new feature that needs its own "screen" should be a new `<div id="page-X" class="app-page">` with a corresponding bottom nav button added to `.bottom-nav`.
