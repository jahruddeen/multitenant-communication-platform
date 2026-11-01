
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  Outlet,
} from "react-router-dom";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Companies from "./pages/Companies";
import Contacts from "./pages/Contacts";
import SMS from "./pages/SMS";
import Calls from "./pages/Calls";
import Reports from "./pages/Reports";

function ProtectedLayout() {
  const token = sessionStorage.getItem("access_token");

  if (!token) return <Navigate to="/login" replace />;

  return (
    <div className="app-layout">
      <Sidebar />

      <main className="main-content">
        <Header title="Notification Management" />
        <Outlet />
      </main>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route element={<ProtectedLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/companies" element={<Companies />} />
          <Route path="/contacts" element={<Contacts />} />
          <Route path="/sms" element={<SMS />} />
          <Route path="/calls" element={<Calls />} />
          <Route path="/reports" element={<Reports />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
