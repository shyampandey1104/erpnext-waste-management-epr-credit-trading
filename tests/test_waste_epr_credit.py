import unittest
from waste_epr_credit.engine import PIBOObligation, RecyclingCertificate, EPRCreditTradingEngine

class TestEPRCreditTradingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = EPRCreditTradingEngine()
        self.ob = PIBOObligation(
            brand_owner_name="OmniBeverages India Pvt Ltd", cpcb_reg_no="CPCB/EPR/2026/BO/0091",
            target_year="2025-2026", category_1_rigid_kg=50000.0, category_2_flexible_kg=30000.0,
            category_3_multilayer_kg=20000.0, category_4_compostable_kg=5000.0
        )
        self.engine.set_pibo_obligation(self.ob)

    def test_certificate_trading_and_fulfillment(self):
        cert = RecyclingCertificate(
            cert_id="CERT-RECY-DEL-001", recycler_cpcb_id="RECY/DEL/441",
            category="CAT_1", verified_quantity_kg=50000.0, unit_credit_price_inr=4.50
        )
        self.engine.register_recycler_certificate(cert)
        
        trade = self.engine.execute_credit_trade(
            cpcb_reg_no="CPCB/EPR/2026/BO/0091", cert_id="CERT-RECY-DEL-001", purchase_qty_kg=50000.0
        )
        self.assertEqual(trade["traded_qty_kg"], 50000.0)
        self.assertEqual(trade["total_consideration_inr"], 225000.0)
        self.assertEqual(self.ob.fulfilled_cat1_kg, 50000.0)

    def test_annual_return_compliance(self):
        ret = self.engine.generate_cpcb_annual_return("CPCB/EPR/2026/BO/0091")
        self.assertIn("compliance_percentage", ret)
        self.assertEqual(ret["brand_owner_name"], "OmniBeverages India Pvt Ltd")

if __name__ == "__main__":
    unittest.main()
