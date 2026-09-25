evaluation_dataset = [

    {
        "question": "When will my shipment arrive?",

        "expected_sections": [
            "2. Shipment Processing and Handling Times",
            "3. Domestic Shipping Options and Delivery Rates"
        ],

        "expected_answer":
            "Standard orders are processed within 1 to 2 business days. "
            "Standard shipping takes 3 to 5 business days, "
            "Two-Day Expedited takes 2 business days, "
            "and Overnight Delivery takes 1 business day."
    },

    {
        "question": "What shipping options do you offer?",

        "expected_sections": [
            "3. Domestic Shipping Options and Delivery Rates"
        ],

        "expected_answer":
            "We offer Standard Shipping, Two-Day Expedited, and Overnight Delivery. "
            "Standard Shipping takes 3 to 5 business days, "
            "Two-Day Expedited takes 2 business days, "
            "and Overnight Delivery takes 1 business day."
    },

    {
        "question": "Can I change my shipping address?",

        "expected_sections": [
            "7. Order Modifications and Cancellations"
        ],

        "expected_answer":
            "Address modifications are only guaranteed if requested within "
            "60 minutes of the original checkout timestamp. "
            "Once a tracking number has been generated, the package cannot "
            "be intercepted or modified in transit."
    },

    {
        "question": "What happens if my package is damaged?",

        "expected_sections": [
            "6. Lost, Stolen, or Damaged Shipments"
        ],

        "expected_answer":
            "For packages damaged in transit, take photographs of the damaged "
            "outer packaging and individual items immediately. "
            "File a claim through the portal or contact support within 48 hours "
            "of receipt to initiate an expedited replacement shipment."
    },

    {
        "question": "Can I ship to a P.O. Box?",

        "expected_sections": [
            "4. Delivery to P.O. Boxes and Military Addresses"
        ],

        "expected_answer":
            "Yes. Shipments to P.O. Boxes can be handled via USPS. "
            "Premium expedited tiers, including Two-Day and Overnight, "
            "are not available for P.O. Box destinations."
    },

    {
        "question": "Are expedited options available for military addresses?",

        "expected_sections": [
            "4. Delivery to P.O. Boxes and Military Addresses"
        ],

        "expected_answer":
            "No. Premium expedited tiers, including Two-Day and Overnight, "
            "are not available for military addresses. "
            "Shipments to APO, FPO, or DPO addresses can only be handled via USPS."
    },

    {
        "question": "Do you deliver to Canada?",

        "expected_sections": []
    },

    {
        "question": "What payment methods do you accept?",

        "expected_sections": []
    }
]