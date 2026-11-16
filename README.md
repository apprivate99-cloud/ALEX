# Nearby — restaurants & bars near you

A static website that finds the best restaurants, bars and pubs around the visitor's GPS location and lets them book directly on each business's own website.

## Features
- **GPS location** (“Use my location”) with a fallback search by town or postcode.
- **Map + ranked list**: numbered pins and cards, filter by Restaurants / Bars & pubs, radius (500 m–5 km), cuisine/name text filter, and “Bookable online” toggle.
- **Best-match ranking**: OpenStreetMap has no star ratings, so venues are scored on quality signals — notable/listed venues, independents over chains, takes reservations, has a website, published opening hours, cuisine info — with a small distance penalty. Sort by nearest or A–Z is also available.
- **Book a table**: opens the venue’s own reservation page (`reservation:url`) or website in a new tab. Venues with no listed site get a “Find booking site” web-search link.
- Details panel with address, phone, opening hours (“Open now”), booking policy, features and directions.

## Running it
No build step and no API keys. Serve the folder over HTTPS (browsers only allow GPS on `https://` or `localhost`):

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

To publish, push to any static host — GitHub Pages, Netlify, Vercel, Cloudflare Pages.

## Data sources
- Venues: [OpenStreetMap](https://www.openstreetmap.org/copyright) via the public Overpass API (with fallback mirrors).
- Place search: Nominatim. Map tiles: OpenStreetMap.

These public services are free but rate-limited. For heavy traffic, or to show real star ratings and reviews, swap the data layer in `js/app.js` (`fetchOverpass` / `normalise`) for the Google Places API or Yelp Fusion API (both need an API key and a small server-side proxy to keep the key private).
