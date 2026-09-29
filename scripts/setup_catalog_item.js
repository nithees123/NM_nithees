/**
 * ServiceNow Automated Setup Script
 * Project: Streamlining IT Procurement - Automating Standard Laptop Orders with Flow Designer
 * 
 * Instructions:
 * 1. Navigate to: System Definition > Scripts - Background (in your ServiceNow instance).
 * 2. Paste this entire script into the Run script box.
 * 3. Scope: global
 * 4. Click "Run script".
 */

(function runSetup() {
    gs.info("=== Starting Standard Laptop Procurement Setup ===");

    // 1. Ensure 'Hardware' Assignment Group exists
    var hardwareGroupId = "";
    var grGroup = new GlideRecord("sys_user_group");
    grGroup.addQuery("name", "Hardware");
    grGroup.query();
    if (grGroup.next()) {
        hardwareGroupId = grGroup.getUniqueValue();
        gs.info("[OK] Found existing 'Hardware' Assignment Group: " + hardwareGroupId);
    } else {
        grGroup.initialize();
        grGroup.setValue("name", "Hardware");
        grGroup.setValue("description", "Hardware Fulfillment and Configuration Team");
        hardwareGroupId = grGroup.insert();
        gs.info("[CREATED] 'Hardware' Assignment Group created with sys_id: " + hardwareGroupId);
    }

    // 2. Find Service Catalog & Hardware Category
    var catalogId = "";
    var grCatalog = new GlideRecord("sc_catalog");
    grCatalog.addQuery("title", "Service Catalog");
    grCatalog.query();
    if (grCatalog.next()) {
        catalogId = grCatalog.getUniqueValue();
    }

    var categoryId = "";
    var grCat = new GlideRecord("sc_category");
    grCat.addQuery("title", "Hardware");
    if (catalogId) {
        grCat.addQuery("sc_catalog", catalogId);
    }
    grCat.query();
    if (grCat.next()) {
        categoryId = grCat.getUniqueValue();
        gs.info("[OK] Found 'Hardware' Catalog Category: " + categoryId);
    }

    // 3. Create or Update 'Standard Laptop' Catalog Item
    var catItemId = "";
    var grItem = new GlideRecord("sc_cat_item");
    grItem.addQuery("name", "Standard Laptop");
    grItem.query();
    if (grItem.next()) {
        catItemId = grItem.getUniqueValue();
        gs.info("[OK] Found existing 'Standard Laptop' Catalog Item: " + catItemId);
    } else {
        grItem.initialize();
        grItem.setValue("name", "Standard Laptop");
        grItem.setValue("short_description", "Request a standard corporate laptop with hardware configuration");
        grItem.setValue("description", "Standard corporate laptop for employee productivity. Options include high-performance specifications and enterprise security configuration.");
        if (catalogId) grItem.setValue("sc_catalogs", catalogId);
        if (categoryId) grItem.setValue("category", categoryId);
        grItem.setValue("price", "1200.00");
        grItem.setValue("recurring_price", "0.00");
        grItem.setValue("active", true);
        grItem.setValue("visible_standalone", true);
        catItemId = grItem.insert();
        gs.info("[CREATED] 'Standard Laptop' Catalog Item created with sys_id: " + catItemId);
    }

    // 4. Define Helper to Add Variables
    function createVariable(name, label, type, order, mandatory, referenceTable) {
        var grVar = new GlideRecord("item_option_new");
        grVar.addQuery("cat_item", catItemId);
        grVar.addQuery("name", name);
        grVar.query();
        if (grVar.next()) {
            gs.info("[OK] Variable already exists: " + name);
            return grVar.getUniqueValue();
        }
        grVar.initialize();
        grVar.setValue("cat_item", catItemId);
        grVar.setValue("name", name);
        grVar.setValue("question_text", label);
        grVar.setValue("type", type); // 6=Single Line, 2=Multi-line, 5=Select Box, 8=Reference
        grVar.setValue("order", order);
        grVar.setValue("mandatory", mandatory);
        if (referenceTable) {
            grVar.setValue("reference", referenceTable);
        }
        var varId = grVar.insert();
        gs.info("[CREATED] Variable: " + name + " (" + label + ")");
        return varId;
    }

    function createChoice(variableId, value, text, order) {
        var grChoice = new GlideRecord("question_choice");
        grChoice.addQuery("question", variableId);
        grChoice.addQuery("value", value);
        grChoice.query();
        if (!grChoice.next()) {
            grChoice.initialize();
            grChoice.setValue("question", variableId);
            grChoice.setValue("value", value);
            grChoice.setValue("text", text);
            grChoice.setValue("order", order);
            grChoice.insert();
            gs.info("  [CHOICE] Added option: " + text);
        }
    }

    // 5. Create Variables & Choices
    // Variable: Requested For (Reference to sys_user)
    createVariable("requested_for", "Requested For", 8, 100, true, "sys_user");

    // Variable: Laptop Model (Select Box)
    var modelVarId = createVariable("laptop_model", "Laptop Model", 5, 200, true);
    createChoice(modelVarId, "dell_latitude", "Dell Latitude 5440 (14-inch, Intel Core i7)", 10);
    createChoice(modelVarId, "lenovo_thinkpad", "Lenovo ThinkPad T14 (14-inch, AMD Ryzen 7)", 20);
    createChoice(modelVarId, "macbook_pro", "Apple MacBook Pro 14 (M3 Pro Chip)", 30);

    // Variable: RAM (Select Box)
    var ramVarId = createVariable("ram_size", "RAM Size", 5, 300, true);
    createChoice(ramVarId, "16gb", "16 GB Unified Memory / DDR5", 10);
    createChoice(ramVarId, "32gb", "32 GB Unified Memory / DDR5", 20);

    // Variable: Storage (Select Box)
    var storageVarId = createVariable("storage_capacity", "Storage Capacity", 5, 400, true);
    createChoice(storageVarId, "512gb", "512 GB NVMe SSD", 10);
    createChoice(storageVarId, "1tb", "1 TB NVMe SSD", 20);

    // Variable: Business Justification (Multi-line Text)
    createVariable("business_justification", "Business Justification", 2, 500, true);

    gs.info("=== Setup Completed Successfully! ===");
    gs.info("Standard Laptop sys_id: " + catItemId);
    gs.info("Hardware Assignment Group sys_id: " + hardwareGroupId);
})();
