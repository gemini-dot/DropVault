"""
Sentry Integration Configuration
This module initializes Sentry for error tracking and performance monitoring in the DropVault application. It config
ures Sentry with the DSN, environment, release version, and sampling rates for traces and profiles. It also ensures that personally identifiable information (PII) is not sent to Sentry by default.
@copyright: 2026 DropVault Team
@created: 2026-04-16 12:00 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from os import getenv


def init_sentry():
    dsn = str(getenv("SENTRY_KEY"))
    if not dsn:
        return

    sentry_sdk.init(
        dsn=dsn,
        integrations=[FlaskIntegration()],
        environment=getenv("ENV", "development"),
        release=getenv("RELEASE", "dropvault@dev"),
        traces_sample_rate=0.1,
        profiles_sample_rate=0.05,
        send_default_pii=False,
    )
