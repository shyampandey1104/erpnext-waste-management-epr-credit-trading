"""Extended Producer Responsibility (EPR) CPCB Compliance & Credit Trading Engine."""
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Any, Optional

@dataclass
class PIBOObligation:
    brand_owner_name: str
    cpcb_reg_no: str
    target_year: str
    category_1_rigid_kg: float       # Cat I: Rigid plastic packaging
    category_2_flexible_kg: float    # Cat II: Single layer/flexible plastic
    category_3_multilayer_kg: float  # Cat III: Multi-layered plastic packaging
    category_4_compostable_kg: float # Cat IV: Compostable plastics
    fulfilled_cat1_kg: float = 0.0
    fulfilled_cat2_kg: float = 0.0
    fulfilled_cat3_kg: float = 0.0
    fulfilled_cat4_kg: float = 0.0

@dataclass
class RecyclingCertificate:
    cert_id: str
    recycler_cpcb_id: str
    category: str  # CAT_1, CAT_2, CAT_3, CAT_4
    verified_quantity_kg: float
    unit_credit_price_inr: float
    status: str = "AVAILABLE"  # AVAILABLE, RESERVED, TRADED, RETIRED

class EPRCreditTradingEngine:
    def __init__(self):
        self.obligations: Dict[str, PIBOObligation] = {}
        self.certificates: Dict[str, RecyclingCertificate] = {}
        self.trades: List[Dict[str, Any]] = []

    def set_pibo_obligation(self, ob: PIBOObligation) -> Dict[str, Any]:
        self.obligations[ob.cpcb_reg_no] = ob
        total_target = ob.category_1_rigid_kg + ob.category_2_flexible_kg + ob.category_3_multilayer_kg + ob.category_4_compostable_kg
        return {"cpcb_reg_no": ob.cpcb_reg_no, "total_target_kg": total_target}

    def register_recycler_certificate(self, cert: RecyclingCertificate) -> Dict[str, Any]:
        self.certificates[cert.cert_id] = cert
        return {"cert_id": cert.cert_id, "category": cert.category, "quantity_kg": cert.verified_quantity_kg}

    def execute_credit_trade(self, cpcb_reg_no: str, cert_id: str, purchase_qty_kg: float) -> Dict[str, Any]:
        if cpcb_reg_no not in self.obligations:
            raise ValueError(f"PIBO {cpcb_reg_no} not registered.")
        if cert_id not in self.certificates:
            raise ValueError(f"Certificate {cert_id} not found.")

        ob = self.obligations[cpcb_reg_no]
        cert = self.certificates[cert_id]

        if cert.status != "AVAILABLE":
            raise ValueError(f"Certificate {cert_id} is not available for trading.")
        if purchase_qty_kg > cert.verified_quantity_kg:
            raise ValueError(f"Requested qty {purchase_qty_kg} kg exceeds cert balance {cert.verified_quantity_kg} kg.")

        cost = round(purchase_qty_kg * cert.unit_credit_price_inr, 2)
        
        # Credit category fulfillment
        if cert.category == "CAT_1":
            ob.fulfilled_cat1_kg += purchase_qty_kg
        elif cert.category == "CAT_2":
            ob.fulfilled_cat2_kg += purchase_qty_kg
        elif cert.category == "CAT_3":
            ob.fulfilled_cat3_kg += purchase_qty_kg
        elif cert.category == "CAT_4":
            ob.fulfilled_cat4_kg += purchase_qty_kg

        cert.verified_quantity_kg -= purchase_qty_kg
        if cert.verified_quantity_kg <= 0:
            cert.status = "RETIRED"

        trade_record = {
            "trade_id": f"EPR-TRD-{len(self.trades) + 1:04d}",
            "cpcb_reg_no": cpcb_reg_no,
            "cert_id": cert_id,
            "category": cert.category,
            "traded_qty_kg": purchase_qty_kg,
            "total_consideration_inr": cost,
            "timestamp": datetime.now().isoformat()
        }
        self.trades.append(trade_record)
        return trade_record

    def generate_cpcb_annual_return(self, cpcb_reg_no: str) -> Dict[str, Any]:
        if cpcb_reg_no not in self.obligations:
            raise ValueError(f"PIBO {cpcb_reg_no} not registered.")
        ob = self.obligations[cpcb_reg_no]
        total_target = ob.category_1_rigid_kg + ob.category_2_flexible_kg + ob.category_3_multilayer_kg + ob.category_4_compostable_kg
        total_fulfilled = ob.fulfilled_cat1_kg + ob.fulfilled_cat2_kg + ob.fulfilled_cat3_kg + ob.fulfilled_cat4_kg
        compliance_pct = round((total_fulfilled / total_target * 100.0) if total_target > 0 else 100.0, 2)
        
        return {
            "brand_owner_name": ob.brand_owner_name,
            "cpcb_reg_no": ob.cpcb_reg_no,
            "target_year": ob.target_year,
            "total_obligation_kg": total_target,
            "total_fulfilled_kg": total_fulfilled,
            "compliance_percentage": compliance_pct,
            "status": "COMPLIANT" if compliance_pct >= 100.0 else "DEFICIT_LIABLE_FOR_ENVIRONMENTAL_COMPENSATION"
        }
