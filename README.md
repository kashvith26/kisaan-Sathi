# 🌾 KISSAN SATHI

### AI-Assisted Farmer–Buyer Platform for Smarter Agricultural Decisions

**KISSAN SATHI** is a full-stack SIH prototype designed to help farmers make better decisions around crop selling, buyer discovery, transport, weather, dairy operations, and farmer support — all from one platform.

## 🚀 Live Demo

**Web App:**  
https://kisaan-sathi-wg3m.vercel.app

**GitHub:**  
https://github.com/kashvith26/kisaan-Sathi

> This is an SIH demonstration prototype. Several market, buyer, transport, weather, dairy, payment, and advisory values are demo/modelled data unless explicitly stated otherwise.

---
## 🔑 Demo Accounts

### Farmer
```text
Email: farmer@kisansathi.demo
Password: demo1234
### Buyer
Email: buyer@kisansathi.demo
Password: demo1234
## 🎯 What KISSAN SATHI Does

KISSAN SATHI connects the major steps of a farmer's decision journey:

**Produce → Understand Market → Find Buyers → Compare Options → Calculate Profit → Plan Transport → Complete Deal**

It also provides dedicated workflows for **dairy farmers** and **agricultural buyers**.

---

## 👨‍🌾 Farmer Portal

The Farmer Portal provides:

- 🌱 Crop selling workflow
- 📊 Market-price comparison
- 🤝 Buyer discovery and matching
- 💰 Profit and transport calculations
- 🚚 Tractor / truck / rail transport comparison
- 🌦️ Weather and route-risk information
- 📦 Storage and transport planning
- 🧑‍🌾 Farmer help desk and guidance
- 🔎 Global search
- 🎤 Browser-based voice assistant
- 🤖 Role-aware AI assistant
- 🌐 Multi-language interface
- 🔐 Demo Aadhaar-verification workflow
- 💾 Remember Me login

---

## 🐄 Dairy Farmer Support

Dairy farmers are supported **inside the Farmer Portal**.

Features include:

- 🥛 Milk collection planning
- 💹 Indicative milk-rate comparison
- 🧪 Fat and SNF quality information
- 🚚 Milk pickup and transport planning
- 🤝 Milk buyer discovery
- 📍 Buyer location and collection details
- 🕐 Pickup timing
- 💳 Payment-cycle information

### Milk Buyer Connection

Farmers can view milk buyers with information such as:

- Buyer name
- Location
- Indicative milk rate
- Daily milk requirement
- Minimum fat requirement
- Minimum SNF requirement
- Pickup window
- Payment cycle
- Verification/demo status

> Milk procurement figures shown in the prototype are demonstration values and are not guaranteed live offers.

---

## 🏢 Buyer Portal

The Buyer Portal supports agricultural sourcing and procurement workflows.

### Features

- Farmer / supplier discovery
- Competitive bidding workflow
- Crop sourcing
- Buyer requirements
- Transport planning
- Weather support
- AI assistant

### 🥛 Milk Requirements

Dairy buyers can publish milk requirements including:

- Required litres per day
- Minimum fat %
- Minimum SNF %
- Collection location
- Collection time window
- Other sourcing conditions

These requirements are demonstrated as part of the prototype workflow.

---

## 📰 Farmer Community

KISSAN SATHI includes a dedicated **Community** section for farmers.

It provides a curated feed covering:

- Agriculture updates
- Farmer-focused developments
- Dairy and livestock topics
- Agricultural technology
- Climate and farming-related information
- Farmer livelihood and diversification

The Community section is available from both the **main page** and **Farmer Portal**.

> The current news feed is a curated prototype snapshot, not a guaranteed live government news service.

---

## 🤖 AI & Voice Assistance

KISSAN SATHI includes a floating AI helper for both farmers and buyers.

It supports:

- Role-aware quick questions
- Contextual assistance
- Text chat
- Browser voice input where supported
- Voice/audio responses where supported

The assistant is designed to provide simple, farmer-friendly guidance during the workflow.

---

## 🌦️ Weather & Route Planning

The weather dashboard uses **Leaflet + OpenStreetMap**.

The selected route is displayed using geographic coordinates so that it stays aligned with the map during panning and zooming.

> Weather values, route distances, corridor points, and transport figures are demo/modelled values and are not live navigation data.

**Internet access is required for OpenStreetMap map tiles.**

---

## 🧪 SIH Demo Scope

The prototype demonstrates:

- Mobile/PWA-style interface
- Demo Aadhaar verification
- Competitive bidding
- Small-farmer polling
- FPO connection workflow
- Farmer help desk
- Farmer instruction guide
- AI assistant
- Browser voice assistant
- Weather-risk mapping
- Global search
- Minimum/reference-price guardrails
- Transport comparison
- Dairy farmer workflows
- Milk-buyer requirements
- Farmer Community
- Buyer Portal

---

## ⚠️ Demo Boundary

The following are **not claimed as live production integrations**:

- Real Aadhaar / UIDAI authentication
- Guaranteed live market feeds
- Real payment processing
- Production-grade AI/ML guarantees
- Live turn-by-turn navigation
- Guaranteed live buyer procurement offers
- Guaranteed live agricultural news feeds

Where live integrations are unavailable, the prototype uses **sample, simulated, or modelled data**.

---

## 🏗️ Tech Stack

### Frontend
- React
- TypeScript
- Vite
- Leaflet
- Responsive/PWA-style UI

### Backend
- Node.js
- Express
- TypeScript
- JWT authentication
- PostgreSQL connectivity

### AI Service
- Python
- FastAPI

### Database
- PostgreSQL

### Deployment
- **Vercel** → Frontend
- **Render** → Express API
- **Render** → AI Service
- **Render PostgreSQL** → Database

---

```markdown
## 💻 Local Setup

### Local Services
Frontend   → http://localhost:5173
API        → http://localhost:4000
AI Service → http://localhost:8000
### Prerequisites

- Node.js 20+
- npm
- Python 3.x (only if running the AI service locally)

### Run

```bash
npm install
npm run dev
## 📁 Project Structure

```text
KissanSaathi/
├── client/       # React + Vite frontend
├── server/       # Express + TypeScript API
├── ai-service/   # FastAPI AI service
├── database/     # PostgreSQL schema/assets
├── docs/         # Documentation
├── scripts/      # Build/helper scripts
└── README.md
