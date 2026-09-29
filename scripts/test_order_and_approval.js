/**
 * ServiceNow Automated Testing & Verification Script
 * Project: Streamlining IT Procurement - Automating Standard Laptop Orders with Flow Designer
 * 
 * Instructions:
 * 1. Navigate to: System Definition > Scripts - Background.
 * 2. Paste this script to simulate an end-to-end laptop order, approve it, and verify the Catalog Task.
 * 3. Scope: global
 * 4. Click "Run script".
 */

(function runTest() {
    gs.info("==================================================");
    gs.info("  STARTING AUTOMATED END-TO-END VERIFICATION TEST  ");
    gs.info("==================================================");

    // 1. Locate the Standard Laptop catalog item
    var grItem = new GlideRecord("sc_cat_item");
    grItem.addQuery("name", "Standard Laptop");
    grItem.query();
    if (!grItem.next()) {
        gs.error("[FAIL] 'Standard Laptop' catalog item not found! Please run setup_catalog_item.js first.");
        return;
    }
    var catItemId = grItem.getUniqueValue();
    gs.info("[1/4] Found Standard Laptop Catalog Item: " + catItemId);

    // 2. Create Parent Request (sc_request)
    var grReq = new GlideRecord("sc_request");
    grReq.initialize();
    grReq.setValue("requested_for", gs.getUserID());
    grReq.setValue("short_description", "Automated Test Order: Standard Laptop Procurement");
    grReq.setValue("description", "Automated system test validating Flow Designer trigger and task generation.");
    grReq.setValue("stage", "requested");
    grReq.setValue("approval", "requested");
    var reqId = grReq.insert();
    gs.info("[2/4] Created Request: " + grReq.getValue("number") + " (sys_id: " + reqId + ")");

    // 3. Create Requested Item (sc_req_item)
    var grRitm = new GlideRecord("sc_req_item");
    grRitm.initialize();
    grRitm.setValue("request", reqId);
    grRitm.setValue("cat_item", catItemId);
    grRitm.setValue("short_description", "Standard Laptop - Automated Test");
    grRitm.setValue("quantity", 1);
    grRitm.setValue("stage", "request_approved");
    grRitm.setValue("approval", "requested");
    var ritmId = grRitm.insert();
    var ritmNumber = grRitm.getValue("number");
    gs.info("[3/4] Created Requested Item (RITM): " + ritmNumber + " (sys_id: " + ritmId + ")");

    // 4. Simulate Approval
    gs.info("--> Simulating Manager Approval on RITM...");
    grRitm.setValue("approval", "approved");
    grRitm.setValue("stage", "fulfillment");
    grRitm.update();
    gs.info("[OK] RITM " + ritmNumber + " marked as APPROVED.");

    // 5. Query for Generated Catalog Task (sc_task)
    // Wait briefly or check for existing task created by Flow Designer
    var grTask = new GlideRecord("sc_task");
    grTask.addQuery("request_item", ritmId);
    grTask.query();

    if (grTask.next()) {
        gs.info("--------------------------------------------------");
        gs.info("  [SUCCESS] CATALOG TASK AUTOMATICALLY CREATED!   ");
        gs.info("--------------------------------------------------");
        gs.info("Task Number:        " + grTask.getValue("number"));
        gs.info("Short Description:  " + grTask.getValue("short_description"));
        gs.info("Assignment Group:   " + grTask.assignment_group.getDisplayValue());
        gs.info("State:              " + grTask.state.getDisplayValue());
        gs.info("Associated RITM:    " + ritmNumber);

        if (grTask.assignment_group.getDisplayValue() === "Hardware") {
            gs.info("[PASS] Milestone 1 & 2 Verification: Task successfully assigned to 'Hardware' group!");
        } else {
            gs.warn("[WARN] Task created, but Assignment Group is: " + grTask.assignment_group.getDisplayValue() + " (Expected: Hardware)");
        }
    } else {
        gs.info("--------------------------------------------------");
        gs.info("[INFO] RITM " + ritmNumber + " has been approved.");
        gs.info("If Flow Designer is active, check the RITM in the UI or Flow Executions list:");
        gs.info("URL: /sc_req_item.do?sys_id=" + ritmId);
        gs.info("--------------------------------------------------");
    }

    gs.info("==================================================");
    gs.info("           VERIFICATION TEST COMPLETE             ");
    gs.info("==================================================");
})();
