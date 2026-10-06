# Copyright (c) 2026 Lumen Solutions. All rights reserved.
# SPDX-License-Identifier: LicenseRef-Lumen-Proprietary
# Proprietary and confidential. See license.txt. "Lumen Reports" is a trademark of Lumen Solutions.

"""Install/migrate hooks: the app's roles.

Three roles, mirroring how dashboard tools are actually used:

- Fibersoft Viewer            — opens the app, sees published dashboards (subject
                            to each dashboard's audience). Data inside widgets
                            still follows the viewer's own doctype permissions.
- Fibersoft Restricted Viewer — sees ONLY dashboards that name them (personally or
                            via an audience role). The way to hand somebody
                            exactly one dashboard.
- Fibersoft Builder           — Viewer + creates dashboards and edits/deletes their
                            OWN. Can only report on doctypes their roles let
                            them read — the engines enforce that per request.
- Fibersoft Manager           — full control of all dashboards without needing the
                            very broad System Manager role.

Created here (idempotently) rather than shipped as fixtures so a bare
`bench install-app` and every migrate self-heal missing roles.
"""

import frappe

FIBERSOFT_ROLES = ("Fibersoft Viewer", "Fibersoft Restricted Viewer", "Fibersoft Builder", "Fibersoft Manager")


def ensure_roles():
	for name in FIBERSOFT_ROLES:
		if not frappe.db.exists("Role", name):
			frappe.get_doc(
				{"doctype": "Role", "role_name": name, "desk_access": 0}
			).insert(ignore_permissions=True)


def after_install():
	ensure_roles()


def after_migrate():
	ensure_roles()
