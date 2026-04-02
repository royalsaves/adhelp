import { NavLink, Route, Routes } from "react-router-dom";
import { appConfig } from "./config/appConfig";
import { ChatWidget } from "./components/ChatWidget";
import { HomePage } from "./pages/HomePage";
import { RequestAccountPage } from "./pages/RequestAccountPage";
import { ChangePasswordPage } from "./pages/ChangePasswordPage";
import { ResetPasswordPage } from "./pages/ResetPasswordPage";
import { UnlockAccountPage } from "./pages/UnlockAccountPage";
import { QrRequestPage } from "./pages/QrRequestPage";

const navItems = [
  ["/", "Overview"],
  ["/request", "Request"],
  ["/password", "Change Password"],
  ["/reset", "Reset Password"],
  ["/unlock", "Unlock"],
  ["/qr-request", "QR Reissue"]
];

export default function App() {
  return (
    <div className="shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">{appConfig.company.tagline}</p>
          <h1>{appConfig.service.name}</h1>
        </div>
        <nav className="nav">
          {navItems.map(([to, label]) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}
            >
              {label}
            </NavLink>
          ))}
        </nav>
      </header>

      <main className="page">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/request" element={<RequestAccountPage />} />
          <Route path="/password" element={<ChangePasswordPage />} />
          <Route path="/reset" element={<ResetPasswordPage />} />
          <Route path="/unlock" element={<UnlockAccountPage />} />
          <Route path="/qr-request" element={<QrRequestPage />} />
        </Routes>
      </main>

      <ChatWidget />
    </div>
  );
}
