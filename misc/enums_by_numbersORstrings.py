from enum import Enum, auto

class OrganizationRole(Enum):
    CEO = auto() # = "ceo"
    PRESIDENT = auto() # = "president"
    MANAGER = auto() # = "manager"
    STAFF = auto() # = "staff"

class OrgRoleRange(Enum):
    CEO, PRESIDENT, MANAGER, STAFF = range(4)

def main():
    my_role = OrganizationRole.MANAGER
    print(my_role)
    print(my_role.value)

if __name__ == '__main__':
    main()
