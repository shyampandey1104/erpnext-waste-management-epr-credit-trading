# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "waste_epr_credit"
app_title = "Erpnext Waste Management Epr Credit Trading"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Waste Management Epr Credit Trading - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/waste_epr_credit/css/waste_epr_credit.bundle.css"
app_include_js = "/assets/waste_epr_credit/js/waste_epr_credit.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Erpnext Waste Management Epr Credit Trading Entry": {
        "validate": "waste_epr_credit.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "waste_epr_credit.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "waste_epr_credit.tasks.hourly_sync"
    ],
    "daily": [
        "waste_epr_credit.tasks.daily_reconciliation"
    ],
    "weekly": [
        "waste_epr_credit.tasks.weekly_digest"
    ]
}
