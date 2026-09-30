# Solution Requirements Specification: Functional, Non-Functional & Service Level Agreements

**Project**: Streamlining IT Procurement: Automating Standard Laptop Orders with Flow Designer  
**Document Reference**: REQ-PHASE2-SRS-V1.0  
**Target Environment**: ServiceNow Utah / Vancouver / Washington DC / Xanadu LTS  
**System Module**: Service Catalog, Flow Designer, ITAM, Platform Governance  

---

## 1. Executive Summary

This document establishes the definitive engineering baseline for the automated Standard Laptop Procurement solution. It details:
1. **Functional Requirements (FR-01 to FR-12)**: The deterministic business capabilities, routing logic, validation policies, and transactional workflows required.
2. **Non-Functional Requirements (NFR-01 to NFR-06)**: The performance, security, availability, usability, auditability, and maintainability mandates.
3. **Platform Constraints & Architecture Assumptions**: The operational boundaries governing ServiceNow configuration.
4. **SLA & OLA Governance Framework**: The multi-tiered Service Level Agreement and Operational Level Agreement hierarchy ensuring end-to-end fulfillment within 72 business hours.

---

## 2. Functional Requirements (FR)

The system enforces 12 discrete functional requirements across the requisition, governance, staging, asset management, and lifecycle closure modules.

| Requirement ID | Requirement Name | Description & Functional Logic | Priority | Acceptance Verification Criteria | Traceability |
|:---|:---|:---|:---:|:---|:---|
| **FR-01** | Unified Catalog Item Definition | The system shall provide a single catalog item named "Standard Laptop Order" located under `Hardware > Computers` in the enterprise Service Catalog. The item shall be governed by User Criteria (`snc_internal`), accessible to all active corporate employees. | **Must Have** | Authenticate as standard employee; verify item appears in catalog search and category view; verify external/vendor users cannot access item. | US-01 |
| **FR-02** | Structured Variable Architecture & Dynamic Defaults | The catalog form shall capture: `requested_for` (Reference: `sys_user`), `hardware_bundle` (Choice: Windows Business, Windows Developer, macOS Developer), `delivery_method` (Choice: Desk Drop, Depot Pickup, Remote Courier), `shipping_address` (String), and `business_justification` (Multi-line text). Form shall dynamically auto-populate employee department, site, and manager from `sys_user`. | **Must Have** | Load form as employee Alex Chen; verify `requested_for`, Department, Location, and Manager auto-fill; verify `shipping_address` becomes visible and mandatory only when `delivery_method == 'Remote Courier'`. | US-01, US-02 |
| **FR-03** | Transactional Order Cart & Item Generation | Submission of the catalog item shall generate exactly one parent `sc_request` record and one child `sc_req_item` record. The parent request `price` shall reflect the aggregated cost of the selected laptop hardware bundle. | **Must Have** | Submit catalog order; query database to confirm generation of linked `sc_request` and `sc_req_item`; verify record numbering conventions (`REQ...`, `RITM...`). | US-01 |
| **FR-04** | Flow Designer Autonomous Triggering | The flow `Automated_Standard_Laptop_Fulfillment` shall trigger autonomously and execute within 5 seconds of `sc_req_item` insert when: `cat_item` IS "Standard Laptop Order" AND `state` IS "1" (Open). | **Must Have** | Inspect `sys_flow_context` upon record insertion; verify trigger conditions evaluate to true; verify execution begins within 5000 milliseconds. | US-03 |
| **FR-05** | Dynamic Two-Tier Approval Routing | The flow shall execute the `Ask for Approval` action targeting the requester's direct manager (`requested_for.manager`). If `hardware_bundle == 'Developer Standard (macOS)'` (unit cost > $2,500), the flow shall dynamically append a secondary approval tier to the IT Finance Director. | **Must Have** | Submit Windows Developer order -> verify single manager approval generated. Submit macOS Developer order -> verify sequential or parallel approval generated for Finance Director. | US-03 |
| **FR-06** | Actionable Interactive Notifications | The platform shall dispatch actionable email notifications to designated approvers containing employee details, hardware tier, cost center, and business justification, featuring 1-click cryptographic `[Approve]` and `[Reject]` actions requiring zero portal login. | **Must Have** | Trigger approval; inspect outbound email in `sys_email`; reply via 1-click token; verify `sysapproval_approver` transitions state to `approved` automatically. | US-03 |
| **FR-07** | Deterministic Rejection Handling | If any approval step evaluates to "Rejected", the flow shall immediately update `sc_req_item.state = 4` (Closed Incomplete), set `stage = request_cancelled`, log the approver's mandatory comments in Work Notes, send an explanatory notification to the requester, and terminate execution. | **Must Have** | Reject approval record with reason "Budget exceeded"; verify RITM transitions to Closed Incomplete; verify requester receives rejection email; confirm zero `sc_task` records created. | US-04 |
| **FR-08** | Automated Catalog Task (`sc_task`) Dispatch | Immediately upon approval confirmation, Flow Designer shall instantiate an `sc_task` assigned to the `Hardware Fulfillment Depot` group. The task must inherit all RITM variables into its Variable Editor and set Priority = `3` (Moderate) or `2` (High if requester is VIP). | **Must Have** | Approve pending RITM; verify `sc_task` generated within 10 seconds; verify assignment group is `Hardware Fulfillment Depot`; verify short description includes laptop model and user name. | US-06 |
| **FR-09** | Mandatory Asset Reconciliation (`alm_hardware`) | A ServiceNow Data Policy shall prevent closing an `sc_task` unless `u_asset_tag` is populated with a valid barcode corresponding to an in-stock asset in `alm_hardware`. Upon valid task closure, the flow shall update the asset record: `install_status = 1` (In Use), `assigned_to = requested_for`, `substatus = NULL`. | **Must Have** | Attempt task closure with empty asset tag -> verify blocked with error. Enter valid asset tag `AST-009482` and close -> verify `alm_hardware` updates status to `In Use` and sets `assigned_to`. | US-07 |
| **FR-10** | End-to-End Portal Stage Transparency | The flow shall update `sc_req_item.stage` at each operational milestone: `waiting_for_approval` -> `fulfillment` -> `delivery` -> `complete`. These stages must render linearly on the Service Portal request tracker widget. | **Should Have** | Monitor Service Portal `/esc` during workflow execution; verify stage tracker reflects current phase accurately in real time. | US-08 |
| **FR-11** | Cascading Record Lifecycle Closure | When the fulfillment `sc_task` transitions to `Closed Complete`, the flow shall update `sc_req_item.state` to `3` (`Closed Complete`) and trigger cascading closure of the parent `sc_request` if all child items are complete. | **Must Have** | Mark staging task Closed Complete; verify RITM transitions to Closed Complete; verify parent `sc_request` transitions `request_state` to `closed_complete`. | US-08 |
| **FR-12** | Automated CSAT Feedback Dispatch | Exactly 2 hours following item closure, the system shall trigger an automated Customer Satisfaction (CSAT) survey containing 3 standard Likert-scale questions to the `requested_for` user. | **Should Have** | Fast-forward scheduled job / inspect `asmt_assessment_instance`; verify survey record generated and invitation email sent to employee. | US-08 |

---

## 3. Non-Functional Requirements (NFR)

The system complies with 6 enterprise non-functional dimensions governing reliability, scale, compliance, and user experience.

### 3.1. NFR-01: Performance & Execution Latency
* **Trigger Initiation**: Flow Designer engine shall evaluate trigger conditions and instantiate `sys_flow_context` within **5 seconds** of `sc_req_item` database insertion.
* **Task Provisioning**: Automated creation of child `sc_task` records upon approval receipt shall complete within **10 seconds**.
* **Client-Side Form Performance**: The "Standard Laptop Order" catalog form shall reach Time-to-Interactive (TTI) within **1.5 seconds** over standard enterprise network connections (10 Mbps+), with client scripts completing execution within **200 milliseconds**.
* **Database Query Budget**: No catalog script or flow action may execute un-indexed table scans or queries taking longer than **100 milliseconds** of execution time.

### 3.2. NFR-02: Security, Governance & Role-Based Access Control (RBAC)
* **Principle of Least Privilege**:
  * *Requesters (`snc_internal`)*: Can view and track only requests where `opened_by == gs.getUserID()` or `requested_for == gs.getUserID()`.
  * *Approvers (`approver_user` or `itil`)*: Granted update access exclusively to approval records (`sysapproval_approver`) assigned to their user ID or delegated groups.
  * *Hardware Technicians (`itil`)*: Restricted to reading and updating `sc_task` records assigned to `Hardware Fulfillment Depot`.
  * *Asset Synchronization*: Direct write operations to `alm_hardware` are restricted to the Flow Designer system execution context (`System User`) and credentialed Asset Managers (`asset` role).
* **Data Sanitization**: All user inputs in multi-line fields (`shipping_address`, `business_justification`) shall be sanitized against cross-site scripting (XSS) and SQL injection prior to database persistence.

### 3.3. NFR-03: High Availability, Fault Tolerance & Idempotency
* **Idempotent Flow Execution**: The flow design must be strictly idempotent. If a network interruption or node restart causes a flow action to re-fire, the system must query for existing child records before executing creation logic, preventing duplicate `sc_task` or approval generation.
* **Transient Error Handling**: Outbound notification actions shall incorporate automatic retry mechanisms (up to 3 retries at 60-second intervals) upon encountering transient SMTP or integration gateway failures.
* **Execution State Persistence**: Every state transition must be committed to `sys_flow_context`, allowing administrators to pause, resume, or replay flows without data loss.

### 3.4. NFR-04: Usability & Multi-Device Accessibility
* **WCAG 2.1 AA Compliance**: The catalog interface, variable controls, contrast ratios, and screen-reader labels must pass Web Content Accessibility Guidelines (WCAG) 2.1 Level AA standards.
* **Mobile Responsiveness**: 100% of ordering, approval, and task fulfillment views must render responsively within the native ServiceNow Now Mobile and Mobile Agent iOS and Android applications.
* **Zero Technical Jargon**: All catalog prompts and variable tooltips must use plain business language (e.g., "Developer High-Performance Laptop" instead of "Latitude 7440 Intel i9 13800H 32GB LPDDR5x").

### 3.5. NFR-05: Auditability & Compliance Logging
* **SOX / ITIL Audit Compliance**: 100% of approval submissions, rejections, delegation updates, and technician staging handoffs must be immutably preserved with microsecond timestamps in `sys_audit`, `sysapproval_approver`, and the RITM activity stream.
* **Zero Log Deletion**: Approval and asset attribution records are classified as permanent enterprise compliance artifacts and must be protected against manual deletion or truncation by Business Rules and Access Control Lists (ACLs).

### 3.6. NFR-06: Maintainability, Upgradeability & LTS Longevity
* **Zero Custom Code**: The implementation shall avoid custom compiled Java, jelly scripting, or deprecated Legacy Workflow Editor components.
* **Low-Code Architecture**: All process automation shall be constructed using native out-of-the-box Flow Designer action blocks, subflows, and standard ServiceNow data models.
* **Upgrade Safety**: Configurations must achieve a 100% pass rate in the ServiceNow Automated Test Framework (ATF) across Utah, Vancouver, Washington DC, and Xanadu LTS releases without requiring upgrade-skips or manual remediation.

---

## 4. Platform Technical Constraints & Design Assumptions

### 4.1. Technical Constraints
1. **ServiceNow LTS Platform**: The architecture is constrained to standard functionality available in ServiceNow Utah, Vancouver, Washington DC, and Xanadu releases.
2. **Core Plugin Dependencies**:
   * `com.glide.hub.flow_designer` (Flow Designer Engine v2.0+)
   * `com.snc.service_catalog.core` (Service Catalog Framework)
   * `com.snc.asset_management` (ITAM Hardware Asset Lifecycle Management)
3. **Execution Script Constraints**: Catalog Client Scripts must be configured as `Isolate Script = true` to run cleanly within the modern Service Portal Angular framework, avoiding direct DOM manipulation (`document.getElementById`).
4. **Data Policy Enforcement**: Validation of mandatory asset tags on `sc_task` must be enforced at the server-level via Data Policy (`sys_data_policy2`) to ensure API and REST updates cannot bypass the rule.

### 4.2. Design Assumptions
1. Corporate user identity, manager hierarchies, and department assignments are synchronized continuously from enterprise Active Directory / Okta via automated LDAP/SSO sync into `sys_user`.
2. Standard hardware bundles (models, RAM, CPU) are maintained in `cmdb_hardware_product_model` and kept in sufficient safety stock (minimum 15 units per model) at the central hardware depot.
3. Technicians possess handheld barcode scanners capable of scanning Code 128 / QR asset tags directly into the browser or Now Mobile app.
4. Line managers have active Microsoft Outlook / Exchange or mobile clients capable of rendering HTML5 Actionable Email Messages.

---

## 5. Service Level Agreement (SLA) & Operational Level Agreement (OLA) Hierarchy

To guarantee the primary business outcome of **reducing standard laptop procurement cycle time from 14.2 business days to under 3 business days (<72 hours)**, a multi-tier SLA/OLA hierarchy is established within the ServiceNow SLA Engine (`contract_sla` and `task_sla`).

```
+---------------------------------------------------------------------------------------------------+
| SLA / OLA TIMELINE HIERARCHY (< 72 BUSINESS HOURS TOTAL)                                          |
+---------------------------------------------------------------------------------------------------+
| [Overall SLA-01: End-to-End Procurement Request SLA (72h)]                                        |
| ├─ [OLA-01: Line Manager Approval OLA (24h)]                                                      |
| │  ├── 0h: Approval Dispatched                                                                    |
| │  ├── 24h: Automated Reminder                                                                    |
| │  └── 48h: Escalation to Dept Head                                                               |
| ├─ [OLA-02: Hardware Depot Staging & Imaging OLA (24h)]                                            |
| │  ├── 0h: sc_task Created                                                                        |
| │  ├── 16h: Warning Threshold (75%)                                                               |
| │  └── 24h: Task Complete & Asset Reconciled                                                      |
| └─ [OLA-03: Logistics Dispatch & Desk Drop OLA (24h)]                                             |
|    ├── 0h: Hardware Packaged                                                                      |
|    └── 24h: Physical Delivery & User First Login                                                  |
+---------------------------------------------------------------------------------------------------+
```

### 5.1. SLA / OLA Matrix & Governance Rules

| Contract Code | Tier | Name | Target Duration | Schedule | Start Condition | Pause Condition | Stop Condition | Breach Escalation Rule |
|:---|:---:|:---|:---:|:---:|:---|:---|:---|:---|
| **SLA-01** | Client SLA | End-to-End Laptop Procurement SLA | **72 Business Hours** | 8x5 Corporate Business Schedule | `sc_req_item` created AND `cat_item` IS "Standard Laptop Order" | `approval == 'requested'` (Paused pending manager action) | `state` IN (`Closed Complete`, `Closed Incomplete`) | At 75% (54h): Warning email to IT Procurement Lead.<br/>At 100% (72h): SLA Breach logged; incident escalated to IT Director. |
| **OLA-01** | Internal OLA | Line Manager Approval Turnaround | **24 Business Hours** | 8x5 Corporate Business Schedule | `sysapproval_approver` created AND `state == 'requested'` | None | `state` IN (`approved`, `rejected`, `cancelled`) | At 24h: High-priority reminder email dispatched.<br/>At 48h: Secondary approval generated for Department Head. |
| **OLA-02** | Internal OLA | Hardware Depot Staging & Imaging | **24 Working Hours** | 8x5 IT Depot Schedule | `sc_task` created with `assignment_group == 'Hardware Fulfillment Depot'` | `state == '2'` AND `work_notes` contains "Awaiting Supplier Stock" | `state` IN (`3 - Closed Complete`, `4 - Closed Incomplete`) | At 75% (18h): Depot Supervisor alert.<br/>At 100% (24h): Ticket color turns red; escalated to Depot Operations Manager. |
| **OLA-03** | Internal OLA | Logistics Delivery & User Handover | **24 Working Hours** | 8x5 IT Depot Schedule | Staging task closed AND `delivery_method` IN (`Desk Drop`, `Remote Courier`) | `courier_status == 'In Transit'` | Employee confirms delivery OR courier tracking marks "Delivered" | At 24h: Courier status investigation triggered by IT Logistics Coordinator. |

---

## 6. Requirements Traceability Matrix (FRTM)

This matrix maps Functional Requirements, Non-Functional Requirements, User Stories, and SLA Contracts to demonstrate complete engineering coverage.

| Requirement ID | Requirement Name | User Story ID | Target Platform Table | SLA / OLA Governance | Verification Test Reference |
|:---|:---|:---:|:---|:---:|:---|
| **FR-01** | Catalog Definition | US-01 | `sc_cat_item` | SLA-01 | Test Case TC-01 |
| **FR-02** | Form Variables | US-01, US-02 | `item_option_new` | N/A | Test Case TC-02 |
| **FR-03** | Cart & Item Insert | US-01 | `sc_request`, `sc_req_item` | SLA-01 | Test Case TC-01 |
| **FR-04** | Flow Triggering | US-03 | `sys_hub_flow`, `sys_flow_context` | NFR-01 | Test Case TC-03 |
| **FR-05** | Approval Routing | US-03 | `sysapproval_approver` | OLA-01 | Test Case TC-03 |
| **FR-06** | Actionable Email | US-03 | `sys_email`, `sysevent` | OLA-01 | Test Case TC-03 |
| **FR-07** | Rejection Handling | US-04 | `sc_req_item`, `sysapproval_approver` | SLA-01 | Test Case TC-04 |
| **FR-08** | Task Generation | US-06 | `sc_task` | OLA-02 | Test Case TC-05 |
| **FR-09** | Asset Sync | US-07 | `sc_task`, `alm_hardware` | NFR-05 | Test Case TC-06 |
| **FR-10** | Stage Progression | US-08 | `sc_req_item.stage` | NFR-04 | Test Case TC-07 |
| **FR-11** | Cascading Closure | US-08 | `sc_req_item`, `sc_request` | SLA-01 | Test Case TC-07 |
| **FR-12** | CSAT Dispatch | US-08 | `asmt_assessment_instance` | N/A | Test Case TC-08 |
| **NFR-01** | Latency & Performance | All | Engine subsystem | SLA-01 | Performance Benchmark PB-01 |
| **NFR-02** | Security & RBAC | All | `sys_security_acl` | N/A | Security Audit SA-01 |
| **NFR-03** | Fault Tolerance | All | `sys_flow_context` | SLA-01 | Resiliency Test RT-01 |
| **NFR-04** | WCAG & Mobile | US-01 | Portal / Now Mobile | N/A | Accessibility Audit AA-01 |
| **NFR-05** | Auditability & Logs | US-03, US-07 | `sys_audit`, `sysapproval_approver` | N/A | Compliance Audit CA-01 |
| **NFR-06** | Maintainability | All | Update Set Artifacts | N/A | ATF Test Suite ATF-01 |

---
*End of Solution Requirements Specification — REQ-PHASE2-SRS-V1.0*
