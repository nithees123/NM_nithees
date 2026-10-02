# Comprehensive Empathy Map Canvas: Core Stakeholder Personas
**Document Reference**: PRJ-SNP-P1-003  
**Project**: Streamlining IT Procurement: Automating Standard Laptop Orders with Flow Designer  
**Milestone**: M1 (Phase 1 — Ideation Deliverables)  
**Author**: Project Implementation Team (Ideation Lead)  
**Classification**: User Experience (UX), Human-Centered Design & Stakeholder Psychology  
**Status**: Submission Ready  

---

## 1. Executive Summary & Persona Mapping Methodology

Enterprise IT transformations often fail when automation is designed strictly around database schemas rather than the real-world operational experiences, frustrations, and behavioral patterns of the human beings who interact with the system. To ensure that the **ServiceNow Flow Designer Standard Laptop Procurement Automation** delivers authentic operational relief, user satisfaction, and frictionless compliance, a rigorous Human-Centered Design (HCD) study was conducted across three pivotal stakeholder personas.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   THE HARDWARE PROCUREMENT TRIAD                                 │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
            ┌────────────────────────────────────────────────────────┐
            │                     DAVID CHEN                         │
            │           End-User Requester / Sr. Developer           │
            │  "I need the right machine to do my job on Day One."   │
            └───────────────────────────┬────────────────────────────┘
                                        │ (Submits Order & Awaits Delivery)
                                        ▼
            ┌────────────────────────────────────────────────────────┐
            │                    SARAH JENKINS                       │
            │          IT Procurement & Asset Specialist             │
            │  "I need 100% compliance without manual data entry."   │
            └───────────────────────────┬────────────────────────────┘
                                        │ (Governs Approvals & Task Dispatch)
                                        ▼
            ┌────────────────────────────────────────────────────────┐
            │                    MARCUS VANCE                        │
            │         Lead Desktop Support & Staging Tech            │
            │  "I need structured specs and predictable queues."     │
            └────────────────────────────────────────────────────────┘
```

The study examined three distinct operational perspectives:
1. **The Fulfillment Orchestrator**: **Sarah Jenkins**, Senior IT Asset & Procurement Coordinator, representing back-office operations, vendor management, and asset compliance.
2. **The End-User Consumer**: **David Chen**, Senior Full-Stack Software Engineer (and incoming new hire/refresh requester), representing technical knowledge workers requiring high-performance computing tools.
3. **The Hardware Configurator**: **Marcus Vance**, Lead Desktop Support & Hardware Staging Technician, representing depot engineering, physical configuration, imaging, and logistics.

For each persona, a deep-dive empathy canvas was synthesized encompassing full demographic context, verbatim statements (**Says**), internal cognitive processes (**Thinks**), observable behavioral habits (**Does**), emotional state dynamics (**Feels**), systemic operational friction (**Pains**), and high-value target outcomes (**Gains**).

---

## 2. Persona 1: IT Procurement Specialist — Sarah Jenkins

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PERSONA PROFILE: SARAH JENKINS                                                                   │
├───────────────────┬──────────────────────────────────────────────────────────────────────────────┤
│ Professional Role │ Senior IT Asset & Procurement Coordinator                                    │
│ Department        │ Corporate IT Operations / Procurement & Vendor Management                    │
│ Demographics      │ Age 34, 7 years in corporate IT asset management; ITIL v4 Managing Professional│
│ Core Environment  │ ServiceNow ITSM, SAP ERP, Excel Workbooks, Dell Premier, CDW, Teams, Outlook│
│ Core Objectives   │ Ensure hardware compliance, minimize holding costs, eliminate audit gaps   │
│ Performance KPIs  │ Procurement cycle time, inventory accuracy, asset attribution rate, audit pass│
└───────────────────┴──────────────────────────────────────────────────────────────────────────────┘
```

### 2.1. Persona Context & Behavioral Profile
Sarah Jenkins is the operational linchpin connecting corporate finance, vendor supply chains, and IT operations. She is responsible for reviewing hardware requisitions, ensuring line-manager authorizations conform to corporate delegated authorities, issuing purchase orders when depot stock is depleted, and ensuring every deployed machine is registered in ServiceNow ITAM (`alm_hardware`). 

In the legacy manual environment, Sarah spends over 60% of her working day acting as a human router and data transcription clerk. Instead of focusing on vendor volume discounting or software license harvesting, she is trapped under an avalanche of unformatted emails, conflicting spreadsheets, and angry messages from hiring managers.

### 2.2. Sarah's Empathy Map Canvas

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   EMPATHY MAP CANVAS: SARAH JENKINS                                    │
├──────────────────────────────────────────────────┬─────────────────────────────────────────────────────┤
│ SAYS (External Communication & Direct Quotes)    │ THINKS (Internal Monologue & Unspoken Concerns)     │
├──────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ • "I spend half my day tracking down managers    │ • "Why are we using an enterprise platform like     │
│   on Teams just to get a one-word email approval."│   ServiceNow if I have to copy data into Excel?"    │
│ • "Every quarter, the external auditors ask for  │ • "An audit finding for unapproved hardware spend   │
│   approval trails, and I have to dig through     │   is going to land squarely on my performance review│
│   archived Outlook PST files to prove signoff."  │   even though it's the process that is broken."     │
│ • "If requesters don't specify their office site │ • "I feel like a clerical typist instead of an IT   │
│   or cost center, I can't place the order."      │   procurement professional."                        │
│ • "We have laptops sitting in depot shelves while│ • "If we lose track of one MacBook Pro, that's $3,000│
│   people are screaming that they don't have one."│   of capital that literally vanishes into thin air."│
├──────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ DOES (Observable Actions & Habits)               │ FEELS (Emotional States & Stress Dynamics)          │
├──────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ • Maintains a shadow Excel workbook on SharePoint│ • Anxious and defensive whenever external audit     │
│   with 28 columns to track order progress.       │   season approaches.                                │
│ • Manually copies employee names, model numbers, │ • Overwhelmed by disjointed email threads and       │
│   and shipping addresses between 3 separate apps.│   constant emergency escalation pings on Teams.     │
│ • Sends polite reminder messages to managers on  │ • Frustrated that strategic vendor negotiations are │
│   day 3, day 5, and day 7 of approval stagnation.│   delayed because she is consumed by clerical data. │
│ • Cross-checks the physical depot inventory by   │ • Resentful of being blamed for fulfillment delays  │
│   calling Marcus directly on his mobile phone.   │   caused by line managers ignoring approval emails. │
├──────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ PAINS (Frustrations, Obstacles & System Friction)│ GAINS (Aspirations, Target Outcomes & Relief)       │
├──────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ • Complete absence of an immutable approval log  │ • A single, automated Flow Designer process that    │
│   in ServiceNow, creating severe SOX audit risk. │   routes approvals and captures immutable logs.     │
│ • Swivel-chair data entry causing transcription  │ • Elimination of the shadow Excel spreadsheet in    │
│   errors in model specs and shipping destinations│   favor of real-time ServiceNow reporting.          │
│ • Ghost assets in alm_hardware caused by         │ • Automatic gating that prevents task completion    │
│   technicians forgetting to record asset tags.   │   without a verified barcode scan.                  │
│ • Constant barrage of status inquiry calls from  │ • Slashing manager approval time from 4.8 days to   │
│   impatient employees and hiring managers.       │   under 8 hours via 1-click mobile email actions.   │
└──────────────────────────────────────────────────┴─────────────────────────────────────────────────────┘
```

---

## 3. Persona 2: End-User Employee / Requester — David Chen

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PERSONA PROFILE: DAVID CHEN                                                                      │
├───────────────────┬──────────────────────────────────────────────────────────────────────────────┤
│ Professional Role │ Senior Full-Stack Software Engineer (New Hire / Refresh Candidate)           │
│ Department        │ Cloud Platform & Core Infrastructure Engineering                             │
│ Demographics      │ Age 31, 8 years software engineering experience; Master's in Computer Science│
│ Core Environment  │ macOS / Linux, Docker, Kubernetes, IntelliJ, VS Code, Git, Jira, Slack       │
│ Core Objectives   │ Build high-availability microservices; execute local containers; commit code │
│ Performance KPIs  │ Sprint velocity, pull request merge rate, mean time to onboard, build latency│
└───────────────────┴──────────────────────────────────────────────────────────────────────────────┘
```

### 3.1. Persona Context & Behavioral Profile
David Chen is an experienced senior software engineer who has recently joined the enterprise to architect microservices for a flagship customer-facing platform. David’s work requires a high-performance workstation equipped with at least 32GB of RAM and high-speed multi-core processing to run local containerized environments (Docker, Kubernetes clusters, local databases, and IDE compilation instances).

In the current legacy model, David experiences the organizational onboarding friction firsthand. He arrived on his first day of employment with eager enthusiasm, only to be handed an eight-year-old dual-core Windows loaner laptop with 8GB of RAM that crashed within thirty minutes of starting a container daemon. When David attempted to order his standardized developer workstation, he was confronted with an opaque, multi-week bureaucratic ordeal.

### 3.2. David's Empathy Map Canvas

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   EMPATHY MAP CANVAS: DAVID CHEN                                       │
├──────────────────────────────────────────────────┬─────────────────────────────────────────────────────┤
│ SAYS (External Communication & Direct Quotes)    │ THINKS (Internal Monologue & Unspoken Concerns)     │
├──────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ • "I can order a personal laptop from Apple or   │ • "Does this company actually value my time if they │
│   Amazon and have it on my doorstep tomorrow.    │   pay me a senior engineering salary to sit idle for│
│   Why does corporate IT take three weeks?"       │   two weeks waiting for basic hardware?"            │
│ • "My manager told me she approved the laptop    │ • "Did my request disappear into a digital black    │
│   last Monday, but the IT portal still says Open."│   hole? Nobody can tell me what stage it's in."  │
│ • "This loaner laptop is so underpowered it can't│ • "I hope they don't send me the standard corporate │
│   even run our Docker compose file without freezing."│ 16GB laptop; I won't be able to run my dev stack."│
│ • "Can someone please tell me if my machine has  │ • "Is corporate IT completely disconnected from the │
│   shipped so I know when to be home for courier?"│   daily reality of modern software development?"    │
├──────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ DOES (Observable Actions & Habits)               │ FEELS (Emotional States & Stress Dynamics)          │
├──────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ • Constantly checks the ServiceNow portal every  │ • Frustrated and professionally blocked during his  │
│   morning, staring at an uninformative static tag.│   first month when he wants to make an impression.  │
│ • Direct-messages his hiring manager and the IT  │ • Embarrassed during team standup meetings when he  │
│   helpdesk channel on Slack every 48 hours.      │   has to report: 'Still blocked waiting on laptop'. │
│ • Attempts to execute development workflows on a │ • Disillusioned by corporate administrative friction│
│   personal machine, creating shadow IT risks.    │   compared to modern consumer digital experiences.  │
│ • Asks teammates if anyone has a spare developer │ • Anxious that his probation milestones and sprint  │
│   machine he can borrow temporarily.             │   commitments will slip through no fault of his own.│
├──────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ PAINS (Frustrations, Obstacles & System Friction)│ GAINS (Aspirations, Target Outcomes & Relief)       │
├──────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ • 14.2-day fulfillment cycle time stalling       │ • A modern, intuitive Service Catalog item with     │
│   sprint productivity and onboarding velocity.   │   clearly defined developer hardware bundles.       │
│ • Zero status visibility between submission and  │ • Real-time, 5-stage graphical progress tracking    │
│   physical delivery (the 'black hole' effect).   │   visible directly on the Employee Center (/esc).   │
│ • Risk of receiving the wrong hardware model due │ • Guaranteed laptop delivery within 72 hours of     │
│   to unvalidated free-text form entries.         │   manager signoff (<3 business days).               │
│ • Wasting hours attending IT service desk queues │ • Automated SMS/Email shipping notifications with   │
│   seeking routine tracking updates.              │   courier tracking numbers for home delivery.       │
└──────────────────────────────────────────────────┴─────────────────────────────────────────────────────┘
```

---

## 4. Persona 3: Hardware Configuration Engineer — Marcus Vance

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PERSONA PROFILE: MARCUS VANCE                                                                    │
├───────────────────┬──────────────────────────────────────────────────────────────────────────────┤
│ Professional Role │ Lead Desktop Support & Hardware Staging Technician                           │
│ Department        │ IT Desktop Support & Depot Staging Logistics                                 │
│ Demographics      │ Age 28, 5 years desktop engineering & endpoint imaging; CompTIA A+, Jamf Pro │
│ Core Environment  │ ServiceNow Task Queues, MDT / SCCM, Jamf Pro, Barcode Scanners, Depot Lab    │
│ Core Objectives   │ High-quality OS deployments, zero staging defects, rapid hardware turnaround │
│ Performance KPIs  │ Staging OLA compliance (<24h), configuration accuracy rate, depot inventory  │
└───────────────────┴──────────────────────────────────────────────────────────────────────────────┘
```

### 4.1. Persona Context & Behavioral Profile
Marcus Vance is the frontline technical specialist who physically transforms boxed hardware into fully configured, secure enterprise workstations. Marcus manages the desktop staging bench, unboxes new equipment, executes network PXE boot deployments, installs required productivity and development software packages, applies asset tags, tests hardware peripherals, and coordinates dispatch via internal desk drops or external couriers.

Under the current manual workflow, Marcus and his depot colleagues are subjected to erratic, unpredictable operational spikes. They receive tickets that lack basic configuration parameters, forcing them to halt staging to contact requesters. Furthermore, Marcus is burdened by tedious manual data entry—typing 12-digit serial numbers, MAC addresses, and barcode asset tags into multiple disconnected screens, resulting in inevitable typographical errors.

### 4.2. Marcus's Empathy Map Canvas

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   EMPATHY MAP CANVAS: MARCUS VANCE                                     │
├──────────────────────────────────────────────────┬─────────────────────────────────────────────────────┤
│ SAYS (External Communication & Direct Quotes)    │ THINKS (Internal Monologue & Unspoken Concerns)     │
├──────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ • "I get tickets assigned to my queue that literally│ • "If tickets had complete hardware profiles and │
│   say 'Prepare laptop for new hire' with no specs,│   verified addresses, I could stage 25 units a day│
│   no delivery site, and no target start date."   │   instead of fighting through 8 tickets."           │
│ • "Why do managers always dump an urgent request │ • "I'm tired of taking the blame for fulfillment    │
│   on us at 4:30 PM on Friday for a Monday start?"│   delays when the ticket sat on a manager's desk for│
│ • "I shouldn't have to type 12-digit serial      │   two full weeks before reaching my queue."         │
│   numbers into three separate screens after      │ • "One typo in a serial number or MAC address ruins │
│   already scanning the physical barcode."        │   our CMDB and network access control for months."  │
│ • "If someone needs a developer image, tell me   │ • "Our team looks disorganized because upstream data│
│   upfront so I don't build a standard Windows box."│  is completely broken."                            │
├──────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ DOES (Observable Actions & Habits)               │ FEELS (Emotional States & Stress Dynamics)          │
├──────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ • Halts staging to send direct emails or chat    │ • Constantly rushed and stressed by unpredictable,  │
│   pings to hiring managers seeking missing info. │   last-minute emergency fulfillment requests.       │
│ • Writes asset tags and serial numbers on paper  │ • Frustrated by repetitive, clerical manual data    │
│   clipboards taped to laptops during imaging.    │   entry that could easily be automated.             │
│ • Performs batch data entry at the end of the    │ • Demoralized when end-users express frustration    │
│   week, manually updating alm_hardware records.  │   upon delivery, assuming the depot caused delays.  │
│ • Manually searches warehouse shelves to confirm │ • Defensive of his team's staging craftsmanship     │
│   whether requested models are physically in stock.│ when tickets lack clear operational specifications.│
├──────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ PAINS (Frustrations, Obstacles & System Friction)│ GAINS (Aspirations, Target Outcomes & Relief)       │
├──────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ • Incomplete, ambiguous sc_task records lacking  │ • Automatically generated sc_task records containing│
│   crucial software bundle and delivery variables.│   pre-validated model, RAM, OS, and site data.      │
│ • Fire-drill requests caused by upstream approval│ • Predictable, leveled staging queues with a strict │
│   delays, leading to stressful emergency rushes. │   24-hour staging OLA and clear prioritization.     │
│ • Manual transcription errors during serial and  │ • Enforced barcode scanning validation directly in   │
│   asset tag entry creating inventory drift.      │   the task UI, automatically updating alm_hardware. │
│ • Lack of clear SLA boundaries, resulting in the │ • Instant closure of upstream RITM and notification │
│   staging team being blamed for entire 14-day wait.│ dispatch upon marking the sc_task Closed Complete. │
└──────────────────────────────────────────────────┴─────────────────────────────────────────────────────┘
```

---

## 5. Cross-Persona Comparative Synthesis & Intersecting Failure Points

A critical insight revealed by the Empathy Map Canvas study is that the three personas do not operate in isolation; rather, **friction experienced by one persona compounds and cascades into the next persona's workflow**, creating an enterprise-wide cycle of operational degradation.

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               CASCADE OF INTERSECTING OPERATIONAL PAINS                                │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘

    [ DAVID CHEN ]                              [ SARAH JENKINS ]                         [ MARCUS VANCE ]
  Submits ambiguous                           Spends 4.8 days chasing                   Receives incomplete
  unvalidated ticket                          manager approval via                      ticket with missing
  lacking specifications ───────────────────► email chains; re-keys ──────────────────► software specs at 4:30 PM
                                              data into Excel spreadsheets              on Friday afternoon
         ▲                                                                                       │
         │                                                                                       │
         │                        [ THE VICIOUS CYCLE OF FAILURE ]                               ▼
         └───────────────────────────────────────────────────────────────────────────────────────┘
                                David waits 14.2 business days, receives
                                wrong model or loaner, Marcus takes the blame,
                                and Sarah fails the external SOX inventory audit.
```

### 5.1. The Vicious Cycle of Legacy Friction
1. **Intake Deficiency**: David submits an unformatted request lacking clear hardware specs.
2. **Administrative Chasing**: Sarah must pause processing to clarify requirements with David, then manually chases David's manager for approval over a 4.8-day email delay.
3. **Transcription & Swivel-Chair**: Sarah manually copies data into an Excel spreadsheet, misinterpreting David's developer requirements and failing to include delivery instructions.
4. **Emergency Staging**: The ticket lands in Marcus's queue with zero warning on Friday afternoon for a Monday start. Marcus rushes to image a standard Windows box instead of David's needed high-RAM developer workstation.
5. **Asset Drift & User Frustration**: Marcus ships the machine without updating ServiceNow, creating a ghost asset in `alm_hardware`. David receives an underpowered machine on Day 14, opens a defect ticket, and begins the cycle anew.

---

## 6. Architectural Translation: How Flow Designer Delivers Persona Gains

The ServiceNow Flow Designer architecture was specifically engineered to dismantle each persona's operational pain points and systematically deliver their target gains.

```
+--------------------+---------------------------------------+---------------------------------------+------------------------------------------+
| Persona            | Core Operational Pain Point           | Flow Designer Architectural Solution  | Quantifiable Target Gain Delivered       |
+--------------------+---------------------------------------+---------------------------------------+------------------------------------------+
| **Sarah Jenkins**  | Chasing managers via email; unlinked  | Flow Designer Action: *Ask for        | Approval time cut from 4.8 days to       |
| (Procurement Lead) | approvals; SOX audit non-compliance   | Approval* with 1-click mobile email   | < 8 hours; 100% immutable audit log in   |
|                    | and Excel spreadsheet tracking.       | and automated 24h reminders.          | sys_flow_context and sysapproval_approver.|
+--------------------+---------------------------------------+---------------------------------------+------------------------------------------+
| **David Chen**     | 14.2-day cycle time; zero status      | Standard Catalog Item with dynamic    | Turnaround reduced to < 3 business days; |
| (Sr. Developer /   | visibility; receiving wrong hardware  | variable bundles; real-time 5-stage   | 100% real-time stage tracking on portal; |
| Requester)         | specs; blocked sprint productivity.   | visual tracking bar on Employee Center| zero spec errors; Day 1 readiness.       |
+--------------------+---------------------------------------+---------------------------------------+------------------------------------------+
| **Marcus Vance**   | Ambiguous tickets; 4:30 PM emergency  | Action: *Create Catalog Task* with    | Fully populated sc_task with pre-bound   |
| (Desktop Support / | rushes; manual serial/tag re-keying;  | data pills binding RITM variables;    | specs; 24h staging OLA; mandatory barcode|
| Staging Tech)      | unlinked ghost assets in inventory.   | mandatory barcode validation on close.| validation updating alm_hardware in-place.|
+--------------------+---------------------------------------+---------------------------------------+------------------------------------------+
```

### 6.1. Architectural Realization for Sarah Jenkins
* **Automated Governance**: The flow automatically looks up `trigger.current.opened_by.manager` and instantiates a formal record in `sysapproval_approver`. If the manager does not respond within 24 business hours, an automated reminder is dispatched. If unapproved at 48 hours, it escalates to the Department Head.
* **Audit Elimination**: Zero need to archive Outlook emails; every approval decision, timestamp, and comment is permanently bonded to the RITM execution record.

### 6.2. Architectural Realization for David Chen
* **Service Portal Transparency**: As Flow Designer executes, it transitions `sc_req_item.stage` across `waiting_for_approval`, `fulfillment`, `delivery`, and `complete`. David views an interactive, graphical stage bar on `/esc` at any time from his desktop or mobile phone.
* **Guaranteed Developer Specifications**: Catalog UI policies enforce pre-approved developer bundles (Apple MacBook Pro 16" or Dell Precision 16" with 32GB RAM and 1TB SSD), preventing human misinterpretation.

### 6.3. Architectural Realization for Marcus Vance
* **Pre-Populated Context**: Flow Designer creates the `sc_task` and populates the Task Description with:
  `"Stage Standard Laptop: Developer Standard (macOS) for David Chen. Delivery Site: Remote Courier (1044 Market St, San Francisco, CA). Target Start Date: 2026-10-15."`
* **Automated Asset Synchronization**: A ServiceNow Data Policy prevents Marcus from setting the task state to "Closed Complete" unless the `u_asset_tag` field contains a valid record from `alm_hardware`. Once saved, Flow Designer automatically updates the asset status from "In Stock" to "In Use" and assigns ownership to David Chen with zero manual re-typing.

---

## 7. Conclusion & Design Sign-Off

The Empathy Map Canvas study demonstrates that automating standard laptop procurement using ServiceNow Flow Designer transcends simple technical scripting; it fundamentally reshapes the day-to-day work environment for employees across the enterprise. 

By eliminating 37.5 hours of manual friction per order, providing real-time transparency, enforcing data integrity at the point of intake, and automating governance and asset lifecycle tracking, the proposed architecture restores trust, elevates productivity, and creates an empowering, modern digital workplace experience.
