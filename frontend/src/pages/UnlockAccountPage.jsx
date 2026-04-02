import { FormPage } from "../components/FormPage";

export function UnlockAccountPage() {
  return (
    <FormPage
      title="Request account unlock"
      description="Creates an unlock ticket and exercises the automation adapter."
      endpoint="/api/account/unlock-request"
      fields={[
        { name: "username", label: "Username", placeholder: "alex.lee" },
        { name: "email", label: "Email", type: "email", placeholder: "alex@example.com" },
        { name: "reason", label: "Reason", type: "textarea", placeholder: "Repeated MFA failures during VPN login" }
      ]}
    />
  );
}
