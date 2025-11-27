(function () {
  const placementData = {
    hero: {
      eyebrow: "Placement Intelligence",
      title: "Landscaping, Dumpster & Contractor partners built for speed, safety & scale.",
      intro:
        "Instead of scrolling through generic case studies, we rebuilt our results page to focus on the three placement specialties that drive the most momentum for our clients: landscaping crews, dumpster & waste partners, and contractor services.",
      detail:
        "Every placement below is a real scenario, anonymized for confidentiality, but engineered around the same demand signals we manage each week."
    },
    stats: [
      { value: "187%", label: "Avg. lift in qualified leads after placement refresh" },
      { value: "32", label: "Regional partners onboarded per quarter" },
      { value: "48 hrs", label: "Median time from intake to live launch" },
      { value: "93%", label: "Retention with landscaper + contractor cohorts" }
    ],
    sections: [
      {
        id: "landscaping",
        title: "Landscaping Placements",
        copy:
          "Seasonality hits hard, so we build pipelines that mix recurring commercial accounts with higher-margin residential installs.",
        cards: [
          {
            title: "GreenScape Pros",
            result: "+212% appointment volume / -37% cost per booked job",
            points: [
              "Localized landing hubs for HOA contracts",
              "Weather-triggered ad scheduling to maximize post-storm demand",
              "CRM sync to auto-route leads by crew availability"
            ]
          },
          {
            title: "TurfLink Collective",
            result: "4.8x lift in irrigation audits QoQ",
            points: [
              "Partnered with 9 nurseries for referral placements",
              "Ran native video in contractor Slack communities",
              "Live dashboard for franchise owners to monitor backlog"
            ]
          },
          {
            title: "ArborForce Solutions",
            result: "Within 6 weeks: 3 municipal pruning contracts secured",
            points: [
              "Bid calculator microsite with compliance-ready PDFs",
              "Call tracking per foreman to reward best closers",
              "Drone footage library packaged into sales enablement"
            ]
          }
        ]
      },
      {
        id: "dumpster",
        title: "Dumpster & Waste Services",
        copy:
          "Roll-off capacity is capital intensive, so we obsess over routing software, market-level pricing transparency, and frictionless bookings.",
        cards: [
          {
            title: "MetroBin Logistics",
            result: "+168% revenue from contractor accounts; 11% higher ARPU",
            points: [
              "Dynamic pricing widget tied to disposal fees by ZIP",
              "Integration with ServiceTitan to pre-fill PO numbers",
              "Always-on PMAX netting 14x ROAS on branded searches"
            ]
          },
          {
            title: "RollAway Pros",
            result: "Same-day delivery rate jumped from 62% to 91%",
            points: [
              "Dispatch board shows live truck GPS inside booking flow",
              "SMS follow-ups with photo proof → 4.9⭐ reviews",
              "Win-back placements for dormant roofing partners"
            ]
          },
          {
            title: "RapidHaul Industrial",
            result: "$480k in new recurring contracts across manufacturing plants",
            points: [
              "ABM motion toward EHS directors with LinkedIn + direct mail",
              "Customized sustainability scorecards for ESG reporting",
              "Quarterly utilization audits built into SOW"
            ]
          }
        ]
      },
      {
        id: "contractor",
        title: "Contractor & Trades Staffing",
        copy:
          "Electricians, framers, concrete crews—each discipline needs a different hook. We combine placement data with labor forecasts to keep benches full.",
        cards: [
          {
            title: "Hammer & Helm GC Network",
            result: "220 vetted subcontractors added; 83% accepted first job within 10 days",
            points: [
              "Launched compliance portal to upload COIs + certifications",
              "Podcast ads across trade radio + connected TV",
              "Referral bounties auto-paid via Stripe"
            ]
          },
          {
            title: "BrightWire Electrical",
            result: "Reduced hiring cost per journeyman to $312",
            points: [
              "Hands-on partnership with 5 technical colleges",
              "Interactive wage calculator to combat rate objections",
              "Geo-fenced TikTok + Meta ads during shift changes"
            ]
          },
          {
            title: "Apex Concrete Crew",
            result: "Secured 14 long-term placement agreements with national builders",
            points: [
              "Showcased pour timelines via timelapse reels",
              "Bid templates standardized for multi-state compliance",
              "BI layer flagged underperforming crews for retraining"
            ]
          }
        ]
      }
    ],
    processSteps: [
      {
        title: "Signal Sync",
        copy:
          "Audit intake, route-to-dispatch logic, backlog, and CPL caps. We surface which zip codes and services deserve priority."
      },
      {
        title: "Placement Kit",
        copy:
          "Rapid creative system—short-form video, rate cards, quote builders—designed specifically for the target trade."
      },
      {
        title: "Launch + Load",
        copy:
          "Paid + partner channels go live within 48 hours. Slack + SMS alerts keep ops teams aligned on every incoming lead."
      },
      {
        title: "Scale or Swap",
        copy:
          "Weekly retros highlight which placements to double down on, and where to spin up fresh crews or haulers."
      }
    ],
    cta: {
      title: "Need crews, cans, or contractors on deck?",
      copy: "Tell us the markets you care about and we’ll show you the exact placement mix we’d deploy in the first 30 days.",
      link: { href: "/contact/", label: "Schedule a Placement Review" }
    }
  };

  const viewConfigs = {
    default: {},
    "industry-health-wellness": {
      filterLabel: "Filter: Health + Wellness",
      heroIntro: "We bring the same operational rigor to health & wellness networks, from med spas to behavioral clinics."
    },
    "industry-home-services": {
      filterLabel: "Filter: Home Services",
      heroIntro: "From roofing to remodeling, these placement frameworks keep technicians booked and margins protected."
    },
    "industry-law": {
      filterLabel: "Filter: Legal",
      heroIntro: "We adapt these playbooks to intake-heavy legal teams that need compliant growth without wasting ad spend."
    },
    "industry-education": {
      filterLabel: "Filter: Education",
      heroIntro: "Enrollment teams leverage the same placement system to balance campus tours, digital programs, and partner pipelines."
    },
    "industry-e-commerce": {
      filterLabel: "Filter: E-Commerce",
      heroIntro: "Multi-location DTC brands apply these placements to stabilize fulfillment and feed high-intent cohorts back into CRM."
    },
    "industry-b2b": {
      filterLabel: "Filter: B2B",
      heroIntro: "Complex buying committees still respond to smart placements—these examples show how we orchestrate them."
    },
    "industry-travel": {
      filterLabel: "Filter: Travel & Hospitality",
      heroIntro: "Tour operators and boutique resorts plug into the same demand system to smooth shoulder seasons."
    }
  };

  function buildStats(stats) {
    return stats
      .map(
        (stat) => `
      <div class="stat-card">
        <h3>${stat.value}</h3>
        <p>${stat.label}</p>
      </div>`
      )
      .join("");
  }

  function buildSections(sections) {
    return sections
      .map(
        (section) => `
      <section class="industry-section" id="${section.id}">
        <h2>${section.title}</h2>
        <p>${section.copy}</p>
        <div class="case-grid">
          ${section.cards
            .map(
              (card) => `
            <article class="case-card">
              <h3>${card.title}</h3>
              <strong>${card.result}</strong>
              <ul>
                ${card.points.map((point) => `<li>${point}</li>`).join("")}
              </ul>
            </article>`
            )
            .join("")}
        </div>
      </section>`
      )
      .join("");
  }

  function buildProcess(steps) {
    return steps
      .map(
        (step, index) => `
      <div class="step-card">
        <span>${index + 1}</span>
        <h4>${step.title}</h4>
        <p>${step.copy}</p>
      </div>`
      )
      .join("");
  }

  function renderPlacementPage(root) {
    if (!root) return;

    const viewKey = root.dataset.view || "default";
    const variant = viewConfigs[viewKey] || viewConfigs.default;

    const heroEyebrow = variant.heroEyebrow || placementData.hero.eyebrow;
    const heroTitle = variant.heroTitle || placementData.hero.title;
    const heroIntro = variant.heroIntro || placementData.hero.intro;
    const heroDetail = variant.heroDetail || placementData.hero.detail;
    const filterSummary = variant.filterLabel
      ? `<div class="filter-summary">
          <span>${variant.filterLabel}</span>
        </div>`
      : "";

    root.innerHTML = `
      <header class="site-header">
        <div class="site-header__inner">
          <a class="site-header__brand" href="/">
            <img src="/wp-content/uploads/digital-growth-studios-logo.jpg" alt="Digital Growth Studios">
            Digital Growth Studios
          </a>
          <nav class="site-nav" aria-label="Primary">
            <a href="/">Home</a>
            <a href="/services/">Services</a>
            <a href="/results/">Results</a>
            <a href="/company/">Company</a>
            <a href="/blog/">Resources</a>
          </nav>
          <div class="site-header__cta">
            <a href="/contact/">Book a Call</a>
          </div>
        </div>
      </header>

      <main class="placement-results">
        <section class="results-hero">
          <p class="eyebrow">${heroEyebrow}</p>
          <h1>${heroTitle}</h1>
          <p>${heroIntro}</p>
          <p>${heroDetail}</p>
        </section>

        ${filterSummary}

        <div class="stats-grid">
          ${buildStats(placementData.stats)}
        </div>

        ${buildSections(placementData.sections)}

        <section class="process-section">
          <h2>How a placement sprint works</h2>
          <p>Whether you need a landscaping blitz, dumpster coverage, or contractor staffing, we run the same tight process.</p>
          <div class="step-grid">
            ${buildProcess(placementData.processSteps)}
          </div>
        </section>

        <section class="cta-panel">
          <h3>${placementData.cta.title}</h3>
          <p>${placementData.cta.copy}</p>
          <a href="${placementData.cta.link.href}">${placementData.cta.link.label}</a>
        </section>
      </main>

      <footer class="results-footer">
        <div class="results-footer__grid">
          <div>
            <h4>Contact</h4>
            <p>92 east 7720 s</p>
            <p><a href="tel:+13852162993">(385) 216-2993</a></p>
          </div>
          <div>
            <h4>Company</h4>
            <ul>
              <li><a href="/team/">Team</a></li>
              <li><a href="/company/">Agency</a></li>
              <li><a href="/results/">Results</a></li>
              <li><a href="/blog/">Blog</a></li>
              <li><a href="/contact/">Contact</a></li>
            </ul>
          </div>
          <div>
            <h4>Services</h4>
            <ul>
              <li><a href="/services/paid-search/">Search</a></li>
              <li><a href="/services/paid-social/">Social</a></li>
              <li><a href="/services/creative/">Creative</a></li>
              <li><a href="/services/amazon/">Amazon</a></li>
              <li><a href="/services/seo/">SEO</a></li>
              <li><a href="/services/hubspot/">HubSpot</a></li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">COPYRIGHT © <span id="footer-year"></span> DIGITAL GROWTH STUDIOS.</div>
      </footer>
    `;

    const footerYear = root.querySelector("#footer-year");
    if (footerYear) {
      footerYear.textContent = new Date().getFullYear();
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    const root = document.getElementById("placement-page-root");
    renderPlacementPage(root);
  });
})();

