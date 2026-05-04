# simplifying-work

Things I have created to simplify my work.

---

## Email Forwarder (`code.js`)

### What it does

This Google Apps Script monitors your Gmail inbox for unread emails from a specific sender with a specific subject, and automatically forwards them to a designated recipient. After forwarding, it marks the original email as read and stars it.

**Flow:**
1. Searches Gmail for unread emails matching a specific sender + subject
2. Forwards the full HTML body of each matching email to a target address
3. Marks the original as read and stars it (so you know it was processed)

This is useful when emails arrive in one inbox (e.g. a shared/service account) and need to be routed to the person or team who actually handles them.

---

### Configuration

At the top of `code.js`, update these three variables:

```js
var SENDER_EMAIL = "SOME_EMAIL_ADDRESS"  // The email address to filter by sender
var EMAIL_SUBJECT = "SOME EMAIL SUBJECT" // The exact subject line to match
var SEND_TO_ADDRESS = "SOME_EMAIL_ADDRESS"  // Where to forward the emails
```

---

### Google Apps Script Setup

1. Go to [script.google.com](https://script.google.com) and create a new project.
2. Paste the contents of `code.js` into the editor.
3. Update the three configuration variables at the top.
4. **Set up a time-driven trigger** to run `forwardMatchingEmails` automatically:
   - Click **Triggers** (clock icon) in the left sidebar → **Add Trigger**
   - Function: `forwardMatchingEmails`
   - Event source: **Time-driven**
   - Type: e.g. *Minutes timer* → every 5 or 10 minutes (adjust to your needs)
   - Click **Save**
5. On first save/run, Google will ask you to authorize the script — grant it access to **Gmail** (read, send, modify).

> The script requires the `GmailApp` service, which is available by default in Apps Script — no additional libraries needed.
