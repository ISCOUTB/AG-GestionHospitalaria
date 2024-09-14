from app.schemas.users import (
    UserBase,
    User,
    UserAll,
    UserLogin,
    UserSearch,
    UserUpdate,
    UserCreate,
    Roles
)

from app.schemas.token import (
    Token,
    TokenPayload
)

from app.schemas.doctors import (
    SpecialityBase,
    Speciality,
    DoctorAll
)

from app.schemas.patient import (
    ResponsablesInfo,
    PatientAll
)

from app.schemas.beds import (
    BedBase,
    UseBed,
    VacateBed
)

from app.schemas.consults import (
    RegisterConsult,
    RegisterHospitalization,
    DischargeHospitalization
)

import app.schemas.models as models
