# Flow Designer Configuration Guide

This guide provides step-by-step instructions for building the **Standard Laptop Procurement Automation Flow** in ServiceNow Flow Designer.

---

## 🎯 Flow Overview

* **Flow Name:** `Standard Laptop Procurement Flow`
* **Application Scope:** `Global`
* **Trigger:** When a `Requested Item (sc_req_item)` is Approved for the `Standard Laptop` catalog item.
* **Primary Action:** Automatically create a `Catalog Task (sc_task)` assigned to the **Hardware** group with specifications and instructions.

---

## 🛠️ Step-by-Step Instructions

### Step 1: Open Flow Designer
1. In the ServiceNow filter navigator, type `Flow Designer`.
2. Click **Process Automation > Flow Designer**.
3. In the Flow Designer header, click **+ New** > **Flow**.
4. Fill in the Flow Properties:
   * **Flow name:** `Standard Laptop Procurement Flow`
   * **Description:** `Automates task creation and routing to the Hardware team upon approval of a Standard Laptop request.`
   * **Application:** `Global`
   * **Run As:** `System User` (or `User who initiates session`)
5. Click **Submit**.

---

### Step 2: Configure the Trigger
1. In the **Trigger** section, click **Add a Trigger**.
2. Select **Record > Updated** (or **Service Catalog** depending on your design preference):
   * **Table:** `Requested Item [sc_req_item]`
   * **Condition:**
     * `[Item] [is] [Standard Laptop]`
     * `AND`
     * `[Approval] [changes to] [Approved]`
3. Click **Done**.

> **Alternative (Service Catalog Trigger):**
> If using `Trigger: Service Catalog`:
> 1. Add action: **Flow Logic > If** (`Approval is Approved`).
> 2. Or add action: **Service Catalog > Get Catalog Variables**.

---

### Step 3: Add Action 1 – Update Requested Item State
1. Under **Actions**, click **+ Add an Action, Flow Logic, or Subflow**.
2. Click **Action** > **ServiceNow Core** > **Update Record**.
3. Drag the **Requested Item Record** data pill from the right panel into the **Record** field.
4. Under **Fields**, click **+ Add Field Value**:
   * **Field:** `State`
   * **Value:** `Work in Progress`
5. Click **Done**.

---

### Step 4: Add Action 2 – Create Catalog Task (Milestone 1 Core Requirement)
1. Click **+ Add an Action, Flow Logic, or Subflow** below Step 3.
2. Select **Action** > **Service Catalog** > **Create Catalog Task** (or **ServiceNow Core > Create Record** on table `sc_task`).
3. Configure the task fields:
   * **Requested Item:** Drag data pill `Trigger - Record Updated > Requested Item Record`.
   * **Short Description:** `Configure and Provision Standard Laptop`
   * **Assignment Group:** `Hardware`
   * **Priority:** `3 - Moderate`
   * **Description:** Click the data pill picker or type:
     ```text
     Please configure and provision the approved standard laptop according to user specifications:
     - Requested For: [Requested Item Record > Requested for]
     - Item: Standard Laptop
     - Instructions: Verify asset tagging, install standard enterprise software stack, and prepare for shipment/pickup.
     ```
4. Click **Done**.

---

### Step 5: Save and Activate
1. Click **Save** in the top right corner.
2. Click **Test** to run a test execution against an existing RITM (optional).
3. Click **Activate** to make the flow live in your ServiceNow environment.

---

### Step 6: Link Flow to Catalog Item (Milestone 2)
1. Go back to the main ServiceNow browser tab.
2. In the navigator, go to **Service Catalog > Catalog Definitions > Maintain Items**.
3. Search for and open **Standard Laptop**.
4. In the form, scroll to the **Process Engine** tab.
5. In the **Flow** field, select **Standard Laptop Procurement Flow**.
6. Clear the **Workflow** field if populated (Flow takes precedence over legacy workflows).
7. Click **Update** to save the item.

---

## 🔍 Execution Verification
Once active, whenever a user orders a Standard Laptop:
1. Manager marks the RITM as **Approved**.
2. Flow Designer immediately fires.
3. In the RITM related list under **Catalog Tasks**, you will see:
   * **Number:** `TASK00XXXXX`
   * **Short Description:** `Configure and Provision Standard Laptop`
   * **Assignment Group:** `Hardware`
   * **State:** `Open`
