var SENDER_EMAIL = "SOME_EMAIL_ADDRESS"
var EMAIL_SUBJECT = "SOME EMAIL SUBJECT"
var SEND_TO_ADDRESS = "SOME_EMAIL_ADDRESS"

function forwardMatchingEmails() {

  var THREADS = GmailApp.search(
    'from:' + SENDER_EMAIL + ' subject:"' + EMAIL_SUBJECT + '" is:unread'
  );                                                                          // Get all unread emails from SENDER_EMAIL with EMAIL_SUBJECT as subject

  for (let i = 0; i < THREADS.length; i++) {
    var currentThread = THREADS[i];
    var messages = currentThread.getMessages();
    var message = messages[0];
    var emailContent = message.getBody();

    GmailApp.sendEmail(
      SEND_TO_ADDRESS,
      EMAIL_SUBJECT,
      "",
      { htmlBody: emailContent }                                                // Use HTML content
    );                                                                          // Send email with the received body

    message.markRead();
    message.star()
  }
}
