from src.schemas.team import TeamOut
from src.schemas.user import UserOut, AdminUserOut

TeamOut.model_rebuild()
UserOut.model_rebuild()
AdminUserOut.model_rebuild()
