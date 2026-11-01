import { useEffect, useState } from "react";
import { getReports } from "../services/api";

export default function Reports() {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    getReports()
      .then((response) => setReports(response.data))
      .catch(() => setReports([]));
  }, []);

  return (
    <div>
      <h2>Communication Reports</h2>

      <table>
        <thead>
          <tr>
            <th>Contact ID</th>
            <th>Channel</th>
            <th>Status</th>
            <th>Attempt</th>
            <th>Date</th>
          </tr>
        </thead>

        <tbody>
          {reports.map((item) => (
            <tr key={item.id}>
              <td>{item.contact_id}</td>
              <td>{item.channel}</td>
              <td>{item.status}</td>
              <td>{item.attempt}</td>
              <td>{new Date(item.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}