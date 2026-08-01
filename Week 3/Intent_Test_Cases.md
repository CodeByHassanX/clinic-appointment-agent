# Intent Detection Test Cases 

> **Important:** A test only counts as a full pass if ALL criteria for that test are met — partial matches (correct content but missing the tag, phone number, or slot-collection step) should be logged as "Pass with notes."

---

### Test 1: Booking Intent
**Patient says:**  
> *"Hi, I need to see a dentist for a routine checkup tomorrow morning."*

**Pass criteria:**
- [ ] Correct doctor/availability info (Dr. Imran Khalid, Mon/Wed/Fri, 11 AM–6 PM).
- [ ] Asks for missing details (name, contact, exact time) BEFORE offering a staff handoff.
- [ ] Does not claim the appointment is confirmed.
- [ ] Ends with `[Detected Intent: BOOK]`.

---

### Test 2: FAQ Intent
**Patient says:**  
> *"How much does a dental checkup cost at your clinic?"*

**Pass criteria:**
- [ ] Correct price: PKR 1,500–2,500 (from services.md).
- [ ] Ends with `[Detected Intent: FAQ]`.

---

### Test 3: Cancel Intent
**Patient says:**  
> *"Something came up and I won't be able to make it to my appointment today. Please cancel it."*

**Pass criteria:**
- [ ] Correct cancellation policy (12 hours prior, from policies.md).
- [ ] Asks for name, contact, and appointment date/time or ID BEFORE offering a staff handoff.
- [ ] Does not say the cancellation has been processed.
- [ ] Ends with `[Detected Intent: CANCEL]`.

---

### Test 4: Reschedule Intent
**Patient says:**  
> *"Can we push my 2 PM appointment to 4 PM instead?"*

**Pass criteria:**
- [ ] Correct reschedule policy (no fee, subject to availability, from policies.md).
- [ ] Asks for existing appointment details + confirms new time BEFORE offering a staff handoff.
- [ ] Does not confirm the new time as final.
- [ ] Ends with `[Detected Intent: RESCHEDULE]`.

---

### Test 5: Human Support Intent
**Patient says:**  
> *"Your bot is annoying. Let me talk to a real person right now!"*

**Pass criteria:**
- [ ] Acknowledges the request for a human.
- [ ] States the clinic phone number `+92-321-4455667`.
- [ ] Offers the support-lead callback as an additional option.
- [ ] Ends with `[Detected Intent: HUMAN]`.

---

### Test 6: Human Support — Medical Boundary
**Patient says:**  
> *"My chest hurts, what should I do?"*

**Pass criteria:**
- [ ] Refuses to give medical advice or a diagnosis.
- [ ] Redirects to nearest ER / urgent care (from clinic-faq.md emergency policy).
- [ ] States the clinic phone number `+92-321-4455667`.
- [ ] Ends with `[Detected Intent: HUMAN]`.

---

### Test 7: Ambiguous Message (bonus)
**Patient says:**  
> *"I need help with my appointment."*

**Pass criteria:**
- [ ] Asks a specific clarifying question naming the options (cancel/reschedule/ask something) — not a generic "connect you with staff" offer.
- [ ] Ends with `[Detected Intent: HUMAN]` or no tag if truly unclassified (note which occurs).