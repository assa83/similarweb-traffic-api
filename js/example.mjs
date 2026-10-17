// Similarweb traffic for a few domains.
// Usage: node example.mjs notion.so clickup.com
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('Set APIFY_TOKEN first: https://console.apify.com/settings/integrations');
    process.exit(1);
}

const domains = process.argv.slice(2).length ? process.argv.slice(2) : ['apify.com', 'openai.com'];
const client = new ApifyClient({ token });
const run = await client.actor('lagenuina_agency/similarweb-scraper').call({ domains });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const it of items) {
    console.log(`${it.domain}: ${it.status}, ${it.totalVisits} visits, global rank ${it.globalRank}, bounce ${it.bounceRatePct}%`);
    for (const c of it.topCountries ?? []) console.log(`  ${c.countryCode}: ${(c.share * 100).toFixed(1)}% (${c.estimatedVisits} visits)`);
}
