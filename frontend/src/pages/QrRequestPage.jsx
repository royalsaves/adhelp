import { FormPage } from "../components/FormPage";

export function QrRequestPage() {
  return (
    <FormPage
      title="Request VPN QR-code reissue"
      description="Sends a notification request for device migration or recovery scenarios."
      endpoint="/api/qr/request"
      fields={[
        { name: "username", label: "Username", placeholder: "alex.lee" },
        { name: "email", label: "Email", type: "email", placeholder: "alex@example.com" },
        { name: "reason", label: "Reason", type: "textarea", placeholder: "New phone enrollment required" }
      ]}
    />
  );
}
