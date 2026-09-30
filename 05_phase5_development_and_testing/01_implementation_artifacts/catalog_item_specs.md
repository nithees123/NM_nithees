# ServiceNow Service Catalog Item Specification: Standard Laptop Order

**Document Identifier**: CAT-SPEC-P5-002  
**Catalog Item Name**: `Standard Business Laptop Request` (Display Name: `Standard Laptop Order`)  
**Application Scope**: `Global` (`global`)  
**Catalog Item Sys ID**: `0b36816197113110a24734000153af45`  
**Target Release**: ServiceNow Washington DC / Xanadu / Utah  
**Author**: worker_phase5 (Phase 5 Development & Testing Lead)  
**Status**: Active & Available in Service Portal  

---

## 1. Catalog Item Definition & Metadata

```
+----------------------------------------------------------------------------------------------------+
|                                 CATALOG ITEM PRESENTATION OVERVIEW                                 |
+----------------------------------------------------------------------------------------------------+
| Portal View: /esc?id=sc_cat_item&sys_id=0b36816197113110a24734000153af45                          |
|                                                                                                    |
|  [Icon: Laptop]  Standard Laptop Order                                                             |
|                  Category: Hardware > Computers | Delivery: 3-5 Business Days                      |
|                  Base Price: $1,250.00 USD (Recurring: $0.00)                                      |
|                                                                                                    |
|  +-- SECTION 1: REQUESTER INFORMATION ----------------------------------------------------------+  |
|  | * Requested For: [ Marcus Vance          ] (Auto-populated from logged-in session)           |  |
|  |   Department:    [ Sales Engineering     ] (Read-Only, derived from sys_user)                |  |
|  |   Manager:       [ Sarah Jenkins         ] (Read-Only, derived from sys_user)                |  |
|  |   Job Title:     [ Senior Sales Engineer ] (Read-Only, derived from sys_user)                |  |
|  +----------------------------------------------------------------------------------------------+  |
|                                                                                                    |
|  +-- SECTION 2: HARDWARE SPECIFICATION ---------------------------------------------------------+  |
|  | * Hardware Tier: (o) Standard Business   ( ) Developer/Engineering   ( ) Executive Ultra-Light|  |
|  | * Laptop Model:  [ Lenovo ThinkPad T14 Gen 4 (Core i7, 16GB, 512GB)                        v ]|  |
|  | * Request Type:  ( ) New Hire   (o) 3-Year Lifecycle Refresh   ( ) Damaged/Lost              |  |
|  | * Existing Asset Tag: [ AST-99482        ] (Mandatory for hardware refresh/swap)             |  |
|  | * Justification:      [ Developer build requires additional compute resources...           ]  |  |
|  |   (Dynamically mandatory for Developer & Executive tiers)                                     |  |
|  +----------------------------------------------------------------------------------------------+  |
|                                                                                                    |
|  +-- SECTION 3: SHIPPING & FULFILLMENT ---------------------------------------------------------+  |
|  | * Delivery Method: ( ) Office Desk Drop   (o) Remote Home Delivery                           |  |
|  | * Shipping Address: [ 742 Evergreen Terrace, Springfield, OR 97477                          ]  |  |
|  |   (Dynamically visible and mandatory when Remote Home Delivery is selected)                  |  |
|  |   Peripheral Bundle: [x] Dual 27" 4K Monitors  [x] USB-C Thunderbolt Dock  [ ] Ergonomic Arm |  |
|  +----------------------------------------------------------------------------------------------+  |
|                                                                                                    |
|                                              [ Save as Draft ]   [ Order Now / Submit Request ]    |
+----------------------------------------------------------------------------------------------------+
```

### 1.1 Item Identification & System Properties
* **Name**: `Standard Business Laptop Request`
* **Short Description**: Standard corporate laptop procurement for employee onboarding and hardware lifecycle refresh.
* **Category**: `Hardware > Computers` (`sys_id: e15706fc0a0a0aa7007fc21e1ab70c2f`)
* **Catalogs**: `Service Catalog` (`sys_id: e0d08b13c3330100c8b837659bba8fb4`)
* **Active**: `true`
* **Workflow Engine**: `Flow Designer`
* **Process Flow**: `Standard Laptop Procurement Flow` (`sys_hub_flow_7e36816197113110a24734000153af22`)
* **Availability**: Desktop, Tablet, Mobile (Responsive Service Portal / ESC)
* **Order / Display Sequence**: `100`
* **Owner**: `IT Hardware Procurement Team` (`sys_user_group: IT Procurement Approvers`)
* **Base Pricing Model**:
  * Standard Business Tier: `$1,250.00 USD`
  * Developer / Engineering Tier: `$2,150.00 USD`
  * Executive Ultra-Light Tier: `$2,450.00 USD`
* **Recurring Price**: `$0.00`
* **Fulfillment Target / SLA**: 72 Business Hours (Standard); 24 Business Hours (Executive VIP)
* **Entitlements / User Criteria**:
  * `Available For`: Any active user with role `snc_internal`
  * `Not Available For`: External contractors without organizational sponsorship (`snc_external`)

---

## 2. Complete Variable Dictionary (`item_option_new`)

The catalog item utilizes structured container formatting, reference qualifiers, dynamic dependencies, and regex validation rules across 13 configuration variables.

| Variable Name | Variable Type | Order | Mandatory | Read-Only | Reference Table / Choices | Default Value / Dynamic Logic | Field Help & Tooltip |
|---|---|---|---|---|---|---|---|
| `sec_requester_start` | Container Start | `100` | No | No | N/A | 2-Column Layout (`split=true`) | Section wrapper for employee demographics |
| `requested_for` | Reference | `110` | **Yes** | No | `sys_user` (`active=true`) | `javascript:gs.getUserID()` | Employee receiving the hardware asset |
| `department` | Reference | `120` | No | **Yes** | `cmn_department` | Auto-populated via Client Script from `requested_for.department` | Cost center and billing allocation department |
| `manager_name` | Reference | `130` | No | **Yes** | `sys_user` | Auto-populated via Client Script from `requested_for.manager` | Approving people manager responsible for fiscal sign-off |
| `job_title` | Single-Line Text | `140` | No | **Yes** | N/A | Auto-populated via Client Script from `requested_for.title` | Employee corporate role |
| `sec_requester_end` | Container End | `190` | No | No | N/A | N/A | End of Requester Section |
| `sec_hardware_start` | Container Start | `200` | No | No | N/A | 2-Column Layout (`split=true`) | Section wrapper for device technical specs |
| `asset_type` | Select Box | `210` | **Yes** | No | Choices:<br>• `standard` (General Business)<br>• `engineering` (Developer / Data Science)<br>• `executive` (Ultra-Light VIP) | `standard` | Determines laptop hardware tier and approval threshold |
| `laptop_model` | Select Box | `220` | **Yes** | No | Dynamic Choices (dependent on `asset_type`):<br>• `lenovo_t14`: Lenovo ThinkPad T14 Gen 4<br>• `dell_5440`: Dell Latitude 5440<br>• `lenovo_p1`: Lenovo ThinkPad P1 Gen 6 (Dev)<br>• `macbook_pro_14`: Apple MacBook Pro 14" M3 Pro<br>• `hp_dragonfly`: HP Elite Dragonfly G4 (Exec)<br>• `macbook_air_15`: Apple MacBook Air 15" M3 (Exec) | `-- None --` | Specific OEM model and configuration package |
| `replacement_reason`| Multiple Choice | `230` | **Yes** | No | Choices:<br>• `new_hire` (New Hire / Additional Asset)<br>• `refresh` (Standard 3-Year Refresh)<br>• `damaged` (Damaged / Hardware Failure)<br>• `stolen` (Stolen / Lost Hardware) | `refresh` | Business justification reason for procurement |
| `asset_tag` / `existing_asset_tag` | Single-Line Text | `240` | Conditional | No | N/A | None | Mandatory if `replacement_reason` is Refresh or Damaged |
| `business_justification` | Multi-Line Text | `250` | Conditional | No | N/A | None | Mandatory for Developer models and Executive Ultra-Light tier |
| `sec_hardware_end` | Container End | `290` | No | No | N/A | N/A | End of Hardware Section |
| `sec_shipping_start`| Container Start | `300` | No | No | N/A | 1-Column Layout | Section wrapper for delivery and logistics |
| `shipping_type` | Select Box | `310` | **Yes** | No | Choices:<br>• `office_desk` (Campus Desk Drop)<br>• `remote_shipment` (Home / Remote Delivery) | `office_desk` | Delivery location method |
| `shipping_address` | Multi-Line Text | `320` | Conditional | No | N/A | None | Mandatory when `shipping_type == 'remote_shipment'` |
| `accessories` | List Collector | `330` | No | No | Table: `cmdb_model`<br>Filter: `cmdb_model_category=Peripherals^active=true` | Dual 27" Monitors, USB-C Dock, Backpack, Wireless Mouse | Optional productivity hardware peripherals |
| `sec_shipping_end` | Container End | `390` | No | No | N/A | N/A | End of Shipping Section |

---

## 3. Catalog UI Policies (`sys_ui_policy`)

Catalog UI Policies dynamically govern the behavior, visibility, and mandatory state of variables without writing custom client scripts.

### 3.1 UI Policy 1: Remote Shipping Address Visibility & Mandatory Enforcement
* **Sys ID**: `a136816197113110a24734000153af91`
* **Short Description**: `Show and Enforce Address for Remote Shipment`
* **Catalog Item**: `Standard Business Laptop Request`
* **On Load**: `true`
* **Reverse if False**: `true`
* **Condition**:
  * Variable: `shipping_type`
  * Operator: `is`
  * Value: `remote_shipment`
* **UI Policy Actions (`sys_ui_policy_action`)**:
  | Target Variable | Mandatory | Visible | Read-Only | Clear Value when Hidden |
  |---|---|---|---|---|
  | `shipping_address` | **Mandatory: True** | **Visible: True** | Read-Only: False | **Clear Value: True** |

---

### 3.2 UI Policy 2: Mandatory Business Justification for Developer & Executive Models
* **Sys ID**: `b136816197113110a24734000153af92`
* **Short Description**: `Require Justification for Developer and Executive Laptops`
* **Catalog Item**: `Standard Business Laptop Request`
* **On Load**: `true`
* **Reverse if False**: `true`
* **Condition**:
  * Variable: `asset_type` IS `engineering`
  * *OR*
  * Variable: `asset_type` IS `executive`
  * *OR*
  * Variable: `laptop_model` IS ONE OF `('lenovo_p1', 'macbook_pro_14', 'hp_dragonfly', 'macbook_air_15')`
* **UI Policy Actions (`sys_ui_policy_action`)**:
  | Target Variable | Mandatory | Visible | Read-Only | Clear Value when Hidden |
  |---|---|---|---|---|
  | `business_justification` | **Mandatory: True** | **Visible: True** | Read-Only: False | Clear Value: False |

---

### 3.3 UI Policy 3: Enforce Read-Only Requester Organizational Fields
* **Sys ID**: `c136816197113110a24734000153af93`
* **Short Description**: `Lock Requester Demographic Fields to Read-Only`
* **Catalog Item**: `Standard Business Laptop Request`
* **On Load**: `true`
* **Reverse if False**: `false`
* **Condition**: `None` (Executes unconditionally on form load)
* **UI Policy Actions (`sys_ui_policy_action`)**:
  | Target Variable | Mandatory | Visible | Read-Only | Clear Value when Hidden |
  |---|---|---|---|---|
  | `department` | Leave alone | Visible: True | **Read-Only: True** | Leave alone |
  | `manager_name` | Leave alone | Visible: True | **Read-Only: True** | Leave alone |
  | `job_title` | Leave alone | Visible: True | **Read-Only: True** | Leave alone |

---

### 3.4 UI Policy 4: Enforce Asset Tag for Hardware Refresh / Replacement
* **Sys ID**: `d136816197113110a24734000153af94`
* **Short Description**: `Require Existing Asset Tag on Refresh or Hardware Failure`
* **Catalog Item**: `Standard Business Laptop Request`
* **On Load**: `true`
* **Reverse if False**: `true`
* **Condition**:
  * Variable: `replacement_reason` IS `refresh`
  * *OR*
  * Variable: `replacement_reason` IS `damaged`
* **UI Policy Actions (`sys_ui_policy_action`)**:
  | Target Variable | Mandatory | Visible | Read-Only | Clear Value when Hidden |
  |---|---|---|---|---|
  | `existing_asset_tag` | **Mandatory: True** | **Visible: True** | Read-Only: False | Clear Value: True |

---

## 4. Hardware Model Technical Specification Matrix

The following hardware options are dynamically presented to the requester based on selected `asset_type`:

| Model Identifier | Display Label | Processor / Architecture | RAM & Storage | Display & GPU | Target Personnel & Base Cost |
|---|---|---|---|---|---|
| `lenovo_t14` | Lenovo ThinkPad T14 Gen 4 | Intel Core i7-1365U (10-Core vPro) | 16GB DDR5 5600MHz / 512GB NVMe PCIe 4.0 | 14" WUXGA (1920x1200) IPS, Intel Iris Xe | Standard Business Users, Sales, HR, Finance (`$1,250.00`) |
| `dell_5440` | Dell Latitude 5440 | Intel Core i7-1365U (10-Core vPro) | 16GB DDR5 5600MHz / 512GB NVMe PCIe 4.0 | 14" FHD (1920x1080) Anti-Glare, Intel Iris Xe | Standard Business Users, Operations (`$1,220.00`) |
| `lenovo_p1` | Lenovo ThinkPad P1 Gen 6 | Intel Core i9-13900H (14-Core) | 32GB DDR5 5600MHz / 1TB NVMe PCIe 4.0 | 16" WQXGA (2560x1600) 165Hz, NVIDIA RTX 4060 8GB | Software Engineers, Architects, Data Scientists (`$2,150.00`) |
| `macbook_pro_14`| Apple MacBook Pro 14" M3 Pro | Apple M3 Pro (12-Core CPU, 18-Core GPU) | 36GB Unified Memory / 1TB Ultra-Fast SSD | 14.2" Liquid Retina XDR (3024x1964) 120Hz ProMotion | iOS/Mobile Developers, Senior Engineering (`$2,399.00`) |
| `hp_dragonfly` | HP Elite Dragonfly G4 | Intel Core i7-1365U vPro | 32GB LPDDR5 / 1TB NVMe Gen 4 SSD | 13.5" WUXGA+ (1920x1280) BrightView 1000 nits, SureView Privacy | Vice Presidents, Directors, C-Suite Executives (`$2,450.00`) |
| `macbook_air_15`| Apple MacBook Air 15" M3 | Apple M3 (8-Core CPU, 10-Core GPU) | 24GB Unified Memory / 512GB SSD | 15.3" Liquid Retina (2880x1864) True Tone | Traveling Executives, Marketing Leadership (`$1,899.00`) |

---

## 5. Portal Widget & Client Side Validation Configuration

1. **Service Portal Widget**: Standard `SC Catalog Item` (`widget-sc-cat-item`).
2. **Order Guide Integration**: Fully compatible with `New Employee Onboarding Order Guide` via variable cascading (`cascade=true`).
3. **Draft Capabilities**: Enables `Save as Draft` via ServiceNow platform preferences.
4. **Variable Sets**: Can be decoupled into two reusable variable sets:
   - `VS_Requester_Demographics` (`sys_id: 8b36816197113110a24734000153af11`)
   - `VS_IT_Shipping_Address` (`sys_id: 8b36816197113110a24734000153af12`)
