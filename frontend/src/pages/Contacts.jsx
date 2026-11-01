
import { useEffect, useState } from "react";

import {
  getContacts,
  createContact,
} from "../services/api";

export default function Contacts() {
  const [contacts, setContacts] = useState([]);
  const [phone, setPhone] = useState("");
  const [name, setName] = useState("");
  const [smsConsent, setSmsConsent] = useState(false);
  const [voiceConsent, setVoiceConsent] = useState(false);
  const [error, setError] = useState("");

  async function loadContacts() {
    const response = await getContacts();
    setContacts(response.data);
  }

  useEffect(() => {
    loadContacts().catch(() => {
      setError("Unable to load contacts.");
    });
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    try {
      await createContact({
        phone,
        name,
        sms_consent: smsConsent,
        voice_consent: voiceConsent,
      });

      setPhone("");
      setName("");
      setSmsConsent(false);
      setVoiceConsent(false);

      await loadContacts();
    } catch {
      setError("Contact creation failed.");
    }
  }

  return (
    <div>
      <h2>Contact Management</h2>

      <form className="contact-form" onSubmit={handleSubmit}>
        <input
          placeholder="Contact Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <input
          placeholder="+919876543210"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          required
        />

        <label>
          <input
            type="checkbox"
            checked={smsConsent}
            onChange={(e) => setSmsConsent(e.target.checked)}
          />
          SMS consent documented
        </label>

        <label>
          <input
            type="checkbox"
            checked={voiceConsent}
            onChange={(e) => setVoiceConsent(e.target.checked)}
          />
          Voice consent documented
        </label>

        <button type="submit">Add Contact</button>
      </form>

      {error && <p className="error">{error}</p>}

      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Phone</th>
            <th>SMS Permission</th>
            <th>Voice Permission</th>
          </tr>
        </thead>

        <tbody>
          {contacts.map((contact) => (
            <tr key={contact.id}>
              <td>{contact.name}</td>
              <td>{contact.phone}</td>
              <td>{contact.sms_consent ? "Yes" : "No"}</td>
              <td>{contact.voice_consent ? "Yes" : "No"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
