
export const GROUP_USER = 'User'
export const GROUP_MOD = 'Moderator'
export const GROUP_ADMIN = 'Administrator'

export const GROUPS_ACCESS = {
    undefined: -1,
    [GROUP_USER]: 1,
    [GROUP_MOD]: 100,
    [GROUP_ADMIN]: 1000
}
