import { FormPage } from "../components/FormPage";

export function RequestAccountPage() {
  return (
    <FormPage
      title="Request a new account"
      description="This calls the account request use case and pushes the request into the in-memory queue."
      endpoint="/api/account/request"
      fields={[
        { name: "username", label: "Username", placeholder: "alex.lee" },
        { name: "email", label: "Email", type: "email", placeholder: "alex@example.com" },
        { name: "fullName", label: "Full name", placeholder: "Alex Lee" },
        { name: "department", label: "Department", placeholder: "Platform Engineering" },
        { name: "reason", label: "Reason", type: "textarea", placeholder: "Need access for onboarding" }
      ]}
    />
  );
}
