# 🎙️ Video Presentation & Voiceover Script
**Project Title:** Streamlining IT Procurement: Automating Standard Laptop Orders with Flow Designer  
**Target Video Duration:** ~1 minute 50 seconds  
**Repository:** https://github.com/nithees123/NM_nithees  

---

### **Scene 1: Introduction & Project Overview (00:00 – 00:15)**
* **Visual on Screen:** SkillWallet dashboard showing the project title and milestone Kanban cards.
* **Speaker Script:**
  > *"Hello everyone. Welcome to the demonstration of our ServiceNow project: **Streamlining IT Procurement: Automating Standard Laptop Orders with Flow Designer**.*  
  > *In this project, we address the manual overhead and fulfillment delays in corporate IT procurement by automating standard laptop requests from initial submission to automated hardware task assignment."*

---

### **Scene 2: Milestone 1 – Flow Designer (`Standard laptop task`) (00:15 – 00:38)**
* **Visual on Screen:** Workflow Studio / Flow Designer displaying `Standard laptop task`, green **Active** badge, `Service Catalog` trigger, and `Create Catalog Task` action.
* **Speaker Script:**
  > *"In **Milestone 1**, we designed and activated our core automation engine using ServiceNow Flow Designer.*  
  > *The flow is named **Standard laptop task** under the Global application scope, configured to execute in the System User context.*  
  > *The trigger is set to **Service Catalog**.*  
  > *Under Actions, we added **Create Catalog Task**, linking the Requested Item data pill directly from the trigger. We populated the Short Description with **'Laptop need to Configured'** and automatically routed the assignment to the **Hardware** group.*  
  > *As shown on screen, the flow is fully compiled, published, and **Active**."*

---

### **Scene 3: Milestone 2 – Flow Assignment in Maintain Items (00:38 – 00:55)**
* **Visual on Screen:** Catalog Item form for **Standard Laptop**, clicking the **Process Engine** tab, and highlighting `Flow: Standard laptop task`.
* **Speaker Script:**
  > *"Moving to **Milestone 2**, we mapped this automated workflow to the Service Catalog item.*  
  > *Navigating to **Maintain Items**, we opened the **Standard Laptop** catalog item and switched to the **Process Engine** tab.*  
  > *Here, we assigned our flow **Standard laptop task** as the fulfillment engine, while ensuring that legacy workflows and delivery plans were cleared to prevent execution conflicts."*

---

### **Scene 4: Milestone 3 – Service Catalog Ordering & Approval (00:55 – 01:12)**
* **Visual on Screen:** Service Catalog ordering view, clicking **Order Now**, and viewing Request `REQ0010001` with stage **Request Approved**.
* **Speaker Script:**
  > *"In **Milestone 3**, we verified the end-to-end ordering lifecycle.*  
  > *An employee accesses the Service Catalog, selects **Standard Laptop**, and submits the order by clicking **Order Now**.*  
  > *This creates Request **REQ0010001** and Requested Item **RITM0010001**.*  
  > *Upon manager approval, the approval condition is satisfied, which immediately fires the NowMQ event and triggers our Flow Designer automation."*

---

### **Scene 5: Milestone 3 Verification – Auto-Generated Task (01:12 – 01:35)**
* **Visual on Screen:** Catalog Tasks list showing `SCTASK0010001` and opening the detailed task record.
* **Speaker Script:**
  > *"Here is the automated result. Under **RITM0010001**, our flow automatically generated Catalog Task **SCTASK0010001**.*  
  > *Looking at the record details, the task state is **Open**, the Short Description is automatically populated with **'Laptop need to Configured'**, and it is directly assigned to the **Hardware** group for hardware provisioning and operating system imaging—completely removing manual dispatcher bottlenecks."*

---

### **Scene 6: Conclusion & GitHub Repository Deliverables (01:35 – 01:50)**
* **Visual on Screen:** GitHub repository `nithees123/NM_nithees` scrolling through the project structure, documentation, DOCX/PDF deliverables, and live execution screenshots.
* **Speaker Script:**
  > *"In conclusion, this Flow Designer automation streamlines IT procurement, reduces user wait times, and improves departmental productivity.*  
  > *All project deliverables—including our complete 6-phase documentation, DOCX and PDF deliverables package, flow XML definitions, and live instance execution proofs—are published on our GitHub repository: **`nithees123/NM_nithees`**.*  
  > *Thank you!"*
