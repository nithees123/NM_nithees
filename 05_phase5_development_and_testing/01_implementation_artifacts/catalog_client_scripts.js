/**
 * ServiceNow Catalog Client Scripts: Standard Laptop Procurement
 * 
 * Target Catalog Item: Standard Business Laptop Request (sys_id: 0b36816197113110a24734000153af45)
 * Scope: Global
 * Architecture: Asynchronous callbacks, strict input validation, responsive UI messaging
 * Author: worker_phase5 (Phase 5 Development & Testing Lead)
 * Target Release: Washington DC / Xanadu / Utah
 */

/* ==============================================================================================
   SCRIPT 1: OnChange — Auto-Populate Requester Demographics & Detect VIP Fast-Track
   Table / Target: Catalog Item Variable [requested_for] (or [employee_name])
   Type: onChange
   UI Type: All (Desktop, Service Portal, Mobile / Now Mobile)
   ============================================================================================== */
function onChange(control, oldValue, newValue, isLoading) {
    // If the form is loading or the field was cleared, reset dependent fields cleanly
    if (isLoading) {
        return;
    }

    if (newValue === '') {
        g_form.setValue('department', '');
        g_form.setValue('manager_name', '');
        g_form.setValue('job_title', '');
        g_form.hideFieldMsg('requested_for');
        return;
    }

    // Asynchronous reference retrieval to prevent UI thread lock
    g_form.getReference('requested_for', function(userRecord) {
        if (!userRecord) {
            return;
        }

        // 1. Auto-populate Department, Manager, and Job Title
        if (userRecord.department) {
            g_form.setValue('department', userRecord.department);
        } else {
            g_form.setValue('department', '');
        }

        if (userRecord.manager) {
            g_form.setValue('manager_name', userRecord.manager);
        } else {
            g_form.setValue('manager_name', '');
            g_form.showFieldMsg('requested_for', 
                'Notice: No direct manager assigned in your profile. Request will route to Department Head.', 
                'warning'
            );
        }

        if (userRecord.title) {
            g_form.setValue('job_title', userRecord.title);
        } else {
            g_form.setValue('job_title', '');
        }

        // 2. VIP / Executive Detection & White-Glove Fast-Track Notification
        var isVip = (userRecord.vip === 'true' || userRecord.vip === true);
        var title = userRecord.title ? userRecord.title.toLowerCase() : '';
        var isExecutiveTitle = (title.indexOf('vice president') > -1 || 
                                title.indexOf('director') > -1 || 
                                title.indexOf('chief') > -1 || 
                                title.indexOf('president') > -1);

        g_form.hideFieldMsg('requested_for');

        if (isVip || isExecutiveTitle) {
            g_form.showFieldMsg(
                'requested_for', 
                '★ VIP / Executive Account Detected: This request qualifies for White-Glove Fast-Track Auto-Approval (24-Hour SLA).', 
                'info'
            );
        }
    });
}


/* ==============================================================================================
   SCRIPT 2: OnChange — Dynamic Model Filter & Technical Specifications Summary Display
   Table / Target: Catalog Item Variable [asset_type] and [laptop_model]
   Type: onChange
   UI Type: All (Desktop, Service Portal, Mobile)
   ============================================================================================== */

/**
 * Triggered on change of [asset_type] to dynamically rebuild [laptop_model] choices
 */
function onChangeAssetType(control, oldValue, newValue, isLoading) {
    if (isLoading) {
        return;
    }

    g_form.clearOptions('laptop_model');
    g_form.addOption('laptop_model', '', '-- Select Laptop Model --');

    if (newValue === 'standard') {
        g_form.addOption('laptop_model', 'lenovo_t14', 'Lenovo ThinkPad T14 Gen 4 (Core i7, 16GB, 512GB)');
        g_form.addOption('laptop_model', 'dell_5440', 'Dell Latitude 5440 (Core i7, 16GB, 512GB)');
        g_form.setValue('laptop_model', 'lenovo_t14'); // Default choice
    } else if (newValue === 'engineering') {
        g_form.addOption('laptop_model', 'lenovo_p1', 'Lenovo ThinkPad P1 Gen 6 (Core i9, 32GB, 1TB, RTX 4060)');
        g_form.addOption('laptop_model', 'macbook_pro_14', 'Apple MacBook Pro 14" M3 Pro (36GB Unified, 1TB SSD)');
        g_form.setValue('laptop_model', 'lenovo_p1');
    } else if (newValue === 'executive') {
        g_form.addOption('laptop_model', 'hp_dragonfly', 'HP Elite Dragonfly G4 Ultra-Light (1kg, 32GB, 1TB)');
        g_form.addOption('laptop_model', 'macbook_air_15', 'Apple MacBook Air 15" M3 (24GB Unified, 512GB SSD)');
        g_form.setValue('laptop_model', 'hp_dragonfly');
    }
}

/**
 * Triggered on change of [laptop_model] to display rich hardware specs banner
 */
function onChangeLaptopModel(control, oldValue, newValue, isLoading) {
    if (isLoading) {
        return;
    }

    g_form.hideFieldMsg('laptop_model');

    if (newValue === '') {
        return;
    }

    // Comprehensive hardware specification catalog dictionary
    var specsDictionary = {
        'lenovo_t14': 'Hardware Specs: Intel Core i7-1365U vPro | 16GB DDR5 5600MHz | 512GB PCIe 4.0 NVMe | 14" WUXGA IPS (1920x1200) | 1.36 kg | Windows 11 Enterprise | Standard Approval Required',
        'dell_5440': 'Hardware Specs: Intel Core i7-1365U vPro | 16GB DDR5 5600MHz | 512GB PCIe 4.0 NVMe | 14" FHD Anti-Glare (1920x1080) | 1.39 kg | Windows 11 Enterprise | Standard Approval Required',
        'lenovo_p1': 'Hardware Specs: Intel Core i9-13900H (14-Core) | 32GB DDR5 5600MHz | 1TB PCIe 4.0 NVMe | NVIDIA RTX 4060 8GB | 16" WQXGA 165Hz | Windows 11 Pro / Ubuntu LTS | Business Justification Required',
        'macbook_pro_14': 'Hardware Specs: Apple M3 Pro (12-Core CPU, 18-Core GPU) | 36GB Unified Memory | 1TB NVMe SSD | 14.2" Liquid Retina XDR 120Hz | macOS Sonoma | Business Justification Required',
        'hp_dragonfly': 'Hardware Specs: Intel Core i7-1365U vPro | 32GB LPDDR5 | 1TB NVMe Gen 4 | 13.5" WUXGA+ (1920x1280) 1000 nits SureView Privacy | 0.99 kg | Windows 11 Enterprise | Executive Tier',
        'macbook_air_15': 'Hardware Specs: Apple M3 (8-Core CPU, 10-Core GPU) | 24GB Unified Memory | 512GB NVMe SSD | 15.3" Liquid Retina True Tone | 1.51 kg | macOS Sonoma | Executive Tier'
    };

    if (specsDictionary[newValue]) {
        g_form.showFieldMsg('laptop_model', specsDictionary[newValue], 'info');
    }
}


/* ==============================================================================================
   SCRIPT 3: OnSubmit — Rigorous Form Integrity, Address & Justification Validation
   Table / Target: Catalog Item Form Level
   Type: onSubmit
   UI Type: All (Desktop, Service Portal, Mobile)
   ============================================================================================== */
function onSubmit() {
    var hasError = false;

    // Clear any previous error messages
    g_form.clearMessages();

    var shippingType = g_form.getValue('shipping_type');
    var shippingAddress = g_form.getValue('shipping_address');
    var assetType = g_form.getValue('asset_type');
    var laptopModel = g_form.getValue('laptop_model');
    var justification = g_form.getValue('business_justification');
    var replacementReason = g_form.getValue('replacement_reason');
    var assetTag = g_form.getValue('existing_asset_tag') || g_form.getValue('asset_tag');

    // -------------------------------------------------------------------------
    // Rule 1: Validate Physical Shipping Address for Remote Delivery
    // -------------------------------------------------------------------------
    if (shippingType === 'remote_shipment') {
        if (!shippingAddress || shippingAddress.trim().length < 15) {
            g_form.showFieldMsg(
                'shipping_address', 
                'Incomplete Address: Home delivery requires street address, apartment/suite (if any), city, state, and 5-digit ZIP code.', 
                'error'
            );
            g_form.addErrorMessage('Validation Failed: Please provide a complete physical shipping address for remote dispatch.');
            hasError = true;
        } else {
            // Regex check: Must contain at least a number, street letters, and a 5-digit postal code
            var postalCodeRegex = /\b\d{5}(-\d{4})?\b/;
            if (!postalCodeRegex.test(shippingAddress)) {
                g_form.showFieldMsg(
                    'shipping_address', 
                    'Missing Postal Code: Shipping address must contain a valid 5-digit US ZIP code.', 
                    'error'
                );
                g_form.addErrorMessage('Validation Failed: Shipping address lacks a valid postal/ZIP code.');
                hasError = true;
            }
        }
    }

    // -------------------------------------------------------------------------
    // Rule 2: Enforce Business Justification for Developer & Executive Models
    // -------------------------------------------------------------------------
    var isHighTierModel = (assetType === 'engineering' || 
                           assetType === 'executive' || 
                           laptopModel === 'lenovo_p1' || 
                           laptopModel === 'macbook_pro_14' || 
                           laptopModel === 'hp_dragonfly' || 
                           laptopModel === 'macbook_air_15');

    if (isHighTierModel) {
        if (!justification || justification.trim().length < 20) {
            g_form.showFieldMsg(
                'business_justification', 
                'Justification Too Brief: Engineering and Executive models require detailed technical or business justification (minimum 20 characters).', 
                'error'
            );
            g_form.addErrorMessage('Validation Failed: Please provide a detailed business justification explaining why standard tier hardware does not satisfy role requirements.');
            hasError = true;
        }
    }

    // -------------------------------------------------------------------------
    // Rule 3: Enforce Asset Tag Format for Refresh or Damaged Replacement
    // -------------------------------------------------------------------------
    if (replacementReason === 'refresh' || replacementReason === 'damaged') {
        if (!assetTag || assetTag.trim() === '') {
            g_form.showFieldMsg(
                'existing_asset_tag', 
                'Mandatory Asset Tag: Hardware refresh and damaged replacements require the asset tag of the retiring unit.', 
                'error'
            );
            g_form.addErrorMessage('Validation Failed: Existing Asset Tag is required for hardware refresh/swap.');
            hasError = true;
        } else {
            // Asset tag regex format: e.g., AST-12345 or 4 to 15 alphanumeric characters
            var assetTagRegex = /^[A-Za-z0-9\-_]{4,15}$/;
            if (!assetTagRegex.test(assetTag.trim())) {
                g_form.showFieldMsg(
                    'existing_asset_tag', 
                    'Invalid Format: Asset Tag must be 4-15 alphanumeric characters (e.g., AST-99482).', 
                    'error'
                );
                g_form.addErrorMessage('Validation Failed: Existing Asset Tag format is invalid.');
                hasError = true;
            }
        }
    }

    // Block submission if any validation failure occurred
    if (hasError) {
        return false;
    }

    return true;
}
