import { useState } from "react";
import { getContacts, sendSMS } from "../services/api";

export default function SMS() {
  const [contacts, setContacts] = useState([]);
  const [contactId, setContactId] = useState("");
  const [message, setMessage] = useState("");
  const [result, setResult] = useState("");

  async function loadContacts() {
    const response = await getContacts();
    setContacts(response.data);
  }

  async function submit(e) {
    e.preventDefault();
    setResult("");

    try {
      const response = await sendSMS(Number(contactId), message);
      setResult(`SMS status: ${response.data.status}`);
    } catch {
      setResult("SMS request failed. Check contact consent.");
    }
  }

  return (
    <div>
      <h2>SMS Notification</h2>

      <button onClick={loadContacts}>Load Contacts</button>

      <form onSubmit={submit}>
        <select
          value={contactId}
          onChange={(e) => setContactId(e.target.value)}
          required
        >
          <option value="">Select contact</option>

          {contacts.filter((c) => c.sms_consent && !c.opted_out).map((c) => (
            <option key={c.id} value={c.id}>
              {c.name} - {c.phone}
            </option>
          ))}
        </select>

        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Enter notification message"
          required
        />

        <button type="submit">Send Test SMS</button>
      </form>

      <p>{result}</p>
    </div>
  );
}