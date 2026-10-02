# ServiceNow Flow Designer Technical Specification: Standard Laptop Procurement

**Document Identifier**: FLOW-SPEC-P5-001  
**Flow Name**: `Standard Laptop Procurement Flow`  
**Internal Flow Name**: `laptop_procurement_flow`  
**Application Scope**: `Global` (`global`) / `ITSM Service Catalog`  
**Flow Sys ID**: `7e36816197113110a24734000153af22`  
**Target ServiceNow Release**: Washington DC / Xanadu / Utah  
**Author**: Project Implementation Team (Technical Lead)  
**Status**: Published & Active  

---

## 1. Flow Metadata & Engine Configuration

### 1.1 Header Metadata
* **Flow Name**: Standard Laptop Procurement Flow
* **Internal Name**: `laptop_procurement_flow`
* **Flow Sys ID**: `7e36816197113110a24734000153af22`
* **Application Scope**: `Global` (`global`)
* **Category**: Service Catalog (`service_catalog`)
* **Flow Type**: Flow (`type=flow`)
* **Status**: `Published` (`published`)
* **Active**: `true`
* **Run As**: `System User` (`run_as=system`)
  * *Architectural Rationale*: Running as System User guarantees that cross-table write operations (such as generating records in `sc_task`, modifying asset status in `alm_hardware`, and generating approvals in `sysapproval_approver`) are never obstructed by restrictive User-level Access Control Lists (ACLs) applied to standard employees.
* **Run With Roles**: Elevated System Context (`sys_id: system`)
* **Callable by Client API**: `false`
* **Compiler Build**: `Rome_Patch9_Hotfix2_GraalVM_Engine`
* **Description**: Enterprise-grade automated orchestration engine for corporate laptop procurement. Intercepts `sc_req_item` insertions, resolves catalog variables, applies executive VIP fast-track routing or manager approval gates, queries hardware asset inventory, spawns sequential configuration and logistics tasks, updates asset records in `alm_hardware`, closes request lifecycle records, and dispatches automated transactional customer notifications.

```
+----------------------------------------------------------------------------------------------------+
|                                FLOW DESIGNER TOPOLOGY ARCHITECTURE                                 |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                  [Record Created: sc_req_item]
                                  Condition: cat_item = 'Standard Laptop'
                                                  │
                                                  ▼
                                      [Get Catalog Variables]
                                                  │
                                                  ▼
                                      [Executive VIP Decision]
                                        /                  \
                        [VIP == True]  /                    \  [VIP == False]
                                      ▼                      ▼
                           [Auto-Approve RITM]       [Ask for Manager Approval]
                                      │                      │
                                      │               +──────┴──────+
                                      │               │             │
                                      │          [Approved]     [Rejected]
                                      │               │             │
                                      │               ▼             ▼
                                      │        [Set Stage:    [Set Stage: Cancelled /
                                      │        Fulfillment]   State: Closed Rejected]
                                      │               │             │
                                      │               │             ▼
                                      │               │       [Send Rejection Email]
                                      │               │             │
                                      │               │             ▼
                                      │               │       [Terminate Flow]
                                      \               /
                                       \             /
                                        ▼           ▼
                                   [Subflow: Check Inventory]
                                   (Reserve Stock / Backorder)
                                                  │
                                                  ▼
                                   [Create Task 1: Hardware Imaging]
                                   (Assignment: Hardware Support)
                                                  │
                                                  ▼
                                   [Wait for Task 1 Complete]
                                                  │
                                                  ▼
                                   [Create Task 2: Logistics & Ship]
                                   (Assignment: IT Logistics)
                                                  │
                                                  ▼
                                   [Wait for Task 2 Complete]
                                                  │
                                                  ▼
                                   [Update alm_hardware: In Use]
                                                  │
                                                  ▼
                                   [Update RITM: Closed Complete]
                                                  │
                                                  ▼
                                   [Update REQ: Closed Complete]
                                                  │
                                                  ▼
                                   [Send Shipped Email Notification]
                                                  │
                                                  ▼
                                          [Flow Completed]
+----------------------------------------------------------------------------------------------------+
|                          GLOBAL ERROR HANDLER BLOCK (All Steps Protected)                          |
|  [Catch Exception] -> [Log System Error] -> [RITM On Hold] -> [Create INC] -> [Alert Operations]  |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Trigger Specifications

* **Trigger Definition**: `Record Created` (`297ee6efe0a2a1509cd4b52b2fd96111`)
* **Trigger Instance Sys ID**: `ba36816197113110a24734000153af33`
* **Trigger Table**: `sc_req_item` (Requested Item)
* **Execution Timing**: `Run in Background` (Asynchronous worker queue via `sys_trigger`)
* **Condition Filter**:
  ```sql
  cat_item=0b36816197113110a24734000153af45^stage=request_approved^ORstage=waiting_for_approval^EQ
  ```
* **Filter Explanation**: Triggers specifically when a Requested Item record is generated referencing the `Standard Business Laptop Request` catalog item (`0b36816197113110a24734000153af45`) and the initial stage is either `waiting_for_approval` or `request_approved`.

### 2.1 Trigger Output Data Pills
The Flow Designer engine instantiates and exposes the following root data pills from the trigger record:

| Data Pill Identifier | Label | Data Type | Source Path | Description |
|---|---|---|---|---|
| `{{1__request_item}}` | Trigger - Record Created > Requested Item | `GlideRecord` | `sc_req_item` | Full record context of the inserted RITM |
| `{{1__request_item.sys_id}}` | RITM Sys ID | `GUID` | `sc_req_item.sys_id` | 32-character hexadecimal unique identifier |
| `{{1__request_item.number}}` | RITM Number | `String` | `sc_req_item.number` | Formatted identifier (e.g., `RITM0010482`) |
| `{{1__request_item.opened_by}}` | Opened by | `Reference` | `sc_req_item.opened_by` | Reference to `sys_user` record of submitter |
| `{{1__request_item.opened_by.manager}}` | Requester Manager | `Reference` | `sc_req_item.opened_by.manager` | Submitter's direct reporting manager in `sys_user` |
| `{{1__request_item.opened_by.manager.email}}`| Manager Email | `String` | `sc_req_item.opened_by.manager.email` | Manager email address for direct notifications |
| `{{1__request_item.opened_by.vip}}` | Requester VIP Flag | `Boolean` | `sc_req_item.opened_by.vip` | VIP designation flag on `sys_user` record |
| `{{1__request_item.opened_by.department}}` | Requester Department | `Reference` | `sc_req_item.opened_by.department` | Reference to `cmn_department` |
| `{{1__request_item.opened_by.department.dept_head}}`| Department Head | `Reference` | `sc_req_item.opened_by.department.dept_head` | Fallback approver if manager is null |
| `{{1__request_item.request}}` | Parent Request | `Reference` | `sc_req_item.request` | Reference to parent `sc_request` envelope |
| `{{1__request_item.cat_item}}` | Catalog Item | `Reference` | `sc_req_item.cat_item` | Reference to `sc_cat_item` record |

---

## 3. Comprehensive 17-Action Execution Sequence

Below is the definitive sequence of 17 discrete flow actions, logic gates, and subflows orchestrating the end-to-end lifecycle.

### Step 0: Trigger Instance
* **Action Type**: `sys_hub_trigger_instance` (`Record Created`)
* **Target Table**: `sc_req_item`
* **Outputs Generated**: `{{1__request_item}}`

---

### Step 1: Get Catalog Variables
* **Action Definition**: `core_action_get_variables` (`sys_hub_action_type_definition: 77a064100b10030085c083eb37673a38`)
* **Action Order**: `1`
* **UI ID**: `step_get_variables`
* **Input Parameters**:
  * `Submitted Item` = `{{1__request_item}}`
  * `Catalog Item` = `Standard Business Laptop Request` (`0b36816197113110a24734000153af45`)
  * `Variables to Extract`:
    1. `employee_name` (Reference: `sys_user`)
    2. `department` (Reference: `cmn_department`)
    3. `manager_name` (Reference: `sys_user`)
    4. `job_title` (String)
    5. `asset_type` (Choice: `standard`, `engineering`, `executive`)
    6. `laptop_model` (Choice: `lenovo_t14`, `dell_5440`, `lenovo_p1`, `macbook_pro_14`, `hp_dragonfly`, `macbook_air_15`)
    7. `replacement_reason` (Choice: `new_hire`, `refresh`, `damaged`, `stolen`)
    8. `existing_asset_tag` (String)
    9. `business_justification` (String)
    10. `shipping_type` (Choice: `office_desk`, `remote_shipment`)
    11. `shipping_address` (String)
    12. `accessories` (List Collector: `cmdb_model`)
* **Output Pills Generated**:
  * `{{step[1].variables.employee_name}}`
  * `{{step[1].variables.department}}`
  * `{{step[1].variables.asset_type}}`
  * `{{step[1].variables.laptop_model}}`
  * `{{step[1].variables.replacement_reason}}`
  * `{{step[1].variables.existing_asset_tag}}`
  * `{{step[1].variables.business_justification}}`
  * `{{step[1].variables.shipping_type}}`
  * `{{step[1].variables.shipping_address}}`
  * `{{step[1].variables.accessories}}`

---

### Step 2: Flow Logic — VIP Executive Threshold Decision
* **Action Definition**: `flow_logic_if` (`sys_hub_predicate_action`)
* **Action Order**: `2`
* **UI ID**: `branch_vip_eval`
* **Condition Logic**:
  * `Condition 1`: `{{1__request_item.opened_by.vip}}` IS `true`
  * *OR*
  * `Condition 2`: `{{1__request_item.opened_by.title}}` CONTAINS `Vice President`
  * *OR*
  * `Condition 3`: `{{1__request_item.opened_by.title}}` CONTAINS `Director`
  * *OR*
  * `Condition 4`: `{{step[1].variables.asset_type}}` EQUALS `executive` AND `{{1__request_item.opened_by.vip}}` IS `true`
* **Branching Execution**:
  * If condition evaluates to **TRUE**, execute **Step 3A** (VIP Fast-Track Path).
  * If condition evaluates to **FALSE**, execute **Step 3B** (Standard Approval Path).

---

### Step 3A: VIP Fast-Track Record Update & Auto-Approval
* **Action Definition**: `update_record` (`sys_hub_action_type_definition: f9d01445c0a80166007b88939c381d64`)
* **Action Order**: `3A` (Sub-branch of Step 2 TRUE)
* **UI ID**: `action_vip_auto_approve`
* **Inputs**:
  * `Record`: `{{1__request_item}}`
  * `Table`: `sc_req_item`
  * `Field Values`:
    * `approval` = `approved` (`approved`)
    * `stage` = `fulfillment` (`fulfillment`)
    * `state` = `2` (Work in Progress)
    * `work_notes` = `Executive VIP Fast-Track Rule Applied: Manager approval requirement bypassed for VIP requester {{1__request_item.opened_by.name}} (Title: {{1__request_item.opened_by.title}}). Routed directly to hardware provisioning.`
* **Outputs Generated**: `{{step[3a].record_status}}` = `Success`

---

### Step 3B: Standard Path — Ask for Manager Approval
* **Action Definition**: `ask_for_approval` (`sys_hub_action_type_definition: f8f2e2720b10030085c083eb37673a5a`)
* **Action Order**: `3B` (Sub-branch of Step 2 FALSE)
* **UI ID**: `action_ask_manager_approval`
* **Inputs**:
  * `Record`: `{{1__request_item}}`
  * `Approval Rules`:
    * Rule 1: **Approve when**: `Anyone approves` from `Users`:
      * Dynamic Pill Binding:
        ```javascript
        fd_transform.coalesce(
            {{1__request_item.opened_by.manager}},
            {{1__request_item.opened_by.department.dept_head}},
            "287ee6efe0a2a1509cd4b52b2fd96191" // IT Service Desk Leads Group Sys ID
        )
        ```
    * Rule 2: **Reject when**: `Anyone rejects` from `Users` (same approver pool)
  * `Due Date`: Calculated via transform `fd_transform.date_add_business_days({{1__request_item.sys_created_on}}, 3)` (3 Business Days)
  * `Wait for Completion`: `true` (Halts flow execution until approval event fires)
* **Outputs Generated**:
  * `{{step[3b].approval_state}}` (String: `approved`, `rejected`, `cancelled`)
  * `{{step[3b].approver_record}}` (Reference: `sysapproval_approver`)

---

### Step 4: Flow Logic — Evaluate Approval Result
* **Action Definition**: `flow_logic_if`
* **Action Order**: `4`
* **UI ID**: `branch_approval_eval`
* **Condition Logic**:
  * `Condition 1`: `{{step[3b].approval_state}}` EQUALS `approved`
  * *OR*
  * `Condition 2`: Execution originated from Step 3A (`VIP Auto-Approved`)
* **Branching Execution**:
  * If condition evaluates to **TRUE**, proceed to **Step 5** (Fulfillment Lifecycle).
  * If condition evaluates to **FALSE**, divert to **Step 15** (Rejection Lifecycle).

---

### Step 5: Update RITM to Fulfillment Stage
* **Action Definition**: `update_record`
* **Action Order**: `5`
* **UI ID**: `action_set_ritm_fulfillment`
* **Inputs**:
  * `Record`: `{{1__request_item}}`
  * `Table`: `sc_req_item`
  * `Field Values`:
    * `stage` = `fulfillment` (`fulfillment`)
    * `state` = `2` (Work in Progress)
    * `comments` = `Your laptop procurement request has been authorized and dispatched to IT Hardware Operations for configuration and staging.`
    * `work_notes` = `Authorization confirmed by {{step[3b].approver_record.approver.name}} on {{step[3b].approver_record.sys_updated_on}}. Fulfillment lifecycle initiated.`

---

### Step 6: Subflow — Check Hardware Inventory & Reserve Stock
* **Action Definition**: `call_subflow` (`sys_hub_subflow_instance`)
* **Subflow Called**: `subflow_check_hardware_inventory` (`sys_id: 3c36816197113110a24734000153af88`)
* **Action Order**: `6`
* **UI ID**: `subflow_stock_check`
* **Inputs**:
  * `model_name` = `{{step[1].variables.laptop_model}}`
  * `target_location` = `{{1__request_item.opened_by.location}}`
  * `request_item` = `{{1__request_item.sys_id}}`
* **Subflow Operational Logic**:
  1. Queries `alm_hardware` where `model.name == model_name` AND `install_status == 6` (In Stock) AND `substatus == 'available'`.
  2. If count > 0:
     - Atomically marks first available record `substatus = 'reserved'`.
     - Links `alm_hardware.request_line = {{1__request_item.sys_id}}`.
     - Returns `is_in_stock = true`, `asset_tag = record.asset_tag`, `serial_number = record.serial_number`.
  3. If count == 0:
     - Returns `is_in_stock = false`, `asset_tag = ""`, `serial_number = ""`.
* **Outputs Generated**:
  * `{{step[6].is_in_stock}}` (Boolean)
  * `{{step[6].asset_tag}}` (String)
  * `{{step[6].serial_number}}` (String)

---

### Step 7: Create Catalog Task 1 — Hardware Imaging & Configuration
* **Action Definition**: `create_catalog_task` (`sys_hub_action_type_definition: 155792440b10030085c083eb37673a32`)
* **Action Order**: `7`
* **UI ID**: `action_create_sctask_imaging`
* **Inputs**:
  * `Request Item`: `{{1__request_item}}`
  * `Table`: `sc_task`
  * `Fields`:
    * `short_description` = `Build, Image, and Configure Laptop: ` + `{{step[1].variables.laptop_model}}`
    * `assignment_group` = `Hardware Support` (`sys_id: 8a5055c7c61122780019363fb2241370`)
    * `priority` = Scripted transform:
      ```javascript
      if ({{1__request_item.opened_by.vip}} === true) {
          return 2; // High Priority for VIP
      } else {
          return 3; // Moderate Priority for Standard
      }
      ```
    * `description` = Concatenated string:
      ```text
      HARDWARE PROVISIONING DISPATCH:
      Requester: {{1__request_item.opened_by.name}}
      Department: {{step[1].variables.department.name}}
      Hardware Model: {{step[1].variables.laptop_model}}
      Asset Type: {{step[1].variables.asset_type}}
      Allocated Stock Asset Tag: {{step[6].asset_tag}}
      Serial Number: {{step[6].serial_number}}
      Selected Accessories: {{step[1].variables.accessories}}
      Replacement Reason: {{step[1].variables.replacement_reason}}
      Existing Asset Tag to Retire: {{step[1].variables.existing_asset_tag}}
      
      MANDATORY PROCEDURE:
      1. Retrieve reserved asset {{step[6].asset_tag}} from secure storage.
      2. Apply enterprise Gold Master OS image matching departmental baseline.
      3. Enroll device into Microsoft Intune MDM / Jamf Pro.
      4. Verify BitLocker / FileVault TPM 2.0 full-disk encryption key escrow in Active Directory.
      5. Attach physical tamper-evident barcode asset label.
      6. Enter verified Asset Tag and Serial Number into Task fields before closure.
      ```
    * `due_date` = `fd_transform.date_add_business_days({{1__request_item.sys_created_on}}, 2)`
  * `Wait for Completion`: `true`
* **Outputs Generated**:
  * `{{step[7].catalog_task}}` (Reference: `sc_task`)
  * `{{step[7].catalog_task.state}}` (Choice: `1`=Open, `2`=WIP, `3`=Closed Complete, `4`=Closed Incomplete)

---

### Step 8: Wait for Condition — Task 1 Completion
* **Action Definition**: `wait_for_condition` (`sys_hub_action_type_definition: c4901445c0a80166007b88939c381d55`)
* **Action Order**: `8`
* **UI ID**: `action_wait_task1`
* **Inputs**:
  * `Record`: `{{step[7].catalog_task}}`
  * `Table`: `sc_task`
  * `Conditions`: `state` IS ONE OF `3` (Closed Complete), `4` (Closed Incomplete)
* **Output Evaluation**:
  * If `state == 4` (Closed Incomplete): Trigger Error Handler or escalate to Hardware Supervisor.
  * If `state == 3` (Closed Complete): Advance to Step 9.

---

### Step 9: Create Catalog Task 2 — Logistics & Asset Deployment
* **Action Definition**: `create_catalog_task`
* **Action Order**: `9`
* **UI ID**: `action_create_sctask_logistics`
* **Inputs**:
  * `Request Item`: `{{1__request_item}}`
  * `Table`: `sc_task`
  * `Fields`:
    * `short_description` = `Package, Dispatch, and Ship Laptop to ` + `{{1__request_item.opened_by.name}}`
    * `assignment_group` = `IT Logistics & Field Services` (`sys_id: 287ee6efe0a2a1509cd4b52b2fd96191`)
    * `priority` = `3` (Moderate)
    * `description` = Concatenated string:
      ```text
      DEPLOYMENT & SHIPPING INSTRUCTIONS:
      Recipient: {{1__request_item.opened_by.name}} ({{1__request_item.opened_by.email}})
      Delivery Method: {{step[1].variables.shipping_type}}
      Destination Address:
      {{step[1].variables.shipping_address}}
      
      Packaging Checklist:
      [ ] Configured laptop unit (Serial: {{step[6].serial_number}})
      [ ] OEM 65W/100W USB-C PD power adapter and AC cord
      [ ] Peripherals: {{step[1].variables.accessories}}
      [ ] Return prepaid shipping box and label for retiring asset {{step[1].variables.existing_asset_tag}} (if applicable)
      [ ] Printed Onboarding Quick-Start Guide
      
      REQUIRED CLOSURE ACTION:
      Record Carrier Tracking Number in task work notes and update Delivery Status field.
      ```
    * `due_date` = `fd_transform.date_add_business_days({{1__request_item.sys_created_on}}, 3)`
  * `Wait for Completion`: `true`
* **Outputs Generated**:
  * `{{step[9].catalog_task}}` (Reference: `sc_task`)
  * `{{step[9].catalog_task.work_notes}}`

---

### Step 10: Wait for Condition — Task 2 Completion
* **Action Definition**: `wait_for_condition`
* **Action Order**: `10`
* **UI ID**: `action_wait_task2`
* **Inputs**:
  * `Record`: `{{step[9].catalog_task}}`
  * `Table`: `sc_task`
  * `Conditions`: `state` EQUALS `3` (Closed Complete)

---

### Step 11: Update Asset Record in `alm_hardware`
* **Action Definition**: `update_record`
* **Action Order**: `11`
* **UI ID**: `action_sync_asset_record`
* **Inputs**:
  * `Table`: `alm_hardware`
  * `Record`: Evaluated via query matching `asset_tag == {{step[6].asset_tag}}`
  * `Field Values`:
    * `install_status` = `1` (In Use)
    * `substatus` = `""` (Empty string; clears 'reserved')
    * `assigned_to` = `{{1__request_item.opened_by}}`
    * `assigned` = `{{flow.current_date_time}}`
    * `comments` = `Asset issued via automated Flow Designer workflow for RITM: ` + `{{1__request_item.number}}`

---

### Step 12: Update RITM Record to Closed Complete
* **Action Definition**: `update_record`
* **Action Order**: `12`
* **UI ID**: `action_close_ritm`
* **Inputs**:
  * `Record`: `{{1__request_item}}`
  * `Table`: `sc_req_item`
  * `Field Values`:
    * `stage` = `complete` (`complete`)
    * `state` = `3` (Closed Complete)
    * `active` = `false`
    * `comments` = `Your laptop order has been successfully fulfilled, provisioned, and shipped! Tracking information and onboarding instructions have been dispatched to your corporate email.`
    * `work_notes` = `All sequential fulfillment tasks (Imaging & Logistics) completed successfully. Hardware asset {{step[6].asset_tag}} marked In Use and linked to user {{1__request_item.opened_by.name}}. Flow lifecycle complete.`

---

### Step 13: Update Parent Request Envelope (`sc_request`)
* **Action Definition**: `update_record`
* **Action Order**: `13`
* **UI ID**: `action_close_parent_req`
* **Inputs**:
  * `Record`: `{{1__request_item.request}}`
  * `Table`: `sc_request`
  * `Field Values`:
    * `request_state` = `closed_complete` (`closed_complete`)
    * `stage` = `closed_complete`
    * `state` = `3` (Closed Complete)
    * `work_notes` = `Automated Flow Designer cascade: All child requested items are complete. Closing parent Request.`

---

### Step 14: Send Email Notification — Shipped with Tracking
* **Action Definition**: `send_email` (`sys_hub_action_type_definition: 04e01445c0a80166007b88939c381d44`)
* **Action Order**: `14`
* **UI ID**: `action_send_shipped_email`
* **Inputs**:
  * `To`: `{{1__request_item.opened_by.email}}`
  * `Subject`: `Your Standard Laptop Has Been Shipped - ` + `{{1__request_item.number}}`
  * `Body`:
    ```html
    <p>Dear {{1__request_item.opened_by.first_name}},</p>
    <p>We are pleased to inform you that your laptop procurement order (<strong>{{1__request_item.number}}</strong>) has been fully configured and dispatched.</p>
    
    <div style="background-color: #f8f9fa; border-left: 4px solid #007bff; padding: 15px; margin: 15px 0;">
      <h4 style="margin-top: 0;">Device & Delivery Summary</h4>
      <p><strong>Hardware Model:</strong> {{step[1].variables.laptop_model}}</p>
      <p><strong>Asset Tag Barcode:</strong> {{step[6].asset_tag}}</p>
      <p><strong>Serial Number:</strong> {{step[6].serial_number}}</p>
      <p><strong>Delivery Method:</strong> {{step[1].variables.shipping_type}}</p>
      <p><strong>Shipping Address:</strong> {{step[1].variables.shipping_address}}</p>
    </div>
    
    <h4>First-Time Setup Instructions:</h4>
    <ol>
      <li>Unbox device and connect to the supplied AC adapter.</li>
      <li>Power on and connect to your local Wi-Fi network.</li>
      <li>Log in using your corporate email address ({{1__request_item.opened_by.email}}) and Okta / Azure AD password with MFA.</li>
      <li>Allow 15 minutes for security profiles and productivity applications to finalize.</li>
    </ol>
    <p>Need setup assistance? Visit our <a href="https://service-portal.company.com/kb_view.do?sysparm_article=KB0019284">Hardware Onboarding Portal</a> or reply to this message to reach the IT Service Desk.</p>
    ```

---

### Step 15: Flow Logic — Rejection Path Branch
* **Action Definition**: `flow_logic_else_if`
* **Action Order**: `15`
* **UI ID**: `branch_rejection`
* **Condition Logic**: `{{step[3b].approval_state}}` EQUALS `rejected`

---

### Step 16: Update RITM Record to Cancelled / Rejected
* **Action Definition**: `update_record`
* **Action Order**: `16`
* **UI ID**: `action_reject_ritm`
* **Inputs**:
  * `Record`: `{{1__request_item}}`
  * `Table`: `sc_req_item`
  * `Field Values`:
    * `stage` = `request_cancelled` (`request_cancelled`)
    * `state` = `7` (Closed Rejected)
    * `approval` = `rejected`
    * `active` = `false`
    * `comments` = `Your laptop procurement request has been reviewed and rejected by {{step[3b].approver_record.approver.name}}. Please consult with your department manager regarding procurement requirements.`
    * `work_notes` = `Request rejected by manager. Approval record: {{step[3b].approver_record.sys_id}}. Flow terminated without task creation.`

---

### Step 17: Send Rejection Email Notification
* **Action Definition**: `send_email`
* **Action Order**: `17`
* **UI ID**: `action_send_rejection_email`
* **Inputs**:
  * `To`: `{{1__request_item.opened_by.email}}`
  * `Subject`: `Procurement Request Rejected - ` + `{{1__request_item.number}}`
  * `Body`:
    ```html
    <p>Dear {{1__request_item.opened_by.first_name}},</p>
    <p>Your recent request for a corporate laptop (<strong>{{1__request_item.number}}</strong>) has been reviewed and was <strong>not approved</strong> by your manager, {{step[3b].approver_record.approver.name}}.</p>
    
    <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 15px 0;">
      <p><strong>Requested Hardware:</strong> {{step[1].variables.laptop_model}}</p>
      <p><strong>Date Evaluated:</strong> {{step[3b].approver_record.sys_updated_on}}</p>
      <p><strong>Reviewer Comments:</strong> {{step[3b].approver_record.comments}}</p>
    </div>
    
    <p>If you believe this decision was made in error or if your hardware requirement has changed, please speak with your manager or submit a revised request via the <a href="https://service-portal.company.com/esc">Service Portal</a>.</p>
    ```

---

## 4. Error Handler Block Configuration

The Flow Designer **Global Error Handler** wraps all 17 actions in a robust try-catch boundary to ensure that no technical fault leaves a ticket in an unmonitored zombie state.

```
+----------------------------------------------------------------------------------------------------+
|                                    FLOW ERROR HANDLER TOPOLOGY                                     |
+----------------------------------------------------------------------------------------------------+
                                                  │
                               [Technical Exception / Action Failure]
                                                  │
                                                  ▼
                        [Step E1: Log Structured Diagnostic via gs.error()]
                                                  │
                                                  ▼
                        [Step E2: Place sc_req_item On Hold (State = -5)]
                                                  │
                                                  ▼
                        [Step E3: Create Priority 2 Incident for Platform Support]
                                                  │
                                                  ▼
                        [Step E4: Dispatch Operational Pager Alert to IT Ops]
+----------------------------------------------------------------------------------------------------+
```

### Step E1: Log Diagnostic Error
* **Action Type**: `core_action_log`
* **Order**: `E1`
* **Inputs**:
  * `Level`: `Error`
  * `Message`:
    ```javascript
    "FLOW_EXECUTION_FAILURE: Flow 'Standard Laptop Procurement Flow' encountered unhandled error on RITM " + 
    {{1__request_item.number}} + " at Step " + {{flow.step_number}} + ". Error Detail: " + {{flow.error_message}}
    ```

### Step E2: Update RITM to Technical Hold
* **Action Type**: `update_record`
* **Order**: `E2`
* **Inputs**:
  * `Record`: `{{1__request_item}}`
  * `Table`: `sc_req_item`
  * `Field Values`:
    * `state` = `-5` (Pending / On Hold)
    * `hold_reason` = `Technical Exception in Workflow Engine`
    * `work_notes` = `CRITICAL EXCEPTION: Automated workflow engine halted at Step {{flow.step_number}} due to error: {{flow.error_message}}. Automatically generating triage Incident for ServiceNow Platform Support.`

### Step E3: Create Triage Incident
* **Action Type**: `create_record`
* **Order**: `E3`
* **Inputs**:
  * `Table`: `incident`
  * `Field Values`:
    * `caller_id` = `System Administrator` (`sys_id: 6816f79cc0a8016400b0ee22381ac541`)
    * `assignment_group` = `ServiceNow Platform Engineering` (`sys_id: d8e9f0a1b2c34567890abcdef1234567`)
    * `impact` = `2` (Medium)
    * `urgency` = `2` (Medium)
    * `priority` = `2` (High)
    * `short_description` = `Flow Failure: Laptop Procurement Workflow on ` + `{{1__request_item.number}}`
    * `description` = `Flow Context ID: {{flow.context_id}}\nRITM: {{1__request_item.number}}\nFailing Step: {{flow.step_number}}\nError Message: {{flow.error_message}}\nRequester: {{1__request_item.opened_by.name}}`

### Step E4: Dispatch Operational Alert Email
* **Action Type**: `send_email`
* **Order**: `E4`
* **Inputs**:
  * `To`: `it_procurement_ops@company.com`, `servicenow_oncall@company.com`
  * `Subject`: `CRITICAL ALERT: Workflow Failure on Laptop Request ` + `{{1__request_item.number}}`
  * `Body`: `A system-level workflow failure occurred during execution of the Standard Laptop Procurement Flow. Incident INC created. Immediate administrative intervention required.`

---

## 5. Data Pill Transformation & Binding Matrix

| Source Step | Source Output Data Pill | Target Action | Target Input Field | Transformation Expression (`fd_transform`) | Rationale |
|---|---|---|---|---|---|
| Step 1 | `{{step[1].variables.laptop_model}}` | Step 7 | `short_description` | `String.concat("Build & Image Laptop: ", {{step[1].variables.laptop_model}})` | Dynamically formats SCTASK title for technician queue |
| Step 0 | `{{1__request_item.opened_by.manager}}`| Step 3B| `approver_users` | `fd_transform.coalesce({{1__request_item.opened_by.manager}}, {{1__request_item.opened_by.department.dept_head}}, "287ee6efe0a2a1509cd4b52b2fd96191")` | Prevents flow stall when user profile manager is null |
| Step 0 | `{{1__request_item.sys_created_on}}`| Step 3B | `due_date` | `fd_transform.date_add_business_days({{1__request_item.sys_created_on}}, 3)` | Calculates 3 business day approval SLA window |
| Step 0 | `{{1__request_item.opened_by.vip}}` | Step 7 | `priority` | `{{1__request_item.opened_by.vip}} ? 2 : 3` | Automatically elevates task urgency for executives |
| Step 6 | `{{step[6].asset_tag}}` | Step 11 | `asset_tag` | `String.trim({{step[6].asset_tag}})` | Ensures whitespace sanitization during asset sync |

---

## 6. Execution Lifecycle Diagnostics & Verification

The flow status and execution steps can be audited via:
1. **Flow Context Record**: Table `sys_flow_context`, query `name=Standard Laptop Procurement Flow^source_record={{sc_req_item.sys_id}}`.
2. **Step Level Executions**: Table `sys_flow_execution_step` detailing microsecond execution duration, input payload, output payload, and condition evaluation.
3. **Execution State Flags**:
   - `WAITING_ON_APPROVAL`: Flow engine paused on Step 3B awaiting event from `sysapproval_approver`.
   - `WAITING_ON_TASK`: Flow engine paused on Step 8 or 10 awaiting state change in `sc_task`.
   - `COMPLETE`: All 14 standard steps finished successfully.
   - `CANCELLED`: Diverted to rejection branch or terminated by administrator.
   - `ERROR`: Main thread aborted and redirected to Global Error Handler.
