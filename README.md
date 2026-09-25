# KISSAN SATHI — Final Demo

This folder contains the final KISSAN SATHI demo application.

## Easiest way on Windows

1. Install Node.js 20 or newer.
2. Double-click **RUN-KISSAN-SATHI.bat**.
3. Wait for the first-time package installation.
4. Open **http://localhost:5173**.

Or open a terminal in this folder and run:

```bash
npm run dev
```

## Demo journey

**Open the selling desk → Farmer desk → Sell Crop → Details → Prices → Buyers → Profit → Deal**

The deeper farmer and buyer pages remain available from the side menu.

## Demo boundary

This release uses sample/demo market, buyer, transport, forecast and payment information. Payments are simulated and forecasts are estimates.

PostgreSQL and the separate AI service are not required for the normal local demo launcher.

## SIH demo feature set
The current prototype demonstrates the expanded SIH workflow with: mobile/PWA experience, demo Aadhaar verification, competitive bidding, small-farmer polling, FPO connection, help desk, farmer instruction guide, browser voice-assistant demo, weather-risk map, global search, minimum/reference-price guardrails, and tractor/truck/rail transport comparison. External integrations such as real Aadhaar/UIDAI authentication, live market feeds, real payments and production AI services are not claimed as live in this local demo.


### Weather route view
The weather dashboard uses a lightweight India-only map with the selected route rendered in the same coordinate system as the map, so the route does not drift when selections change. The map is local UI/data and is intended as a demo route planner, not live turn-by-turn navigation.

## Weather map note
The weather dashboard now uses Leaflet with OpenStreetMap tiles. The selected route is drawn in geographic coordinates, so it stays attached to the map when you pan or zoom. Route distances, corridor points, weather and transport figures are demo/modelled values, not live navigation data. An internet connection is required for the map tiles.


## Latest UI polish
- Sidebar language selector and sign-out are full-width clickable controls.
- Global search is widened.
- Floating Kissan Sathi AI helper is available on farmer and buyer portals with role-aware quick questions and a small chat panel.
