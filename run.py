from check_for_updates import check
from release import update

v = check()

if v is not None:
    update(v)
