import { FormPage } from "../components/FormPage";

export function ChangePasswordPage() {
  return (
    <FormPage
      title="Change current password"
      description="In demo mode, any non-empty password except 'wrong-password' is accepted."
      endpoint="/api/password/change"
      fields={[
        { name: "username", label: "Username", placeholder: "alex.lee" },
        { name: "currentPassword", label: "Current password", type: "password" },
        { name: "newPassword", label: "New password", type: "password" }
      ]}
    />
  );
}
