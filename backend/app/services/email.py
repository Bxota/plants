import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from app.config import settings

logger = logging.getLogger(__name__)


def _is_smtp_configured() -> bool:
    return bool(settings.smtp_host and settings.smtp_user and settings.smtp_password)


async def send_invitation_email(to_email: str, invite_token: str) -> None:
    if not _is_smtp_configured():
        logger.warning("SMTP non configuré — email d'invitation non envoyé")
        return

    invite_url = f"{settings.app_base_url}/invite/{invite_token}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Vous êtes invité(e) sur Mes Plantes 🌿"
    msg["From"] = settings.smtp_from or settings.smtp_user
    msg["To"] = to_email

    text = f"""Bonjour,

Vous avez été invité(e) à rejoindre Mes Plantes.

Cliquez sur ce lien pour créer votre compte (valable 7 jours) :
{invite_url}

À bientôt !
"""

    html = f"""<!DOCTYPE html>
<html>
<body style="font-family: Georgia, serif; background: #f9f6f0; margin: 0; padding: 40px 20px;">
  <div style="max-width: 480px; margin: 0 auto; background: #fff; border: 1px solid #c8d5b9; padding: 48px;">
    <p style="font-size: 10px; letter-spacing: 0.25em; text-transform: uppercase; color: #7a9e6e; margin: 0 0 16px;">
      Invitation
    </p>
    <h1 style="font-family: 'Georgia', serif; font-size: 36px; font-weight: 400; color: #2d4a1e; line-height: 1; margin: 0 0 32px;">
      Mes<br /><em style="color: #b5872a;">Plantes</em>
    </h1>
    <p style="font-size: 14px; color: #3d3d3d; line-height: 1.7; margin: 0 0 32px;">
      Vous avez été invité(e) à rejoindre <strong>Mes Plantes</strong>.<br />
      Cliquez sur le bouton ci-dessous pour créer votre compte.
    </p>
    <a href="{invite_url}"
       style="display: inline-block; background: #2d4a1e; color: #f9f6f0; text-decoration: none;
              font-size: 11px; letter-spacing: 0.2em; text-transform: uppercase;
              padding: 14px 28px;">
      Créer mon compte →
    </a>
    <p style="font-size: 11px; color: #9ab08a; margin: 32px 0 0;">
      Ce lien est valable 7 jours.
    </p>
  </div>
</body>
</html>"""

    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    await aiosmtplib.send(
        msg,
        hostname=settings.smtp_host,
        port=settings.smtp_port,
        username=settings.smtp_user,
        password=settings.smtp_password,
        start_tls=True,
    )
    logger.info("Email d'invitation envoyé à %s", to_email)
