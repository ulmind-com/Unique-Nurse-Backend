"""Seed the Unique Nurse and Aya Services catalogue and brand settings.

Idempotent: run it as often as you like. Existing documents are updated in
place (matched on slug) rather than duplicated.

    python seed_site.py            # categories, services, website settings
    python seed_site.py --purge    # also delete catalogue docs not in the list
"""

from __future__ import annotations

import argparse
import asyncio

from slugify import slugify

from app.database.catalogue import (
    BRAND_ADDRESS,
    BRAND_NAME,
    BRAND_PHONE_DISPLAY,
    BRAND_WHATSAPP,
    CATALOGUE,
)
from app.database.connection import (
    close_mongo_connection,
    connect_to_mongo,
    init_database,
)
from app.models.enums import ContentStatus
from app.models.service import Category, Service
from app.models.settings import WebsiteSettings, WorkingHour

WORKING_HOURS = [
    WorkingHour(day=day, open_time="00:00", close_time="23:59")
    for day in (
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    )
]


async def seed_settings() -> None:
    """Create or update the singleton website-settings document."""
    doc = await WebsiteSettings.find_one({})
    values = {
        "website_name": BRAND_NAME,
        "tagline": "Nursing, Aya & Patient Care at Home in Kolkata",
        "phone": BRAND_PHONE_DISPLAY,
        "whatsapp": BRAND_WHATSAPP,
        "address": BRAND_ADDRESS,
        "working_hours": WORKING_HOURS,
        "about_address_name": BRAND_NAME,
        "about_address_line1": "3, Anukul Chandra Road, Tetulberia",
        "about_address_line2": "Garia, Kolkata - 700084",
    }
    if doc is None:
        await WebsiteSettings(**values).insert()
        print("settings: created")
        return
    for key, value in values.items():
        setattr(doc, key, value)
    await doc.save()
    print("settings: updated")


async def seed_catalogue(purge: bool = False) -> None:
    """Upsert every category and its services from the canonical catalogue."""
    seen_categories: list[str] = []
    seen_services: list[str] = []

    for order, entry in enumerate(CATALOGUE, start=1):
        seen_categories.append(entry["slug"])
        category = await Category.find_one({"slug": entry["slug"]})
        fields = {
            "name": entry["name"],
            "slug": entry["slug"],
            "description": entry["description"],
            "icon": entry["icon"],
            "hero_badge": entry["hero_badge"],
            "hero_title": entry["hero_title"],
            "hero_description": entry["hero_description"],
            "hero_cta_primary_text": "Book This Service",
            "hero_cta_secondary_text": "Talk to Us",
            "order": order,
            "is_active": True,
        }
        if category is None:
            category = Category(**fields)
            await category.insert()
            action = "created"
        else:
            for key, value in fields.items():
                setattr(category, key, value)
            await category.save()
            action = "updated"
        print(f"category {action}: {entry['name']}")

        for s_order, (title, short_description) in enumerate(entry["services"], start=1):
            slug = slugify(f"{title}-{entry['slug']}", max_length=90)
            seen_services.append(slug)
            s_fields = {
                "title": title,
                "slug": slug,
                "short_description": short_description,
                "description": short_description,
                "category_id": str(category.id),
                "category_name": entry["name"],
                "icon": entry["icon"],
                "order": s_order,
                "is_featured": s_order == 1,
                "status": ContentStatus.PUBLISHED,
            }
            service = await Service.find_one({"slug": slug})
            if service is None:
                await Service(**s_fields).insert()
            else:
                for key, value in s_fields.items():
                    setattr(service, key, value)
                await service.save()
        print(f"  → {len(entry['services'])} services synced")

    if purge:
        removed_c = await Category.find({"slug": {"$nin": seen_categories}}).delete()
        removed_s = await Service.find({"slug": {"$nin": seen_services}}).delete()
        print(
            "purged:",
            getattr(removed_c, "deleted_count", 0),
            "categories,",
            getattr(removed_s, "deleted_count", 0),
            "services",
        )


async def main(purge: bool) -> None:
    await connect_to_mongo()
    await init_database()
    try:
        await seed_settings()
        await seed_catalogue(purge=purge)
    finally:
        await close_mongo_connection()
    print("\nSeed complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--purge",
        action="store_true",
        help="delete categories/services that are not in the canonical catalogue",
    )
    args = parser.parse_args()
    asyncio.run(main(args.purge))
