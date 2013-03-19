from ftw.lawgiver.interfaces import IActionGroupRegistry
from zope.interface import implements


class ActionGroupRegistry(object):

    implements(IActionGroupRegistry)

    def __init__(self):
        self._permissions = {}

    def update(self, action_group, permissions, workflow=None):
        for perm in permissions:
            if perm not in self._permissions:
                self._permissions[perm] = {}

            self._permissions[perm][workflow] = action_group

    def get_action_groups_for_workflow(self, workflow_name):
        result = {}

        for permission, workflows in self._permissions.items():
            if workflow_name in workflows:
                wfname = workflow_name
            elif None in workflows:
                wfname = None
            else:
                continue

            group = workflows[wfname]
            if group not in result:
                result[group] = set()

            result[group].add(permission)

        return result

    def get_action_group_for_permission(self, permission_title,
                                        workflow_name=None):
        if permission_title not in self._permissions:
            return None

        permission = self._permissions[permission_title]
        return permission.get(workflow_name, permission.get(None, None))