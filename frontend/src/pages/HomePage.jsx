import { Link } from "react-router-dom";
import { noticeConfig } from "../config/noticeConfig";

const cards = [
  {
    title: "Account onboarding",
    body: "Submit a new account request and track the approval flow.",
    to: "/request"
  },
  {
    title: "Password lifecycle",
    body: "Verify the current password or issue a reset code.",
    to: "/password"
  },
  {
    title: "Access recovery",
    body: "Handle unlock requests and VPN QR-code reissue scenarios.",
    to: "/unlock"
  }
];

export function HomePage() {
  return (
    <div className="stack-large">
      <section className="hero">
        <div>
          <p className="eyebrow">Hexagonal architecture demo</p>
          <h2>Identity operations without vendor lock-in at the core</h2>
          <p>
            This portfolio version keeps the HTTP API stable while moving directory access,
            notifications, email, automation, and AI support behind adapters.
          </p>
        </div>
        <aside className="notice">
          <h3>{noticeConfig.title}</h3>
          <p>{noticeConfig.summary}</p>
          <a href={noticeConfig.link} target="_blank" rel="noreferrer">
            Read deployment notes
          </a>
        </aside>
      </section>

      <section className="grid">
        {cards.map((card) => (
          <Link key={card.to} to={card.to} className="card card-link">
            <p className="eyebrow">Module</p>
            <h3>{card.title}</h3>
            <p>{card.body}</p>
          </Link>
        ))}
      </section>
    </div>
  );
}
