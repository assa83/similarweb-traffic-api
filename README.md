# Similarweb API alternative – website traffic in Python, JavaScript and n8n

Get **Similarweb website traffic** data for any list of domains as clean JSON: monthly visits (3-month history), global / country / category rank, bounce rate, pages per visit, visit duration, traffic sources (incl. AI chatbots), top countries with estimated visits, top organic keywords with volume and CPC, and AI referral traffic.

Powered by the [Similarweb Website Traffic Scraper](https://apify.com/lagenuina_agency/similarweb-scraper) actor on Apify. No Similarweb account, no API key from Similarweb, no browser.

## Example output (real result, shortened)

```json
{
  "status": "ok",
  "domain": "apify.com",
  "snapshotDate": "2026-09-01T00:00:00+00:00",
  "globalRank": 9800,
  "countryRank": { "Country": 840, "CountryCode": "US", "Rank": 9730 },
  "estimatedMonthlyVisits": { "2026-07-01": 4490242, "2026-08-01": 4201537, "2026-09-01": 3990936 },
  "totalVisits": 3990936,
  "bounceRatePct": 35.95,
  "pagesPerVisitNum": 7.61,
  "avgVisitDurationSec": 317.5,
  "topCountries": [{ "countryCode": "US", "share": 0.221, "estimatedVisits": 882384 }],
  "trafficSources": { "Direct": 0.4396, "Search": 0.3966, "Referrals": 0.0581, "Social": 0.0505, "Mail": 0.0153, "Paid Referrals": 0.0058 },
  "topKeywords": [{ "name": "apify", "volume": 798490, "estimatedValue": 888360, "cpc": 1.56 }],
  "aiTraffic": { "totalVisits": 123427.65, "chatbots": [{ "name": "chatgpt.com", "sharePct": 66.9 }] }
}
```

## Quickstart (3 steps)

1. Create a free Apify account and copy your API token from [Settings → Integrations](https://console.apify.com/settings/integrations).
2. Put it in an environment variable (never in code): `export APIFY_TOKEN=your_token`
3. Run the example:

```bash
pip install -r python/requirements.txt
python python/example.py notion.so clickup.com asana.com
```

JavaScript: `cd js && npm install && node example.mjs notion.so clickup.com`

## Examples

**Python** (`pip install "apify-client<2"`)

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("lagenuina_agency/similarweb-scraper").call(run_input={"domains": ["apify.com", "openai.com"]})
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item["domain"], item.get("totalVisits"), item.get("globalRank"))
```

**JavaScript / Node.js** (`npm install apify-client`)

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('lagenuina_agency/similarweb-scraper').call({ domains: ['apify.com', 'openai.com'] });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

**cURL / any language** – one HTTP call, results in the response:

```bash
curl -X POST "https://api.apify.com/v2/acts/lagenuina_agency~similarweb-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"domains": ["apify.com", "openai.com"]}'
```

All input fields are documented on the [actor page](https://apify.com/lagenuina_agency/similarweb-scraper) (Input tab).

## Use case: competitor traffic report to CSV / Google Sheets

`python/example.py` fetches your competitors and writes one row per domain (`similarweb_<date>.csv`): month, visits, global rank, top country, bounce rate, pages per visit, visit duration, channel shares and AI-referred visits. Import it in Google Sheets, or let the n8n workflow append the rows every month.

## n8n workflow

[`n8n/workflow.json`](n8n/workflow.json): on the 15th of every month at 08:00 → run the actor → one row per domain → append to Google Sheets.

1. In n8n: **Workflows → Import from File** and pick `n8n/workflow.json`.
2. Create a **Header Auth** credential named `Apify API token` with name `Authorization` and value `Bearer <your token>`, and select it in the *Run Apify actor* node.
3. Edit the domains in the JSON body, set your Google Sheet ID and activate.

The `run-sync-get-dataset-items` endpoint waits up to 300 s (thousands of domains fit); for bigger runs use `/runs` plus a webhook.

## Use with AI agents (MCP)

Give Claude, ChatGPT, Cursor or any MCP client this actor as a tool:

```json
{
  "mcpServers": {
    "similarweb-scraper": {
      "url": "https://mcp.apify.com/?actors=lagenuina_agency/similarweb-scraper"
    }
  }
}
```

Sign in with Apify OAuth when asked, or send `Authorization: Bearer <APIFY_TOKEN>`.

## Pricing

$2.40 per 1,000 domains on the Apify Free plan, $0.94 on Bronze and above, platform usage included, no start fee, failed domains free – see [lagenuina_agency/similarweb-scraper](https://apify.com/lagenuina_agency/similarweb-scraper).

## More competitor research tools

- [Google Ads Transparency Scraper](https://apify.com/lagenuina_agency/google-ads-transparency-scraper): the ads your competitors run on Google.
- [Google Trends Scraper](https://apify.com/lagenuina_agency/google-trends-scraper): how search interest for their brand moves.

## Disclaimer

Independent, not affiliated with or endorsed by Similarweb Ltd. It reads only publicly available, aggregated estimates. Use it in line with the applicable terms and laws.

## License

[MIT](LICENSE) © Quelli di Carne Genuina
