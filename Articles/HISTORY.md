# From Project Rome to Vatican Vault
## The Untold Story of Windows Activity Tracking — and the Tool That Unlocks It

---

> *"Those who cannot remember the past are condemned to repeat it."*
> — George Santayana
>
> *Windows, it turns out, remembers everything.*

---

## Part I: The Vision — Microsoft Project Rome (2015–2018)

In the summer of 2015, as Windows 10 was rolling out to hundreds of millions of PCs, Microsoft's engineering teams were quietly working on something far more ambitious than a new operating system. They were building a platform for **continuity of human experience** across every device a person might own.

The project was called **Rome**.

Project Rome was Microsoft's cross-device SDK — a developer platform that allowed applications to seamlessly hand off tasks, share data, and synchronize state between phones, tablets, PCs, and Xbox consoles. The philosophical heart of Rome was simple but profound: a person's digital life does not exist on one device. It exists in *their head* — and every device should be able to see the full picture.

The engineering problem Rome tried to solve was synchronization. If you started drafting an email on your phone at breakfast, Rome would ensure that email was waiting for you, exactly as you left it, when you sat down at your desktop at the office. If you paused a video on your Xbox, Rome would let you resume it on your Surface tablet during a flight.

To do this, Rome needed to know what you were doing, and when.

Rome introduced the concept of **User Activities** — structured records of what a user was working on, including the application, the document or URL, a timestamp, and enough context to reconstruct the task. These activity records became the raw material for a feature that would eventually ship to hundreds of millions of Windows users.

That feature was called **Timeline**.

---

## Part II: The Product — Windows Timeline (2018–2021)

### "Scroll Back in Time on Your PC"

On April 30, 2018, Microsoft shipped **Windows 10 version 1803**, codenamed "April 2018 Update." Buried in the release notes, alongside improvements to Cortana and a new Fluent Design refresh, was a modest new feature: **Timeline**.

The Windows Timeline button lived in the taskbar, right next to the Task View button. Click it and a scrollable history of everything you had worked on — every document, every website, every app — stretched back across weeks and months like an infinite scroll of your digital life.

Timeline was genuinely useful. Forgot the name of that spreadsheet from three weeks ago? Scroll back. Need to find the research tab you had open during that conference call? It was there. Timeline remembered.

Under the hood, Timeline was powered by a **SQLite database** called `ActivitiesCache.db`, stored in the user profile at:

```
C:\Users\<username>\AppData\Local\ConnectedDevicesPlatform\<account_id>\ActivitiesCache.db
```

This database contained dozens of tables that recorded every application launch, every file access, every website visit, and the precise timestamps of each interaction. Each record included a JSON payload with structured metadata — application names, content URLs, device identifiers, clipboard contents, and more.

Timeline synchronized this data to Microsoft's cloud via the **Connected Devices Platform** (CDP) service, meaning your activity history could roam across all your signed-in Windows devices. Cross-device continuity, just as Project Rome had promised.

### The Forensic Gold Mine Nobody Was Talking About

Security researchers began to notice. In 2018 and 2019, a small number of digital forensics practitioners and incident responders started analyzing `ActivitiesCache.db` and publishing their findings.

What they found was remarkable:

- **Application launch history**: Every executable that ran, with timestamps precise to the millisecond
- **File access records**: Paths to documents, images, and archives — including files that had since been deleted from the filesystem
- **Browser history**: URLs visited across all Chromium-based browsers, saved in structured JSON
- **Clipboard contents**: In some versions, text copied to the clipboard
- **Device correlation**: Records from other synced devices, allowing cross-machine activity reconstruction
- **Network paths**: UNC paths suggesting remote file server access

The SQLite schema was complex but parseable. A determined analyst could reconstruct a user's complete digital workday, minute by minute, simply by querying this single database file — with no special tools required beyond SQLite and patience.

Timeline had quietly created the most comprehensive user activity log that had ever shipped to mainstream Windows users.

### The Deprecation

In March 2021, Microsoft announced that Windows Timeline's cross-device sync feature would be removed. By the end of 2021, Timeline was quietly deprecated, with new Windows 11 installations no longer showing it in the taskbar. Microsoft offered no public explanation beyond a vague statement about "streamlining" the experience.

The `ActivitiesCache.db` database remained, but it was no longer actively promoted as a user feature.

The lesson: Microsoft had built an extraordinary activity tracking infrastructure, shipped it to the world, and then stepped back from it — only to return with something far more powerful three years later.

---

## Part III: The Successor — Microsoft Recall (2024)

### "Recall Anything You've Seen on Your PC"

At Microsoft's May 2024 Build conference, CEO Satya Nadella unveiled **Copilot+ PCs** — a new class of Windows 11 hardware powered by dedicated AI accelerators (NPU chips from Qualcomm, Intel, and AMD). The flagship feature of Copilot+ PCs was a new AI tool called **Microsoft Recall**.

The pitch was audacious: Recall would take **screenshots of everything you did on your PC**, every few seconds, and use AI vision models to index the content of every screen. You could then search your entire visual history using natural language — "the email about the Johnson contract," "the recipe I was looking at last Tuesday," "the GitHub issue I was debugging" — and Recall would show you the exact screenshot.

It was Timeline's philosophy taken to its ultimate extreme: not just logging metadata about what you did, but **visually recording everything**.

### The Architecture

Recall stored its data in a SQLite database called `ukg.db`, located in the user profile at:

```
C:\Users\<username>\AppData\Local\CoreAIPlatform.00\UKP\{<GUID>}\ukg.db
```

The database schema was sophisticated:

- **`WindowCapture` table**: Records for every screenshot taken, including timestamps, window titles, and application identifiers
- **`ImageText` table**: The OCR-extracted text from every screenshot, fully indexed and searchable
- **`WebPage` table**: URLs detected in screenshots of browsers
- **`AppActivity` table**: Application-level activity aggregations

The screenshots themselves were stored as encrypted image files on disk, with Recall using Windows Hello biometric authentication (facial recognition or fingerprint) to decrypt them on demand.

The AI indexing pipeline ran entirely **on-device** — the NPU would process the screenshots locally, extract entities and text via OCR, and build a semantic index without any data leaving the machine. Microsoft positioned this as a privacy-forward design.

### The Privacy Firestorm

Within days of the announcement, security researchers tore apart the Recall architecture and published explosive findings:

- Recall captured screenshots containing **passwords, credit card numbers, private messages, medical information, and banking data** with no awareness that sensitive content was in frame
- The OCR database was fully searchable by any process running as the user — no special permissions required
- Security researcher Kevin Beaumont published a tool called **TotalRecall** that demonstrated how to extract and search the entire Recall database in minutes
- Another researcher showed that the database could capture **authentication tokens and API keys** visible in terminal windows, providing a ready-made credential harvesting mechanism

The backlash was immediate and severe. Privacy advocates, security researchers, and government bodies in the UK and EU raised alarms. Headlines called Recall "the most dangerous feature Microsoft has ever shipped." Microsoft delayed the Recall rollout, first to remove it from default installations, then to add additional security measures including biometric authentication for the database and a "sensitive content filter" that attempted to detect and skip screenshots containing passwords and payment information.

By late 2024 and into 2025, a revised version of Recall began rolling out to Copilot+ PC owners who opted in. The data remained — encrypted but accessible to the authenticated user, and therefore accessible to any forensic analyst, law enforcement investigator, or malicious actor who obtained access to the machine.

---

## Part IV: The Tool — Vatican Vault

### Born from Necessity

The Timeline/Recall ecosystem had created an extraordinary paradox:

On one hand, Microsoft had built the most comprehensive user activity logging system ever shipped in a mainstream operating system — a forensic goldmine that could reconstruct exactly what a person did, saw, and accessed on their PC, often going back months or years.

On the other hand, the tools available to analyze this data were fragmented, primitive, and inaccessible. A handful of open-source Python scripts could parse `ActivitiesCache.db`. Some DFIR (Digital Forensics and Incident Response) platforms had added Timeline support as an afterthought. Nobody had built a unified, AI-powered platform that treated Windows Timeline and Recall as the primary intelligence sources they deserved to be.

**Vatican Vault** was built to fill that gap.

### The Design Philosophy

Vatican Vault was built on a core conviction: **the data already exists**. Every Windows PC running Timeline or Recall is already recording a rich, structured log of user behavior. The problem is not data collection — it's data interpretation.

The platform was designed to answer the questions that investigators, security teams, and analysts actually ask:

- *"What was this person doing between 2 PM and 5 PM on the day of the incident?"*
- *"Who accessed this file, and when was the last time it was opened?"*
- *"Does this user's behavior match the profile of an insider threat?"*
- *"Were any credentials or sensitive documents visible on screen during this session?"*
- *"What anomalous activities occurred outside normal working hours?"*

### The Technical Foundation

Vatican Vault combines several layers of analysis:

**Layer 1 — Database Parsing**: Native parsers for `ActivitiesCache.db` (Windows Timeline), `ukg.db` (Windows Recall), and network capture files (PCAP/PCAPNG). The parsers handle schema variations across Windows versions and provide normalized, queryable data structures.

**Layer 2 — Entity Extraction**: A hybrid NLP engine combining rule-based regex patterns (for structured data like emails, IP addresses, and API keys) with spaCy neural NER (for people, organizations, locations, and contextual entities). The entity extractor can identify 20+ entity types across all database content.

**Layer 3 — Behavioral Analytics**: Machine learning models — Isolation Forest for anomaly detection, HDBSCAN for behavioral clustering, Prophet for time-series forecasting — that transform raw activity records into risk signals and behavioral profiles.

**Layer 4 — AI Integration**: Optional integration with Groq, OpenAI, and Anthropic APIs for natural-language explanation of findings, risk scoring, and automated threat narrative generation.

**Layer 5 — Reporting**: Professional HTML, PDF, and structured data exports designed for incident reports, legal proceedings, and executive briefings.

### The Name

The name "Vatican Vault" carries a specific meaning. The Vatican Secret Archives — formally the Vatican Apostolic Archive — is one of the world's most extensive repositories of historical records, containing documents spanning nearly twelve centuries. Access is controlled. Most of the collection has never been publicly examined. The archive holds the accumulated history of an institution that has watched the world from the center of events.

A Windows PC running Recall is, in its own way, a vault. It holds a detailed record of its user's digital life — their communications, their research, their errors, their private moments. Most of that data has never been examined by anyone. Vatican Vault was built to open that vault, understand what's inside, and make sense of it.

---

## Timeline: The Through-Line

Looking back across a decade, the arc is clear:

| Year | Event |
|------|-------|
| 2015 | Microsoft launches Project Rome — cross-device continuity SDK |
| 2017 | Windows Insider builds begin testing Timeline |
| 2018 | Windows Timeline ships in Windows 10 v1803; `ActivitiesCache.db` becomes forensic artifact |
| 2019–2020 | Security community begins publishing Timeline forensics research |
| 2021 | Microsoft deprecates Timeline cross-device sync |
| 2024 | Microsoft announces Recall with Copilot+ PCs; security researchers expose privacy risks |
| 2024 | Microsoft delays Recall rollout, adds encryption and biometric guards |
| 2025 | Recall begins limited rollout to opted-in Copilot+ PC users |
| 2025 | Vatican Vault launches as the first comprehensive Timeline + Recall forensics platform |

---

## The Bigger Picture

Windows Timeline and Recall did not emerge from a vacuum. They are expressions of a broader transformation in how computing platforms think about user activity:

- **Apple** introduced Spotlight with semantic indexing in macOS Tiger (2005); added Siri's contextual awareness; and shipped Screen Time as a behavioral monitoring API.
- **Google** built Chrome History, My Activity, and Google Photos' visual search long before Microsoft shipped Recall.
- **Meta** and social platforms have always treated activity data as their primary asset.

What made Timeline and Recall different was that they sat *on the device*, under the user's (nominal) control, in a format that was locally accessible and forensically analyzable. They created a locally-stored behavioral record of unprecedented richness.

For decades, digital forensics relied on reconstructing user behavior from fragments — browser history here, prefetch files there, event logs scattered across a registry. Timeline and Recall changed the equation. They are complete behavioral logs, designed for human-readable replay.

Vatican Vault was built for the world where that data already exists — and where the ability to read it clearly, quickly, and intelligently is the difference between a solved case and an unsolved one.

---

*Vatican Vault is an open forensics and behavioral intelligence platform. This article was written for educational and historical purposes.*
