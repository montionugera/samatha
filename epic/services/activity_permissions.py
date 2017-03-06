
S_ROLE_AVAILABLE = ['super', 'normal']

NS_ROLE_AVAILABLE = ['owner', 'manager', 'board', 'member']


S_ROLE = {
    'super': ['CRE_NEW_NS']
}
ITEMS = ['ns', 'epic', 'story', 'story-spec', 'role']

NS_ROLE_ACTION_VIEW_EPICS = {'key': 'VIEW_EPICS', 'args': []}

NS_ROLE_ACTION_CRE_NEW_EPIC = {'key': 'CRE_NEW_EPIC', 'args': []}
NS_ROLE_ACTION_MV_EPIC_TO__TODO = {'key': 'MV_EPIC_TO__STATUS__TODO', 'args': ['epic'],
                                   'criteria': ['epic_status_is_w8approve']}#
NS_ROLE_ACTION_ASK_USER_FOR_JOIN_EPIC_AS_ROLE = {'key': 'ASK_USER_FOR_JOIN_EPIC_AS_ROLE',
                                                 'args': ['user', 'epic', 'role']}

NS_ROLE_ACTION_DICT = {
    'owner': [NS_ROLE_ACTION_CRE_NEW_EPIC, NS_ROLE_ACTION_ASK_USER_FOR_JOIN_EPIC_AS_ROLE],  # side
    'member': [NS_ROLE_ACTION_VIEW_EPICS], #common

    'manager': [NS_ROLE_ACTION_CRE_NEW_EPIC, NS_ROLE_ACTION_MV_EPIC_TO__TODO,
                NS_ROLE_ACTION_ASK_USER_FOR_JOIN_EPIC_AS_ROLE,
                ],  # only one person can be
    'board': [NS_ROLE_ACTION_CRE_NEW_EPIC]

}

EPIC_ROLE_ACTION_VIEW_STORIES = {'key': 'VIEW_STORIES', 'args': []}
EPIC_ROLE_ACTION_CRE_NEW_STORY = {'key': 'CRE_NEW_STORY', 'args': ['story']}

EPIC_ROLE_ACTION_ASK_USER_FOR_JOIN_STORY_AS_ROLE = {'key': 'ASK_USER_FOR_JOIN_STORY_AS_ROLE',
                                                 'args': ['user', 'story', 'role']}

EPIC_ROLE_ACTION_MV_STORY_TO__DESIGN_COMPLETE = {'key': 'MV_STORY_TO__DESIGN_COMPLETE', 'args': ['story'],
                                                 'criteria': ['story_specs_complete']}

EPIC_ROLES = ['PO', 'PM', 'SENIOR', 'ANALYST', 'DEV', 'TEST', 'GRAPHIC', 'SUP', 'SCRUM']
STORY_ROLE_AVAILABLE = ['owner', 'manager', 'board', 'member']

EPIC_ROLE_ACTION_DICT = {
    'owner': [EPIC_ROLE_ACTION_CRE_NEW_STORY],
    'member': [EPIC_ROLE_ACTION_VIEW_STORIES], #common
    'PO': [EPIC_ROLE_ACTION_CRE_NEW_STORY],
    'GRAPHIC': [EPIC_ROLE_ACTION_CRE_NEW_STORY],
}

NS_ACTIONS = ['CRE_NEW_NS', 'EDIT_NS', 'DEL_NS', 'ASK_FOR_JOIN_NS']
EPIC_ACTIONS = ['CRE_NEW_EPIC', 'EDIT_EPIC', 'DEL_EPIC', 'ASK_FOR_JOIN_EPIC', 'ASK_FOR_JOIN_EPIC']

STORY_ACTIONS = {'CRE_NEW_STORY',
                 'EDIT_STORY',
                 'ASK_MEMBER_FOR_JOIN_STORY_AS',
                 'MV_STORY_TO_TODO',
                 'ASK_FOR_JOIN_EPIC'}