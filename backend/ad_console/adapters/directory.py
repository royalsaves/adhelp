from __future__ import annotations

import boto3
import ldap3

from ad_console.config import Settings
from ad_console.domain.models import DirectoryUser


class DemoDirectoryAdapter:
    def create_user(self, user: DirectoryUser, temporary_password: str) -> None:
        print(f"[demo] create_user username={user.username} temp_password={temporary_password}")

    def reset_password(self, username: str, new_password: str) -> None:
        print(f"[demo] reset_password username={username} new_password={new_password}")


class AwsDirectoryAdapter:
    def __init__(self, settings: Settings) -> None:
        self._directory_id = settings.directory_id
        self._client = boto3.client("ds", region_name=settings.aws_region)

    def create_user(self, user: DirectoryUser, temporary_password: str) -> None:
        self._client.create_user(
            DirectoryId=self._directory_id,
            SAMAccountName=user.username,
            Password=temporary_password,
            GivenName=user.full_name.split()[0],
            Surname=user.full_name.split()[-1] if " " in user.full_name else "",
            EmailAddress=user.email,
        )

    def reset_password(self, username: str, new_password: str) -> None:
        self._client.reset_user_password(
            DirectoryId=self._directory_id,
            UserName=username,
            NewPassword=new_password,
        )


class DemoIdentityVerifier:
    def verify_password(self, username: str, password: str) -> bool:
        return bool(username and password and password != "wrong-password")


class LdapIdentityVerifier:
    def __init__(self, settings: Settings) -> None:
        self._host = settings.ldap_host
        self._domain = settings.company_domain

    def verify_password(self, username: str, password: str) -> bool:
        try:
            server = ldap3.Server(self._host, get_info=ldap3.ALL)
            user_dn = f"{username}@{self._domain}"
            conn = ldap3.Connection(server, user=user_dn, password=password, auto_bind=True)
            conn.unbind()
            return True
        except Exception:
            return False
