from app.schemas.users import (
    UserBase,
    User,
    UserAll,
    UserLogin,
    UserSearch,
    UserUpdate,
    UserUpdateAll,
    UserCreate,
    Roles,
)

from app.schemas.token import Token, TokenPayload

from app.schemas.doctors import SpecialityBase, Speciality, DoctorAll

from app.schemas.patient import ResponsablesInfo, PatientAll

from app.schemas.beds import BedBase, BedAll, UseBed, VacateBed

from app.schemas.consults import (
    BaseAppointment,
    Consultation,
    RegisterHospitalization,
    DischargeHospitalization,
    Hospitalization,
)

import app.schemas.models as models

from app.schemas.documents import Files
