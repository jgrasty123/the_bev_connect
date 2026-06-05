THE BEV CONNECT — multi-page lead-capture site
================================================

PAGES
  index.html         Home (3PL-first hero, services, rate-sheet capture, FAQ)
  fulfillment.html   Full 3PL capabilities + rate comparison table
  rate-sheet.html    Email-gated rate sheet download (lead magnet)
  marketing.html     Marketing services (demoted sub-page) + tiers
  book-a-call.html   Calendly embed + fallback lead form
  thank-you.html     Post-submission landing page
  assets/            style.css, main.js, downloads/the-bev-connect-rate-sheet.pdf


=====================================================================
DEPLOY (easiest path — Netlify, ~2 minutes, free, no command line)
=====================================================================
1. Go to https://app.netlify.com/drop
2. Drag this ENTIRE folder onto the page. It goes live instantly on a
   temporary URL (e.g. random-name.netlify.app).
3. In Netlify: Site settings > Domain management > add thebevconnect.com.
   Netlify gives you DNS records / nameservers to point your domain at.
   (Free SSL is automatic.)
4. Forms just work — see below.

To redeploy after edits: drag the folder onto Netlify again, OR connect
a GitHub repo for auto-deploys on push.


=====================================================================
LEAD FORMS  (already wired — work the moment you deploy to Netlify)
=====================================================================
Every form uses Netlify Forms (data-netlify="true"). After deploy:
  - Submissions appear in Netlify dashboard > Forms
  - Turn on email notifications: Forms > Settings > Form notifications
    > add your email. You'll get every lead in your inbox.
There are 3 forms: "rate-sheet", "rate-sheet-page", "book-a-call".

DELIVERING THE PDF AUTOMATICALLY:
Netlify Forms doesn't auto-email an attachment. Two options:
  A) Simple: the thank-you page can link the PDF directly. (Add a
     "Download now" button pointing to
     /assets/downloads/the-bev-connect-rate-sheet.pdf — tell me and
     I'll wire it.)
  B) Automated email: connect the form to Zapier/Make (Netlify has a
     native Zapier hook) and have it send the PDF on each submission.


=====================================================================
CALENDLY (book-a-call page)
=====================================================================
Open book-a-call.html and find this line:
   data-url="https://calendly.com/YOUR-CALENDLY-HANDLE/discovery-call"
Replace with your real Calendly event link. That's it — the scheduler
renders inline. Until you do, the lead form beside it still captures calls.


=====================================================================
EASY EDITS
=====================================================================
- Colors/fonts: assets/style.css (top :root block — change --red etc.)
- Email address: search/replace hello@thebevconnect.com across files
- Client logos/social proof: not added yet (you're confirming permission).
  Send me the go-ahead + names and I'll add a logo strip to the homepage.
