# Installing and migrating Fibersoft Reports

Fibersoft Reports is a rebranded fork of Lumen Reports. Original copyright,
license and trademark notices remain in place. `license.txt` still governs the
code; publishing this fork does not grant an open-source license.

## Fresh installation

Use an existing Frappe bench (the app declares Frappe >=14,<17 and Python >=3.10).
ERPNext is optional. Building the frontend requires Node 18 or newer and Yarn
Classic. Built frontend assets are also included in the repository.

```bash
bench get-app https://github.com/Faizan-Sab/fibersoft_reports
bench --site your-site.localhost install-app fibersoft_reports
bench build --app fibersoft_reports
bench --site your-site.localhost migrate
bench --site your-site.localhost clear-cache
bench restart
```

Open `/fibersoft`. Assign Fibersoft Viewer, Fibersoft Restricted Viewer,
Fibersoft Builder or Fibersoft Manager as appropriate. Permissions to the data
being reported remain necessary. AI requires the existing optional Gemini setup;
PDF export requires the dependencies described in README.md.

## Existing Lumen Reports sites

This is a **new app identity**, not an automatic upgrade. `bench migrate` does
not turn Lumen records into Fibersoft records. Installing the new package creates
new DocTypes and roles; existing dashboards remain in the old app until migrated.
Do not uninstall the old app as a migration step: uninstalling deletes its data.

Back up the database and files and rehearse the transfer on a restored staging
site before any production cutover. Keep both source packages available during
the transfer, and pause scheduled report delivery to avoid duplicate emails.

The following DocType mappings must be applied, including child documents and
their `doctype`, `parenttype` and link metadata:

| Old DocType | New DocType |
| --- | --- |
| Lumen Dashboard | Fibersoft Dashboard |
| Lumen Widget | Fibersoft Widget |
| Lumen Dashboard Role | Fibersoft Dashboard Role |
| Lumen Dashboard User | Fibersoft Dashboard User |
| Lumen Brand | Fibersoft Brand |
| Lumen AI Settings | Fibersoft AI Settings |
| Lumen AI Site Settings | Fibersoft AI Site Settings |
| Lumen Report Schedule | Fibersoft Report Schedule |
| Lumen Report Recipient | Fibersoft Report Recipient |

Use an administrator-assisted export/import into the new DocTypes, preserving
document names, dashboard slugs, owners, audiences, child order and schedule
links. Transfer dashboards before their report schedules. Single DocType settings
(brand and site AI settings) need explicit copying; ordinary list exports do not
include them. Re-enter encrypted API keys through the new settings screens;
masked password values are not portable secrets. Copy user role assignments:
Lumen Viewer/Restricted Viewer/Builder/Manager become the corresponding
Fibersoft roles. Check private audiences and role-based dashboard access.

Review stored theme identifiers and JSON preferences for app-specific Lumen
names, and update links to app-owned uploaded logos under
`/assets/lumen_reports/` to `/assets/fibersoft_reports/`. Keep `/files/` and
`/private/files/` URLs and the corresponding uploaded files intact. Update
integrations and external bookmarks as follows:

| Interface | New value |
| --- | --- |
| Python import / API prefix | `fibersoft_reports` |
| App module | `Fibersoft Reports` |
| Page and SPA route prefix | `/fibersoft` |
| Asset prefix | `/assets/fibersoft_reports/` |
| Realtime/cache/browser preference identifiers | `fibersoft…` equivalents |
| LumenPOS integration API | `fibersoft_reports.integrations.lumenpos` |

LumenPOS is a separate application: its names, role names and POS identifiers
are unchanged. Its caller must use the new integration API prefix and returned
URLs. Existing browser preferences can be reset to defaults after the cutover.

The subscription key remains **`sk_lumen_reports`**, and verification still
uses the original licensor's service. The rebrand does not disable checks or
create a new entitlement. Keep the existing authorized subscription setup.

Verify dashboard counts, child widgets, private access, AI, report/PDF export,
embedded dashboards and scheduled delivery on staging. Enable only the new
schedule runner at cutover. Retain the old app and backup until the migration is
accepted; removing it later is a separate administrative operation.

For schema migration behavior, see the
[Frappe migration documentation](https://docs.frappe.io/framework/user/en/guides/deployment/migrations).
