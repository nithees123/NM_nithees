# ServiceNow Project Demo Video Script (2–3 Minutes)

**Project Title:** Streamlining IT Procurement: Automating Standard Laptop Orders with Flow Designer  
**Program:** ServiceNow System Administrator – SmartBridge / SkillWallet Virtual Internship  
**Team Members:** Monish S (Team Lead), Nitheeswaran S, Pooja Shree, Yugesh Kumar J  

---

## 🎬 Video Recording Guide

* **Target Duration:** 2 minutes 30 seconds to 3 minutes.
* **Recording Tool:** OBS Studio, Loom, or Zoom (Record to computer).
* **Format:** Screen recording showing ServiceNow instance + voiceover.

---

## 🎙️ Spoken Presentation Script

### 0:00 – 0:35 | Speaker 1: Monish S (Team Lead)
**On Screen:** *Title slide showing Project Name, Team Members, and Architecture Diagram.*

> "Hello everyone, my name is Monish S, and I am the Team Lead for this project alongside my teammates Nitheeswaran S, Pooja Shree, and Yugesh Kumar J. 
> 
> Our project is **'Streamlining IT Procurement: Automating Standard Laptop Orders with Flow Designer'**. 
> In traditional IT organizations, ordering a laptop involves manual email approvals, delayed handoffs, and manual ticket creation. Our goal was to eliminate manual triage entirely using ServiceNow's low-code Flow Designer. 
> 
> When an employee requests a laptop and their manager approves it, the system immediately and automatically generates a Catalog Task and routes it directly to the Hardware configuration team. Let's see how we built and demonstrated this solution."

---

### 0:35 – 1:15 | Speaker 2: Pooja Shree (Service Catalog Design & Ordering)
**On Screen:** *Navigate to ServiceNow Service Catalog > Hardware > Standard Laptop.*

> "Thank you, Monish. I'm Pooja Shree, and I worked on the **Service Catalog** design and request submission. 
> 
> As you can see on the screen, under **Service Catalog > Hardware**, we created the **Standard Laptop** catalog item. 
> The form includes essential user variables: the **Requested For** user, a choice of laptop models like Dell Latitude, Lenovo ThinkPad, or MacBook Pro, configurable **RAM**, **Storage**, and a mandatory **Business Justification**. 
> 
> When I click **'Order Now'**, ServiceNow creates a Request (REQ) and a Requested Item (RITM). Initially, the RITM enters the **Approval Requested** stage. Now, Nitheeswaran will explain how the flow takes over once approval occurs."

---

### 1:15 – 2:05 | Speaker 3: Nitheeswaran S (Flow Designer & Automation)
**On Screen:** *Navigate to Flow Designer > Open 'Standard Laptop Procurement Flow'. Show trigger and actions.*

> "Hello everyone, I am Nitheeswaran S. My focus was on **Milestone 1 and 2: Flow Designer Automation and Flow Assignment**.
> 
> Here in **Flow Designer**, we created the **Standard Laptop Procurement Flow**. 
> The trigger is set on the **Requested Item** table: whenever the item is 'Standard Laptop' and the Approval state changes to **Approved**, the flow automatically executes.
> 
> First, it updates the RITM state to **'Work in Progress'**. 
> Next, it executes the core requirement: **'Create Catalog Task'**. It dynamically assigns the task to the **Hardware** assignment group, sets the short description to *'Configure and Provision Standard Laptop'*, and attaches the user's specific hardware selections. 
> 
> We then associated this flow directly into the Process Engine of the Standard Laptop catalog definition. Now Yugesh will demonstrate the live execution."

---

### 2:05 – 2:50 | Speaker 4: Yugesh Kumar J (Verification & Conclusion)
**On Screen:** *Open the approved RITM, scroll down to the Catalog Tasks related list, and click open the task.*

> "Thank you, Nitheeswaran. I am Yugesh Kumar J. For the final milestone, we verified the complete end-to-end execution. 
> 
> As you can see on my screen, we simulate the manager approval by marking the RITM as **Approved**. 
> Within seconds, under the **Catalog Tasks** related list, a new task has been automatically generated!
> 
> When we open this task, notice that:
> 1. The **Assignment Group** is populated as **'Hardware'**.
> 2. The **Short Description** is automatically populated with the configuration instructions.
> 3. Zero manual intervention was needed from any IT dispatcher. 
> 
> This automation speeds up procurement fulfillment from hours down to seconds, prevents human routing errors, and provides full transparency for both the employee and IT management. Thank you for your time!"

---

## 📤 Submission Checklist
- [ ] Record the video using the script above.
- [ ] Upload video to YouTube (as *Unlisted*) or Google Drive (set access to *Anyone with the link can view*).
- [ ] Copy the video link.
- [ ] Have Team Lead (Monish S) submit the video link and GitHub repository link into SkillWallet.
