import { useState } from "react";
import { getContacts, startCall } from "../services/api";

export default function Calls() {
  const [contacts, setContacts] = useState([]);
  const [contactId, setContactId] = useState("");
  const [result, setResult] = useState("");

  async function loadContacts() {
    const response = await getContacts();
    setContacts(response.data);
  }

  async function handleCall() {
    setResult("");

    try {
      const response = await startCall(Number(contactId));
      setResult(`Call status: ${response.data.status}`);
    } catch {
      setResult("Call request rejected. Check consent and retry limit.");
    }
  }

  return (
    <div>
      <h2>Voice Calling</h2>

      <button onClick={loadContacts}>Load Contacts</button>

      <select
        value={contactId}
        onChange={(e) => setContactId(e.target.value)}
      >
        <option value="">Select consented contact</option>

        {contacts.filter((c) => c.voice_consent && !c.opted_out).map((c) => (
          <option key={c.id} value={c.id}>
            {c.name} - {c.phone}
          </option>
        ))}
      </select>

      <button disabled={!contactId} onClick={handleCall}>
        Start Test Call
      </button>

      <p>{result}</p>
    </div>
  );
}