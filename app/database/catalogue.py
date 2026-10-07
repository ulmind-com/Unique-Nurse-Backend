"""Canonical service catalogue for Unique Nurse and Aya Services.

Single source of truth for the eight service categories the business offers
and the individual services inside each one. Consumed by ``seed_site.py``.
"""

from __future__ import annotations

from typing import Dict, List

BRAND_NAME = "Unique Nurse and Aya Services"
BRAND_PHONE = "+919432941098"
BRAND_PHONE_DISPLAY = "+91 94329 41098"
BRAND_WHATSAPP = "919432941098"
BRAND_ADDRESS = (
    "3, Anukul Chandra Road, Tetulberia, Garia, Kolkata - 700084"
)

CATALOGUE: List[Dict] = [
    {
        "name": "Home Nursing Services",
        "slug": "home-nursing-services",
        "icon": "Stethoscope",
        "description": (
            "Trained nurses at your doorstep for injections, wound dressing, "
            "post-operative recovery and round-the-clock patient monitoring."
        ),
        "hero_badge": "Qualified Nurses",
        "hero_title": "Professional Home Nursing Care",
        "hero_description": (
            "GNM and ANM qualified nurses who bring hospital-standard clinical "
            "care into your home — safely, patiently and on your schedule."
        ),
        "services": [
            ("Trained Nurse / Nursing Care", "Certified GNM & ANM nurses for clinical care at home."),
            ("Home Nursing Support", "Day or night nursing support tailored to the patient's condition."),
            ("Post-Hospital Care", "Structured recovery care after surgery or hospital discharge."),
            ("Patient Monitoring & Daily Care", "Vitals tracking, medication schedules and daily care routines."),
        ],
    },
    {
        "name": "Patient Care & Attendant Services",
        "slug": "patient-care-attendant-services",
        "icon": "HeartHandshake",
        "description": (
            "Male and female attendants for bedridden, recovering and "
            "long-term patients — at home or in hospital."
        ),
        "hero_badge": "Male & Female Attendants",
        "hero_title": "Dependable Patient Attendant Services",
        "hero_description": (
            "Verified attendants who handle feeding, mobility, hygiene and "
            "bedside support with dignity, on day or night shifts."
        ),
        "services": [
            ("Male & Female Patient Attendants", "Choose the attendant the family is most comfortable with."),
            ("Bedridden Patient Care", "Position changes, bedsore prevention and full bedside assistance."),
            ("Personal Care Assistance", "Bathing, grooming, dressing and toileting support."),
            ("Hospital & Home Patient Care", "The same attendant can support you in hospital and at home."),
            ("Day / Night Shift Attendant", "8, 12 or 24-hour shifts with reliable replacements."),
        ],
    },
    {
        "name": "Elder Care & Senior Citizen Assistance",
        "slug": "elder-care-senior-citizen-assistance",
        "icon": "Users",
        "description": (
            "Companionship, daily assistance and health supervision for "
            "senior citizens living at home."
        ),
        "hero_badge": "Senior Citizen Care",
        "hero_title": "Warm, Respectful Elder Care at Home",
        "hero_description": (
            "Patient caregivers who help with medicines, meals, movement and "
            "company — so elders stay independent in their own home."
        ),
        "services": [
            ("Elderly Care at Home", "Full-time or part-time caregivers for seniors at home."),
            ("Senior Citizen Assistance", "Help with daily routines, walks, meals and medication."),
            ("Doctor Visit Assistance", "Accompanied doctor visits with reports and prescriptions handled."),
            ("Daily Check-in & Support", "Scheduled visits to check on elders living alone."),
            ("Hospital Visit Assistance", "End-to-end support for hospital appointments and tests."),
        ],
    },
    {
        "name": "Hospital Escort & Assistance",
        "slug": "hospital-escort-assistance",
        "icon": "Building2",
        "description": (
            "A trained escort who handles admission, tests, discharge and "
            "family coordination so nobody has to take the day off."
        ),
        "hero_badge": "Hospital Support",
        "hero_title": "Hospital Escort & Coordination",
        "hero_description": (
            "From admission paperwork to discharge summaries, our escorts stay "
            "with the patient and keep the family updated throughout."
        ),
        "services": [
            ("Hospital Escort", "A responsible escort accompanies the patient throughout."),
            ("Hospital Admission Assistance", "Paperwork, formalities and ward coordination handled."),
            ("Doctor Visit Assistance", "Queue management, consultation notes and follow-up reminders."),
            ("Diagnostic Test Visit Assistance", "Support for scans, blood work and report collection."),
            ("Hospital Discharge Assistance", "Billing, medicines and safe transfer back home."),
            ("Family Updates & Coordination", "Regular calls and updates to family members."),
        ],
    },
    {
        "name": "Baby & Newborn Care",
        "slug": "baby-newborn-care",
        "icon": "Baby",
        "description": (
            "Experienced newborn caregivers supporting mothers through "
            "feeding, hygiene and the first months at home."
        ),
        "hero_badge": "Mother & Baby",
        "hero_title": "Gentle Newborn & Baby Care",
        "hero_description": (
            "Trained baby caregivers and Japa support to help new mothers rest, "
            "recover and settle into a routine with confidence."
        ),
        "services": [
            ("Newborn Baby Care", "Specialised care for babies in their first months."),
            ("Baby Care & Assistance", "Daily bathing, massage, sleep routines and supervision."),
            ("Feeding & Burping Assistance", "Support with feeding schedules and safe burping."),
            ("Diaper Changing & Hygiene Care", "Hygiene, nappy changes and rash prevention."),
            ("Mother & Baby Support", "Postnatal support for the mother alongside baby care."),
        ],
    },
    {
        "name": "Aya Services",
        "slug": "aya-services",
        "icon": "UserRound",
        "description": (
            "Male and female Aya for patients, elders and hospital duty — "
            "hourly, daily or long-term."
        ),
        "hero_badge": "Male & Female Aya",
        "hero_title": "Trusted Aya Services in Kolkata",
        "hero_description": (
            "Background-verified Aya for home and hospital duty, available on "
            "flexible shifts with quick replacement if plans change."
        ),
        "services": [
            ("Male & Female Aya", "Pick the Aya that suits the patient and family."),
            ("Patient Aya", "Bedside care, feeding and mobility support for patients."),
            ("Elder Care Aya", "Daily assistance and companionship for senior citizens."),
            ("Hospital Aya", "Full-shift Aya duty inside hospitals and nursing homes."),
            ("Home Care Aya", "Live-in or shift-based Aya for care at home."),
        ],
    },
    {
        "name": "House Maid & Domestic Help",
        "slug": "house-maid-domestic-help",
        "icon": "Home",
        "description": (
            "Full-time and part-time maids for cleaning, cooking and everyday "
            "household work."
        ),
        "hero_badge": "Verified Household Staff",
        "hero_title": "House Maid & Domestic Help",
        "hero_description": (
            "Reliable, verified household help placed quickly — for cooking, "
            "cleaning and the daily running of your home."
        ),
        "services": [
            ("Full-Time Maid", "Live-in or full-day maid for complete household work."),
            ("Part-Time Maid", "Fixed-hour help for specific daily tasks."),
            ("House Cleaning", "Sweeping, mopping, dusting and bathroom cleaning."),
            ("Cooking Assistance", "Daily meal preparation to your family's taste."),
            ("Utensil Washing", "Kitchen clean-up and utensil washing."),
            ("General Household Work", "Laundry, organising and everyday chores."),
        ],
    },
    {
        "name": "Housekeeping Services",
        "slug": "housekeeping-services",
        "icon": "Sparkles",
        "description": (
            "Trained housekeeping staff for homes, hospitals and nursing "
            "homes, with hygiene-first cleaning routines."
        ),
        "hero_badge": "Home & Hospital",
        "hero_title": "Professional Housekeeping Services",
        "hero_description": (
            "Uniformed housekeeping teams for residences, hospitals and "
            "nursing homes — consistent standards, supervised daily."
        ),
        "services": [
            ("Home Housekeeping", "Scheduled deep cleaning and upkeep for residences."),
            ("Hospital / Nursing Home Housekeeping", "Hygiene-compliant cleaning for clinical spaces."),
            ("Cleaning & Maintenance Support", "Ongoing cleaning and light maintenance staff."),
        ],
    },
]
