# Quality Assurance Test Cases Matrix

**Project:** Streamlining IT Procurement: Automating Standard Laptop Orders with Flow Designer  
**Scope:** Service Catalog, Approval Engine, Flow Designer, Catalog Task Assignment  

---

## 🧪 Test Execution Matrix

| Test ID | Test Scenario | Preconditions | Test Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | **Standard Laptop Form Visibility** | User logged in to ServiceNow Service Portal or Native UI. | 1. Navigate to **Service Catalog > Hardware**.<br>2. Search for "Standard Laptop".<br>3. Open form. | "Standard Laptop" item is visible with model, RAM, storage, and justification variables. | **PASSED** |
| **TC-02** | **Mandatory Fields Validation** | On Standard Laptop order form. | 1. Leave "Business Justification" empty.<br>2. Click "Order Now". | System displays form validation error; submission is blocked until mandatory fields are filled. | **PASSED** |
| **TC-03** | **Order Submission & Record Generation** | Valid form values entered. | 1. Fill all required fields.<br>2. Click "Order Now". | System creates parent `sc_request` (REQ) and child `sc_req_item` (RITM) with stage set to "Approval Requested". | **PASSED** |
| **TC-04** | **Rejection Workflow Handling** | RITM pending approval. | 1. Navigate to RITM approval list.<br>2. Select "Reject" and enter comments. | RITM state updates to "Closed Incomplete" / "Request Cancelled"; Flow Designer does NOT trigger task creation. | **PASSED** |
| **TC-05** | **Automated Task Creation on Approval (Core Objective)** | RITM pending approval. | 1. Open RITM approval.<br>2. Set state to "Approved".<br>3. Save record. | Flow Designer triggers immediately; a new `sc_task` record is automatically inserted under RITM. | **PASSED** |
| **TC-06** | **Hardware Group Assignment & Field Verification** | Catalog Task created by Flow. | 1. Open the generated `sc_task`.<br>2. Inspect Assignment Group.<br>3. Inspect Short Description & Priority. | • `Assignment Group` = **Hardware**<br>• `Short Description` = "Configure and Provision Standard Laptop"<br>• `Priority` = Moderate / Planning. | **PASSED** |

---

## 📋 Acceptance Criteria Checklist

- [x] Service Catalog item named **"Standard Laptop"** created and active.
- [x] Flow Designer configured with trigger on approved RITM.
- [x] Catalog Task automatically generated upon approval.
- [x] Assignment Group set strictly to **"Hardware"**.
- [x] Dynamic hardware options captured and passed into task instructions.
- [x] End-to-end audit trail visible on the Requested Item record.
