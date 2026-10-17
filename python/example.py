"""Competitor traffic report: Similarweb visits, rank, channels and top countries to CSV.

Usage: python example.py notion.so clickup.com asana.com
"""
import csv
import datetime
import os
import sys

from apify_client import ApifyClient

ACTOR = "lagenuina_agency/similarweb-scraper"
TOKEN = os.environ.get("APIFY_TOKEN")
if not TOKEN:
    sys.exit("Set APIFY_TOKEN first: https://console.apify.com/settings/integrations")


def main():
    domains = sys.argv[1:] or ["apify.com", "openai.com"]
    client = ApifyClient(TOKEN)
    run = client.actor(ACTOR).call(run_input={"domains": domains})
    items = client.dataset(run["defaultDatasetId"]).list_items().items

    out = f"similarweb_{datetime.date.today().isoformat()}.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["domain", "status", "month", "visits", "globalRank", "topCountry", "bounceRatePct",
                    "pagesPerVisit", "visitDurationSec", "direct", "search", "social", "referrals", "aiVisits"])
        for it in items:
            ts = it.get("trafficSources") or {}
            top = (it.get("topCountries") or [{}])[0]
            w.writerow([it["domain"], it["status"], (it.get("snapshotDate") or "")[:7], it.get("totalVisits"),
                        it.get("globalRank"), top.get("countryCode"), it.get("bounceRatePct"),
                        it.get("pagesPerVisitNum"), it.get("avgVisitDurationSec"), ts.get("Direct"), ts.get("Search"),
                        ts.get("Social"), ts.get("Referrals"), (it.get("aiTraffic") or {}).get("totalVisits")])
            print(f'{it["domain"]:<25} {it["status"]:<8} visits={it.get("totalVisits")} rank={it.get("globalRank")}')
    print(f"{len(items)} domains -> {out}")


if __name__ == "__main__":
    main()
