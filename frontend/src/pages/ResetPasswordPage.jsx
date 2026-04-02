import { FormPage } from "../components/FormPage";

export function ResetPasswordPage() {
  return (
    <div className="stack-large">
      <FormPage
        title="Send reset verification code"
        description="Requests a one-time code through the email adapter."
        endpoint="/api/password/send-code"
        fields={[
          { name: "username", label: "Username", placeholder: "alex.lee" },
          { name: "email", label: "Email", type: "email", placeholder: "alex@example.com" }
        ]}
      />

      <FormPage
        title="Reset password with code"
        description="Completes the reset flow and returns a temporary password in demo mode."
        endpoint="/api/password/reset-with-code"
        fields={[
          { name: "username", label: "Username", placeholder: "alex.lee" },
          { name: "email", label: "Email", type: "email", placeholder: "alex@example.com" },
          { name: "code", label: "Verification code", placeholder: "123456" }
        ]}
      />
    </div>
  );
}
