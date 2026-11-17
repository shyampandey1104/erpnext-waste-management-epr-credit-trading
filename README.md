# ERPNext EPR Waste Management & CPCB Credit Trading Engine

[![Frappe Framework](https://img.shields.io/badge/Frappe-v15.x-blue.svg)](https://frappeframework.com/)
[![CPCB EPR Compliance](https://img.shields.io/badge/CPCB-EPR%20Rules%202022-green.svg)]()
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 📌 Executive Overview & Real-World Client Problem

Under the Ministry of Environment, Forest and Climate Change (MoEFCC) and **CPCB Plastic Waste Management Rules (2022 & 2024 amendments)**, every Producer, Importer, and Brand Owner (PIBO) must fulfill mandatory recycling quotas across four categories of plastic:
- **Category I:** Rigid plastic packaging
- **Category II:** Flexible single layer/multilayer with non-plastic layers
- **Category III:** Multi-layered plastic packaging
- **Category IV:** Compostable plastics

**The Enterprise Problem:**
Brand owners producing consumer packaged goods cannot directly collect their packaging back from retail shelves. They must purchase **verified recycling credits** from registered plastic waste recyclers via the CPCB portal. Missing these deadlines triggers **Environmental Compensation (EC) penalties** reaching ₹5,000 per metric ton.

This Frappe application automates packaging consumption calculations, PIBO obligation tracking, and secondary market recycling credit trading.

---

## 🏛️ System Architecture Flow

```mermaid
flowchart TD
    A["ERPNext Finished Goods Sales"] -->|BOM Packaging Weight Split| B["PIBO Annual Obligation Engine"]
    B -->|Calculate Obligation (Cat I, II, III, IV)| C["CPCB Target Matrix"]
    D["Registered Plastic Recyclers"] -->|Submit Processing Certificates| E["Recycling Certificate Vault"]
    C --> F{"Credit Trading Engine"}
    E --> F
    F -->|Bilateral Purchase Order| G["EPR Credit Settlement & Retirement"]
    G -->|Update Balance| H["CPCB Annual Return Generator"]
    H -->|File with MoEFCC| I["Zero Environmental Compensation (EC) Audit Status"]
```

---

## 🚀 Key Engineering Capabilities

- **BOM Packaging Explosion:** Dissects bill of materials (BOMs) into primary, secondary, and tertiary plastic packaging weights.
- **Categorical Quota Calculator:** Computes exact annual recycling obligations in kilograms across all 4 statutory CPCB categories.
- **Credit Trading Matching Engine:** Facilitates transparent trading between recyclers and brand owners, preventing double-counting through cryptographic certificate serial tracking.
- **CPCB Annual Return Exporter:** Auto-formats filing data ready for upload to the centralized CPCB EPR portal.

---

## 📂 Frappe DocType Schema & Data Structure

```text
waste_epr_credit/
├── waste_epr_credit_core/
│   ├── doctype/
│   │   ├── epr_credit_ledger/
│   │   │   ├── epr_credit_ledger.json
│   │   │   ├── epr_credit_ledger.py
│   │   │   └── epr_credit_ledger.js
│   │   └── pibo_obligation_master/
│   │       └── pibo_obligation_master.json
│   └── workspace/
│       └── waste_epr_credit_workspace/
│           └── waste_epr_credit_workspace.json
```

---

## ⚡ Frappe Hooks & Whitelisted APIs

- **REST Endpoint:** `POST /api/method/waste_epr_credit.api.execute_credit_trade`
- **Whitelisted Method:** `@frappe.whitelist() def generate_cpcb_annual_return(cpcb_reg_no)`
- **Hooks Event:** `on_submit` of `Sales Invoice` updates brand owner's real-time packaging consumption metrics.

---

## 🛠️ Installation & Bench Setup

```bash
bench get-app https://github.com/shyampandey1104/erpnext-waste-management-epr-credit-trading
bench --site erp.yourdomain.com install-app waste_epr_credit
bench --site erp.yourdomain.com migrate
python3 -m unittest discover tests
```

---

## 📄 License
MIT License. Built for FMCG giants, electronics manufacturers, and recycling aggregators.
