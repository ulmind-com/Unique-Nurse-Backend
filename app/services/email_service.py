"""Email service using Resend API with premium HTML templates.

Designed to be scheduled via FastAPI ``BackgroundTasks`` so the request path is
never blocked by API latency. When the Resend API key is not configured the
service logs the message instead of raising, so local development works without
credentials.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from app.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# ──────────────────────────────────────────────────
#  Premium HTML Email Template
# ──────────────────────────────────────────────────

_BOOKING_CONFIRMATION_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <title>Booking Confirmation</title>
  <!--[if mso]>
  <noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript>
  <![endif]-->
</head>
<body style="margin:0;padding:0;background-color:#f0f4f8;font-family:'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;-webkit-font-smoothing:antialiased;">
  <!-- Outer wrapper -->
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f0f4f8;padding:40px 16px;">
    <tr>
      <td align="center">
        <!-- Inner card -->
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background-color:#ffffff;border-radius:24px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,0.08);">
          
          <!-- ════════════ HERO HEADER ════════════ -->
          <tr>
            <td style="background:linear-gradient(135deg, #0f766e 0%, #0d9488 40%, #14b8a6 100%);padding:48px 40px 40px;text-align:center;">
              <!-- Logo / Brand Mark -->
              <table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 auto;">
                <tr>
                  <td style="background:rgba(255,255,255,0.15);border-radius:20px;padding:16px 20px;">
                    <table role="presentation" cellpadding="0" cellspacing="0">
                      <tr>
                        <td style="width:44px;height:44px;background:#ffffff;border-radius:12px;text-align:center;vertical-align:middle;">
                          <span style="font-size:22px;font-weight:800;color:#0f766e;line-height:44px;">U</span>
                        </td>
                        <td style="padding-left:14px;">
                          <span style="color:#ffffff;font-size:20px;font-weight:700;letter-spacing:-0.5px;display:block;line-height:1.2;">Unique</span>
                          <span style="color:rgba(255,255,255,0.85);font-size:11px;font-weight:500;letter-spacing:1.5px;text-transform:uppercase;">Nurse &amp; Aya Services</span>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
              
              <!-- Success Icon -->
              <table role="presentation" cellpadding="0" cellspacing="0" style="margin:32px auto 0;">
                <tr>
                  <td style="width:72px;height:72px;background:rgba(255,255,255,0.2);border-radius:50%;text-align:center;vertical-align:middle;">
                    <span style="font-size:36px;line-height:72px;">&#10003;</span>
                  </td>
                </tr>
              </table>
              
              <h1 style="margin:24px 0 0;color:#ffffff;font-size:28px;font-weight:700;letter-spacing:-0.5px;line-height:1.3;">
                Booking Confirmed!
              </h1>
              <p style="margin:12px 0 0;color:rgba(255,255,255,0.85);font-size:15px;line-height:1.5;max-width:400px;display:inline-block;">
                Thank you for choosing us. Your request has been received and our care team is on it.
              </p>
            </td>
          </tr>
          
          <!-- ════════════ GREETING ════════════ -->
          <tr>
            <td style="padding:40px 40px 0;">
              <p style="margin:0;color:#1e293b;font-size:17px;line-height:1.6;">
                Dear <strong style="color:#0f766e;">{name}</strong>,
              </p>
              <p style="margin:12px 0 0;color:#475569;font-size:15px;line-height:1.7;">
                We're delighted to confirm that your service booking has been successfully submitted. Here's a summary of your request:
              </p>
            </td>
          </tr>
          
          <!-- ════════════ BOOKING DETAILS CARD ════════════ -->
          <tr>
            <td style="padding:28px 40px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:linear-gradient(135deg, #f0fdfa 0%, #f0f9ff 100%);border:1px solid #ccfbf1;border-radius:16px;overflow:hidden;">
                <!-- Reference Badge -->
                <tr>
                  <td style="padding:24px 28px 0;">
                    <table role="presentation" cellpadding="0" cellspacing="0">
                      <tr>
                        <td style="background:#0f766e;border-radius:8px;padding:8px 16px;">
                          <span style="color:#ffffff;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;">Booking Reference</span>
                        </td>
                      </tr>
                    </table>
                    <p style="margin:8px 0 0;color:#0f766e;font-size:24px;font-weight:800;letter-spacing:1px;font-family:'Courier New',monospace;">
                      {reference}
                    </p>
                  </td>
                </tr>
                
                <!-- Divider -->
                <tr>
                  <td style="padding:20px 28px 0;">
                    <div style="height:1px;background:linear-gradient(90deg, transparent, #99f6e4, transparent);"></div>
                  </td>
                </tr>
                
                <!-- Details Grid -->
                <tr>
                  <td style="padding:20px 28px 28px;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                      <!-- Service -->
                      <tr>
                        <td style="padding:10px 0;vertical-align:top;width:40%;">
                          <span style="color:#94a3b8;font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;">Service</span>
                        </td>
                        <td style="padding:10px 0;vertical-align:top;">
                          <span style="color:#1e293b;font-size:15px;font-weight:600;">{service}</span>
                        </td>
                      </tr>
                      <!-- Date -->
                      <tr>
                        <td style="padding:10px 0;vertical-align:top;">
                          <span style="color:#94a3b8;font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;">Preferred Date</span>
                        </td>
                        <td style="padding:10px 0;vertical-align:top;">
                          <span style="color:#1e293b;font-size:15px;font-weight:600;">{date}</span>
                        </td>
                      </tr>
                      <!-- Patient -->
                      <tr>
                        <td style="padding:10px 0;vertical-align:top;">
                          <span style="color:#94a3b8;font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;">Patient Name</span>
                        </td>
                        <td style="padding:10px 0;vertical-align:top;">
                          <span style="color:#1e293b;font-size:15px;font-weight:600;">{name}</span>
                        </td>
                      </tr>
                      <!-- City -->
                      {city_row}
                    </table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          
          <!-- ════════════ WHAT'S NEXT STEPS ════════════ -->
          <tr>
            <td style="padding:0 40px 32px;">
              <h2 style="margin:0 0 20px;color:#1e293b;font-size:18px;font-weight:700;">What Happens Next?</h2>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                <!-- Step 1 -->
                <tr>
                  <td style="padding:0 0 16px;">
                    <table role="presentation" cellpadding="0" cellspacing="0">
                      <tr>
                        <td style="width:44px;vertical-align:top;">
                          <div style="width:36px;height:36px;background:linear-gradient(135deg,#0f766e,#14b8a6);border-radius:10px;text-align:center;line-height:36px;color:#ffffff;font-size:14px;font-weight:700;">1</div>
                        </td>
                        <td style="padding-left:14px;vertical-align:top;">
                          <p style="margin:0;color:#1e293b;font-size:14px;font-weight:600;">Confirmation Call</p>
                          <p style="margin:4px 0 0;color:#64748b;font-size:13px;line-height:1.5;">Our care advisor will call you within 2 hours to confirm details and timing.</p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
                <!-- Step 2 -->
                <tr>
                  <td style="padding:0 0 16px;">
                    <table role="presentation" cellpadding="0" cellspacing="0">
                      <tr>
                        <td style="width:44px;vertical-align:top;">
                          <div style="width:36px;height:36px;background:linear-gradient(135deg,#0f766e,#14b8a6);border-radius:10px;text-align:center;line-height:36px;color:#ffffff;font-size:14px;font-weight:700;">2</div>
                        </td>
                        <td style="padding-left:14px;vertical-align:top;">
                          <p style="margin:0;color:#1e293b;font-size:14px;font-weight:600;">Staff Assignment</p>
                          <p style="margin:4px 0 0;color:#64748b;font-size:13px;line-height:1.5;">We'll match you with a verified, trained professional best suited for your needs.</p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
                <!-- Step 3 -->
                <tr>
                  <td style="padding:0;">
                    <table role="presentation" cellpadding="0" cellspacing="0">
                      <tr>
                        <td style="width:44px;vertical-align:top;">
                          <div style="width:36px;height:36px;background:linear-gradient(135deg,#0f766e,#14b8a6);border-radius:10px;text-align:center;line-height:36px;color:#ffffff;font-size:14px;font-weight:700;">3</div>
                        </td>
                        <td style="padding-left:14px;vertical-align:top;">
                          <p style="margin:0;color:#1e293b;font-size:14px;font-weight:600;">Service Begins</p>
                          <p style="margin:4px 0 0;color:#64748b;font-size:13px;line-height:1.5;">Your caregiver arrives at the scheduled time, ready to provide compassionate care.</p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          
          <!-- ════════════ TRUST BADGES ════════════ -->
          <tr>
            <td style="padding:0 40px 32px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f8fafc;border-radius:12px;overflow:hidden;">
                <tr>
                  <td style="padding:20px;text-align:center;width:33.33%;border-right:1px solid #e2e8f0;">
                    <div style="font-size:24px;margin-bottom:6px;">&#128170;</div>
                    <p style="margin:0;color:#1e293b;font-size:12px;font-weight:700;">Verified Staff</p>
                    <p style="margin:2px 0 0;color:#94a3b8;font-size:11px;">Background checked</p>
                  </td>
                  <td style="padding:20px;text-align:center;width:33.33%;border-right:1px solid #e2e8f0;">
                    <div style="font-size:24px;margin-bottom:6px;">&#9201;</div>
                    <p style="margin:0;color:#1e293b;font-size:12px;font-weight:700;">24/7 Support</p>
                    <p style="margin:2px 0 0;color:#94a3b8;font-size:11px;">Always available</p>
                  </td>
                  <td style="padding:20px;text-align:center;width:33.34%;">
                    <div style="font-size:24px;margin-bottom:6px;">&#128176;</div>
                    <p style="margin:0;color:#1e293b;font-size:12px;font-weight:700;">Fair Pricing</p>
                    <p style="margin:2px 0 0;color:#94a3b8;font-size:11px;">No hidden charges</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          
          <!-- ════════════ CTA BUTTON ════════════ -->
          <tr>
            <td style="padding:0 40px 32px;text-align:center;">
              <p style="margin:0 0 16px;color:#475569;font-size:14px;">Need immediate assistance? Contact us anytime:</p>
              <table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 auto;">
                <tr>
                  <td style="padding-right:12px;">
                    <a href="tel:+919432941098" style="display:inline-block;background:#0f766e;color:#ffffff;text-decoration:none;padding:14px 28px;border-radius:12px;font-size:14px;font-weight:600;letter-spacing:0.3px;">
                      &#128222; Call Us
                    </a>
                  </td>
                  <td>
                    <a href="https://wa.me/919432941098" style="display:inline-block;background:#25D366;color:#ffffff;text-decoration:none;padding:14px 28px;border-radius:12px;font-size:14px;font-weight:600;letter-spacing:0.3px;">
                      &#128172; WhatsApp
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          
          <!-- ════════════ DIVIDER ════════════ -->
          <tr>
            <td style="padding:0 40px;">
              <div style="height:1px;background:linear-gradient(90deg, transparent, #e2e8f0, transparent);"></div>
            </td>
          </tr>
          
          <!-- ════════════ FOOTER ════════════ -->
          <tr>
            <td style="padding:32px 40px;text-align:center;">
              <p style="margin:0;color:#94a3b8;font-size:12px;line-height:1.6;">
                <strong style="color:#64748b;">Unique Nurse and Aya Services</strong><br/>
                3, Anukul Chandra Road, Tetulberia, Garia<br/>
                Kolkata - 700084, West Bengal
              </p>
              <p style="margin:16px 0 0;color:#cbd5e1;font-size:11px;">
                This is an automated confirmation email. Please do not reply directly.<br/>
                &copy; {year} Unique Nurse and Aya Services. All rights reserved.
              </p>
            </td>
          </tr>
          
        </table>
        <!-- /Inner card -->
      </td>
    </tr>
  </table>
  <!-- /Outer wrapper -->
</body>
</html>
"""

_GENERIC_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{subject}</title>
</head>
<body style="margin:0;padding:0;background-color:#f0f4f8;font-family:'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f0f4f8;padding:40px 16px;">
    <tr>
      <td align="center">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background-color:#ffffff;border-radius:24px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,0.08);">
          <!-- Header -->
          <tr>
            <td style="background:linear-gradient(135deg, #0f766e 0%, #0d9488 40%, #14b8a6 100%);padding:36px 40px;text-align:center;">
              <table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 auto;">
                <tr>
                  <td style="width:40px;height:40px;background:#ffffff;border-radius:10px;text-align:center;vertical-align:middle;">
                    <span style="font-size:20px;font-weight:800;color:#0f766e;line-height:40px;">U</span>
                  </td>
                  <td style="padding-left:12px;">
                    <span style="color:#ffffff;font-size:18px;font-weight:700;letter-spacing:-0.3px;">Unique</span>
                    <span style="color:rgba(255,255,255,0.8);font-size:18px;font-weight:400;"> Nurse &amp; Aya</span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <!-- Body -->
          <tr>
            <td style="padding:40px;color:#1e293b;font-size:15px;line-height:1.7;">
              {body}
            </td>
          </tr>
          <!-- Footer -->
          <tr>
            <td style="padding:0 40px;">
              <div style="height:1px;background:linear-gradient(90deg, transparent, #e2e8f0, transparent);"></div>
            </td>
          </tr>
          <tr>
            <td style="padding:28px 40px;text-align:center;">
              <p style="margin:0;color:#94a3b8;font-size:12px;line-height:1.6;">
                <strong style="color:#64748b;">Unique Nurse and Aya Services</strong><br/>
                3, Anukul Chandra Road, Tetulberia, Garia, Kolkata - 700084
              </p>
              <p style="margin:12px 0 0;color:#cbd5e1;font-size:11px;">
                This is an automated message. Please do not reply.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""


class EmailService:
    """Send transactional emails via the Resend API."""

    RESEND_API_URL = "https://api.resend.com/emails"

    def __init__(self) -> None:
        self.enabled = settings.email_enabled

    async def send(
        self,
        to: str,
        subject: str,
        body_html: str,
        text_fallback: Optional[str] = None,
    ) -> bool:
        """Send a single HTML email via Resend. Returns ``True`` on success."""
        if not self.enabled:
            logger.info(
                "Email disabled; skipping send",
                extra={"to": to, "subject": subject},
            )
            return False

        payload = {
            "from": settings.EMAIL_FROM,
            "to": [to],
            "subject": subject,
            "html": body_html,
        }
        if text_fallback:
            payload["text"] = text_fallback

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.RESEND_API_URL,
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                        "Content-Type": "application/json",
                    },
                )

            if response.status_code in (200, 201):
                logger.info("Email sent via Resend", extra={"to": to, "subject": subject})
                return True
            else:
                logger.error(
                    "Resend API error",
                    extra={
                        "to": to,
                        "subject": subject,
                        "status": response.status_code,
                        "body": response.text,
                    },
                )
                return False
        except Exception as exc:  # noqa: BLE001 - never break the request path
            logger.error(
                "Email send failed",
                extra={"to": to, "subject": subject, "error": str(exc)},
            )
            return False

    # ---- Convenience templated senders ----

    async def send_booking_confirmation(self, to: str, context: Dict[str, Any]) -> bool:
        from datetime import datetime

        name = context.get("name", "Customer")
        service = context.get("service", "")
        reference = context.get("reference", "")
        date = context.get("date", "")
        city = context.get("city", "")
        year = str(datetime.now().year)

        # Build optional city row
        city_row = ""
        if city:
            city_row = (
                '<tr>'
                '<td style="padding:10px 0;vertical-align:top;">'
                '<span style="color:#94a3b8;font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;">City</span>'
                '</td>'
                '<td style="padding:10px 0;vertical-align:top;">'
                f'<span style="color:#1e293b;font-size:15px;font-weight:600;">{city}</span>'
                '</td>'
                '</tr>'
            )

        html = _BOOKING_CONFIRMATION_TEMPLATE.format(
            name=name,
            service=service,
            reference=reference,
            date=date,
            city_row=city_row,
            year=year,
        )

        text_fallback = (
            f"Dear {name},\n\n"
            f"Your booking for {service} has been confirmed!\n"
            f"Reference: {reference}\n"
            f"Preferred Date: {date}\n\n"
            "Our team will contact you within 2 hours to confirm the details.\n\n"
            "Thank you,\nUnique Nurse and Aya Services\n"
            "+91 94329 41098"
        )

        return await self.send(
            to,
            f"✅ Booking Confirmed — {reference}",
            html,
            text_fallback,
        )

    async def send_contact_confirmation(self, to: str, context: Dict[str, Any]) -> bool:
        body = (
            f"<p>Dear {context.get('name', 'there')},</p>"
            "<p>We have received your message and will get back to you soon.</p>"
            f"<blockquote style='border-left:3px solid #0f766e;padding-left:16px;color:#475569;margin:16px 0;'>"
            f"{context.get('message', '')}</blockquote>"
        )
        html = _GENERIC_TEMPLATE.format(subject="Message Received", body=body)
        return await self.send(to, "We Received Your Message", html)

    async def send_application_confirmation(self, to: str, context: Dict[str, Any]) -> bool:
        body = (
            f"<p>Dear {context.get('name', 'Applicant')},</p>"
            f"<p>Thank you for applying for <strong>{context.get('job')}</strong>.</p>"
            f"<p>Your application reference is <strong style='color:#0f766e;'>{context.get('reference')}</strong>.</p>"
            "<p>Our HR team will review your application and reach out if shortlisted.</p>"
        )
        html = _GENERIC_TEMPLATE.format(subject="Application Received", body=body)
        return await self.send(to, "Application Received", html)

    async def send_password_reset(self, to: str, reset_link: str) -> bool:
        body = (
            "<p>We received a request to reset your password.</p>"
            f'<p style="text-align:center;margin:28px 0;">'
            f'<a href="{reset_link}" '
            'style="display:inline-block;background:linear-gradient(135deg,#0f766e,#14b8a6);'
            "color:#ffffff;padding:14px 32px;border-radius:12px;text-decoration:none;"
            'font-size:15px;font-weight:600;">Reset Password</a></p>'
            f"<p style='color:#94a3b8;font-size:13px;'>Or copy this link: {reset_link}</p>"
            "<p>If you did not request this, you can safely ignore this email.</p>"
        )
        html = _GENERIC_TEMPLATE.format(subject="Password Reset", body=body)
        return await self.send(to, "Password Reset Request", html)

    async def send_admin_notification(self, subject: str, body_html: str) -> bool:
        if not settings.ADMIN_NOTIFICATION_EMAIL:
            return False
        html = _GENERIC_TEMPLATE.format(subject=subject, body=body_html)
        return await self.send(settings.ADMIN_NOTIFICATION_EMAIL, subject, html)


# Module-level singleton.
email_service = EmailService()
