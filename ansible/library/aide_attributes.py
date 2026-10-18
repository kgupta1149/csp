#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import re

def parse_config(lines):
    rules = {}       # rule name -> list of attributes, e.g. {"CONTENT": ["sha512", "ftype"]}
    in_use = set()   # rule names actually used by selection lines
    for line in lines:
        line = line.strip()
        # Rule definition: NAME = a+b+c
        m = re.match(r'^([A-Za-z_]+)\s*=\s*(.+)$', line)
        if m and '@@' not in m.group(2) and 'file:' not in m.group(2):
            rules[m.group(1)] = m.group(2).split('+')
            continue
        # Selection line: /path RULE
        m = re.match(r'^(/\S*)\s+(\S+)$', line)
        if m:
            in_use.add(m.group(2))
    return rules, in_use

def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type='str', default='/etc/aide.conf'),
            required=dict(type='list', elements='str', default=['acl', 'xattrs']),
        ),
        supports_check_mode=True,
    )
    with open(module.params['path']) as f:
        lines = f.readlines()

    rules, in_use = parse_config(lines)
    missing = {}
    for rule in in_use:
        attrs = rules.get(rule, [])
        lacking = [a for a in module.params['required'] if a not in attrs]
        if lacking:
            missing[rule] = lacking

    module.exit_json(changed=bool(missing), missing=missing)

if __name__ == '__main__':
    main()