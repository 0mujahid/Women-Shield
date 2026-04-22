from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Iterable

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()
OUTPUT_PDF = ROOT / "Section_ID_Mohammad_Mujahid.pdf"


def first_match(*patterns: str) -> Path | None:
    roots = [
        ROOT,
        ROOT / "assets" / "images",
        HOME / "Desktop",
        HOME / "Downloads",
    ]
    for base in roots:
        for pattern in patterns:
            matches = sorted(base.glob(pattern))
            if matches:
                return matches[0]
    return None


def extract_lines(path: Path, start: int, end: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    excerpt = lines[start - 1 : end]
    return "\n".join(excerpt)


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=16,
        )
    )
    styles.add(
        ParagraphStyle(
            "SectionTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=22,
            textColor=colors.HexColor("#7c2d12"),
            spaceBefore=10,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            "SubTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=6,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            "Caption",
            parent=styles["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#475569"),
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            "CoverMeta",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=12,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#334155"),
        )
    )
    styles.add(
        ParagraphStyle(
            "CodeLabel",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#1d4ed8"),
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            "Tiny",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#475569"),
        )
    )
    return styles


def bullet_list(items: Iterable[str], styles) -> ListFlowable:
    return ListFlowable(
        [
            ListItem(Paragraph(item, styles["Body"]), leftIndent=8)
            for item in items
        ],
        bulletType="bullet",
        leftIndent=18,
        bulletFontName="Helvetica",
        bulletFontSize=8,
    )


def figure(path: Path | None, caption: str, max_width_cm: float, styles):
    if path is None or not path.exists():
        return KeepTogether(
            [
                Paragraph("Image unavailable", styles["Tiny"]),
                Paragraph(caption, styles["Caption"]),
            ]
        )

    with PILImage.open(path) as image:
        width, height = image.size

    draw_width = max_width_cm * cm
    draw_height = draw_width * height / width
    flowable = Image(str(path), width=draw_width, height=draw_height)

    return KeepTogether(
        [
            flowable,
            Spacer(1, 0.15 * cm),
            Paragraph(caption, styles["Caption"]),
        ]
    )


def code_block(label: str, path: Path, start: int, end: int, styles):
    snippet = extract_lines(path, start, end)
    code_style = ParagraphStyle(
        "Code",
        fontName="Courier",
        fontSize=6.7,
        leading=8,
        leftIndent=6,
        rightIndent=6,
        borderPadding=6,
        backColor=colors.HexColor("#f8fafc"),
        borderWidth=0.5,
        borderColor=colors.HexColor("#cbd5e1"),
        spaceAfter=10,
    )
    return KeepTogether(
        [
            Paragraph(label, styles["CodeLabel"]),
            Preformatted(snippet, code_style),
        ]
    )


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawRightString(A4[0] - 1.8 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


def build_report():
    styles = make_styles()
    story = []

    logo = first_match("women-shield-logo.png", "WS.png", "womenshield.png")
    hero = first_match("Screenshot 2026-04-21 at 8.23.14*PM.png", "Screenshot 2026-04-18 at 12.19.52*AM.png")
    login_screen = first_match("Screenshot 2026-04-21 at 8.37.41*PM.png")
    register_screen = first_match("Screenshot 2026-04-19 at 10.13.14*PM.png")
    dashboard_screen = first_match("Screenshot 2026-04-17 at 11.11.28*PM.png")
    report_screen = first_match("Screenshot 2026-04-18 at 12.35.07*AM.png", "Screenshot 2026-04-18 at 12.43.22*AM.png")
    emergency_screen = first_match("Screenshot 2026-04-19 at 9.58.41*PM.png", "Screenshot 2026-04-19 at 8.54.10*PM.png")
    map_screen = first_match("Screenshot 2026-04-21 at 10.26.11*PM.png")
    email_screen = first_match("WhatsApp Image 2026-04-21 at 21.16.17.jpeg", "WhatsApp Image 2026-04-21 at 20.58.30.jpeg")
    admin_screen = first_match("Screenshot 2026-04-21 at 8.50.09*PM.png")

    story.append(Spacer(1, 1.3 * cm))
    if logo and logo.exists():
        story.append(figure(logo, "Women Shield project identity", 4.2, styles))
        story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Women Shield", styles["ReportTitle"]))
    story.append(Paragraph("Project Report", styles["ReportTitle"]))
    story.append(
        Paragraph(
            "Prepared following the provided lab report instruction PDF",
            styles["CoverMeta"],
        )
    )
    story.append(Spacer(1, 0.6 * cm))
    story.append(Paragraph("Student: Mohammad Mujahid", styles["CoverMeta"]))
    story.append(Paragraph("Section: Section_ID", styles["CoverMeta"]))
    story.append(Paragraph(f"Date: {date.today().strftime('%B %d, %Y')}", styles["CoverMeta"]))
    story.append(Spacer(1, 0.8 * cm))
    story.append(
        Paragraph(
            "This report describes the complete Women Shield web application, its major modules, user workflow, screenshots, and selected code excerpts from the implementation.",
            styles["Body"],
        )
    )
    story.append(Spacer(1, 0.5 * cm))
    story.append(figure(hero, "Figure 1. Landing page and project theme", 16.5, styles))
    story.append(PageBreak())

    story.append(Paragraph("Abstract", styles["SectionTitle"]))
    story.append(
        Paragraph(
            "Women Shield is a PHP and MySQL based safety support platform built for a local XAMPP environment. "
            "The system combines user authentication, emergency contact management, incident reporting, a danger-aware map, "
            "AI-based incident analysis, emergency email alerts, and an admin configuration area in one deployable application. "
            "The goal of the project is to provide a simple but practical digital safety workflow where a user can document incidents, "
            "receive guidance, contact trusted people, and react quickly during emergencies. The application uses heuristic AI logic instead "
            "of external APIs so the full system can run locally without internet-based model dependencies.",
            styles["Body"],
        )
    )

    story.append(Paragraph("Introduction", styles["SectionTitle"]))
    story.append(
        Paragraph(
            "The project was designed around a common safety problem: people often need one place to store trusted contacts, report risky events, "
            "see danger patterns, and send alerts quickly. Women Shield addresses that gap by integrating multiple safety tools into one website. "
            "Instead of keeping contacts in one app, reports in another place, and emergency actions in a third system, the user can complete the whole response workflow inside one local platform.",
            styles["Body"],
        )
    )

    story.append(Paragraph("System Overview", styles["SectionTitle"]))
    story.append(
        Paragraph(
            "Women Shield follows a classic three-layer web structure. The presentation layer is built with PHP templates, HTML, CSS, and JavaScript. "
            "The logic layer is handled by PHP service functions that validate forms, communicate with the database, run the heuristic AI pipeline, and prepare emergency messages. "
            "The data layer uses MySQL tables for users, admins, contacts, reports, alerts, chat history, and emergency sessions. "
            "Leaflet with OpenStreetMap is used for map visualization, while SMTP or PHPMailer can be used for email delivery.",
            styles["Body"],
        )
    )

    tech_table = Table(
        [
            ["Layer", "Technology Used"],
            ["Frontend", "PHP templates, HTML, CSS, JavaScript"],
            ["Backend", "PHP 8+, modular service functions"],
            ["Database", "MySQL / MariaDB on XAMPP"],
            ["Mapping", "Leaflet + OpenStreetMap tiles"],
            ["Email", "Built-in SMTP support with optional PHPMailer"],
            ["AI Logic", "Local heuristic rules in lib/ai.php"],
        ],
        colWidths=[4.1 * cm, 11.8 * cm],
    )
    tech_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f97316")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#fff7ed")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(tech_table)
    story.append(Spacer(1, 0.35 * cm))

    story.append(Paragraph("Feature Descriptions", styles["SectionTitle"]))
    feature_rows = [
        ["Landing page and role-based login", "The top navigation separates user login and admin login so the correct dashboard opens based on account type."],
        ["Registration and profile setup", "New users can create an account with name, email, phone number, and password."],
        ["Emergency contact CRUD", "Users can create, read, update, and delete trusted contacts, including phone, relation, email, and priority order."],
        ["Incident report CRUD", "Users can create, review, edit, and delete incident reports with location, status, severity, and time."],
        ["AI categorization", "Each report is analyzed locally to classify incident type from the report text."],
        ["Danger score and night risk", "The application computes a danger score using severity, keywords, time of incident, and environmental risk hints."],
        ["Fake report agent", "Suspicious submissions are flagged when the narrative is too short or inconsistent."],
        ["Dashboard and alerts", "The dashboard summarizes user reports, alert history, emergency status, and AI insights in one place."],
        ["Safety map", "Saved report coordinates are displayed on a Leaflet map and the user can compare nearby hotspots with current browser location."],
        ["Emergency mode", "A user can activate emergency mode, record location, notify trusted contacts, and keep a share-ready help message."],
        ["AI assistant", "The system stores conversation history and provides local safety guidance in plain language."],
        ["Admin email setup", "The admin dashboard focuses on SMTP configuration and hides private user activity."],
    ]
    feature_table = Table(feature_rows, colWidths=[5.3 * cm, 10.6 * cm], repeatRows=0)
    feature_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(feature_table)
    story.append(PageBreak())

    story.append(Paragraph("Detailed Features", styles["SectionTitle"]))
    detailed_features = [
        (
            "1. Authentication and account separation",
            "The application supports both standard user login and separate admin login. A user account is redirected to the personal dashboard, while the admin account is redirected to the privacy-first admin area. The login system also blocks admin pages for regular users and blocks user-only pages for admin accounts.",
        ),
        (
            "2. Emergency contact management",
            "The contacts module implements complete CRUD functionality. Users can add trusted people, set a priority number, attach phone and email information, update existing entries, and remove contacts they no longer need. The module validates Bangladesh phone numbers before saving.",
        ),
        (
            "3. Incident report management",
            "The reports module is one of the core features of Women Shield. A user can create a report with a title, description, status, severity, incident time, location summary, and coordinates. After submission, the system stores the report and calculates multiple AI-assisted outputs such as category, confidence, danger score, fake-review signal, night risk, and safety tips. The same form supports editing, while the report table supports viewing and deletion.",
        ),
        (
            "4. Personal dashboard and agent insights",
            "The dashboard shows the total number of reports, high-risk incidents, saved contacts, average danger score, active emergency state, the latest report summary, alert history, and system recommendations. This lets the user review safety activity at a glance.",
        ),
        (
            "5. Safety map",
            "The map module reads report coordinates from the database and plots them as colored markers based on danger score. It also reads the browser geolocation API, stores the current position in local storage, and shows the user marker with an accuracy circle. This helps compare the user's position against known risk hotspots.",
        ),
        (
            "6. Emergency mode and email alerts",
            "Emergency mode creates an active emergency session, records a location summary, prepares a copyable outreach message, surfaces high-priority contacts, and sends email alerts to contacts who have an email address saved. When coordinate data is available, the system includes a direct Google Maps link in the email body.",
        ),
        (
            "7. AI assistant",
            "The assistant page keeps a local conversation history and responds to user questions about reporting, emergency actions, or safer behavior. Even without an external AI provider, the application demonstrates the workflow of an assistant module inside the project.",
        ),
        (
            "8. Admin dashboard and email setup",
            "The admin dashboard is intentionally privacy-focused. It hides user activity, reports, and personal details, and instead provides email transport status, SMTP configuration, and test email functionality. This is important because the admin role is limited to configuration rather than seeing private user data.",
        ),
    ]
    for title, body in detailed_features:
        story.append(Paragraph(title, styles["SubTitle"]))
        story.append(Paragraph(body, styles["Body"]))

    story.append(Paragraph("Technology", styles["SectionTitle"]))
    story.append(
        bullet_list(
            [
                "PHP 8+ powers the page rendering, validation, authentication, and service layer.",
                "MySQL / MariaDB stores the application data inside seven main tables: users, admin, emergency_contacts, reports, alerts, chat_logs, and emergency_sessions.",
                "Plain JavaScript is used for dynamic behavior such as form submission, geolocation capture, local storage, and assistant chat requests.",
                "Leaflet and OpenStreetMap are used to render risk markers and current location on the map page.",
                "SMTP configuration is saved by the admin so emergency emails can be sent to trusted contacts.",
            ],
            styles,
        )
    )

    story.append(Paragraph("Implementation Details", styles["SectionTitle"]))
    story.append(
        Paragraph(
            "The project is organized into page-level modules such as login.php, dashboard.php, contacts.php, reports.php, safety_map.php, emergency.php, assistant.php, and admin/index.php. "
            "Shared business logic is placed in lib/auth.php, lib/services.php, lib/ai.php, and lib/mailer.php. "
            "This separation keeps the code readable: page files handle presentation and user input, while service functions perform validation, database interaction, and workflow decisions.",
            styles["Body"],
        )
    )
    impl_table = Table(
        [
            ["Important file", "Responsibility"],
            ["lib/auth.php", "Authentication, role checks, session handling, registration"],
            ["lib/services.php", "Contacts, reports, alerts, emergency sessions, email workflow"],
            ["lib/ai.php", "Heuristic category, fake score, danger score, night risk, safety tips"],
            ["contacts.php", "Emergency contact create, read, update, delete UI"],
            ["reports.php", "Incident report create, read, update, delete UI and AI output"],
            ["safety_map.php", "Map marker rendering and browser geolocation"],
            ["emergency.php", "Emergency activation flow and current-location sharing"],
            ["mail_setup.php", "Admin SMTP configuration and test email"],
        ],
        colWidths=[4.7 * cm, 11.2 * cm],
    )
    impl_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1d4ed8")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#eff6ff")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(impl_table)
    story.append(PageBreak())

    story.append(Paragraph("How the System Works", styles["SectionTitle"]))
    story.append(
        bullet_list(
            [
                "A new user creates an account and logs in with the user login option.",
                "The user adds important emergency contacts with priority order and email addresses.",
                "The user creates an incident report with descriptive details and location data.",
                "The report is processed by the local AI pipeline to produce category, confidence, danger score, night risk, safety tips, and fake-review indicators.",
                "High-risk or suspicious reports generate alerts that appear on the dashboard.",
                "The map page visualizes saved incidents and also reads the user's current location from the browser.",
                "If an emergency occurs, Emergency Mode records the location summary and emails trusted contacts.",
                "The admin logs in separately to configure SMTP and verify that emergency email delivery is working.",
            ],
            styles,
        )
    )

    story.append(Paragraph("User Interface", styles["SectionTitle"]))
    ui_items = [
        figure(login_screen, "Figure 2. Role-based login page with separate user and admin modes", 15.5, styles),
        figure(register_screen, "Figure 3. Registration page for creating a new user account", 15.5, styles),
        figure(dashboard_screen, "Figure 4. User dashboard with metrics, alerts, and AI insight panels", 15.5, styles),
        figure(report_screen, "Figure 5. Report creation form for incident details and AI analysis workflow", 15.5, styles),
        figure(emergency_screen, "Figure 6. Emergency Mode page with contact priority and rapid action blocks", 15.5, styles),
        figure(map_screen, "Figure 7. Safety map showing current location and coordinate context", 15.5, styles),
        figure(email_screen, "Figure 8. Emergency email output received by a trusted contact", 10.2, styles),
    ]
    for item in ui_items:
        story.append(item)
        story.append(Spacer(1, 0.18 * cm))

    story.append(Paragraph("Important Feature Code", styles["SectionTitle"]))
    story.append(
        Paragraph(
            "The following code excerpts were selected because they show the most important implementation decisions in the project: validation and CRUD, AI-assisted report processing, map rendering, and emergency email generation.",
            styles["Body"],
        )
    )
    story.append(
        code_block(
            "Code Sample 1. Contact validation and save logic from lib/services.php",
            ROOT / "lib" / "services.php",
            13,
            63,
            styles,
        )
    )
    story.append(
        code_block(
            "Code Sample 2. Report save/update pipeline with AI bundle from lib/services.php",
            ROOT / "lib" / "services.php",
            100,
            136,
            styles,
        )
    )
    story.append(
        code_block(
            "Code Sample 3. Heuristic AI bundle assembly from lib/ai.php",
            ROOT / "lib" / "ai.php",
            239,
            258,
            styles,
        )
    )
    story.append(
        code_block(
            "Code Sample 4. Safety map geolocation and current-location storage from safety_map.php",
            ROOT / "safety_map.php",
            90,
            157,
            styles,
        )
    )
    story.append(
        code_block(
            "Code Sample 5. Emergency email location lines and mail body creation from lib/services.php",
            ROOT / "lib" / "services.php",
            319,
            384,
            styles,
        )
    )

    story.append(Paragraph("Problems Faced During Development", styles["SectionTitle"]))
    story.append(
        bullet_list(
            [
                "Configuring XAMPP paths and local routing consistently was difficult during development because the project moved between local folders.",
                "Emergency email delivery depended on correct SMTP credentials and app password configuration, so testing the email workflow required several iterations.",
                "Browser geolocation can fail or be delayed if location permission is denied, which affected the emergency email location field.",
                "Separating admin-only controls from user-only pages required additional session logic and redirects.",
                "Keeping the application fully local meant the AI layer had to be implemented with heuristics rather than external AI APIs.",
            ],
            styles,
        )
    )

    story.append(Paragraph("Conclusion", styles["SectionTitle"]))
    story.append(
        Paragraph(
            "Women Shield successfully demonstrates a complete safety-oriented web application with both CRUD and intelligent workflow features. "
            "The project goes beyond a basic PHP form system because it combines database design, user roles, map integration, email delivery, and a local AI analysis pipeline. "
            "As a result, it satisfies the goal of producing a meaningful full-stack lab project that is practical, testable, and deployable on a local XAMPP environment.",
            styles["Body"],
        )
    )

    story.append(Paragraph("Future Improvement", styles["SectionTitle"]))
    story.append(
        bullet_list(
            [
                "Integrate a real AI API for richer assistant replies and more advanced report analysis.",
                "Add SMS, push notifications, or WhatsApp automation in addition to email alerts.",
                "Allow media uploads such as photos, audio, or evidence attachments with incident reports.",
                "Introduce route recommendation and map clustering for dense hotspot areas.",
                "Add analytics dashboards for authorized moderators while still protecting private user data.",
                "Provide mobile-first optimization and possible native app support for faster emergency access.",
            ],
            styles,
        )
    )

    story.append(Paragraph("Appendix: Notes", styles["SectionTitle"]))
    story.append(
        Paragraph(
            "The instruction PDF requested a cover page from BLC. Since the official BLC cover template was not bundled with the instruction file, this report uses a clean custom cover page and the required PDF output format. "
            "If you receive the official cover template later, it can be inserted as the first page without changing the report content.",
            styles["Body"],
        )
    )

    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=A4,
        rightMargin=1.7 * cm,
        leftMargin=1.7 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.6 * cm,
        title="Women Shield Project Report",
        author="Mohammad Mujahid",
        subject="Lab project report",
    )
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


if __name__ == "__main__":
    build_report()
    print(OUTPUT_PDF)
