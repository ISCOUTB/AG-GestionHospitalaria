import datetime

from sqlalchemy import Column, Date, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import BaseModel


class UsersInfo(BaseModel):
    __tablename__ = 'users_info'

    number_document = Column(String, primary_key=True)
    type_document = Column(String, default=None, nullable=True)
    name = Column(String, default=None, nullable=True)
    surname = Column(String, default=None, nullable=True)
    sex = Column(String, default=None, nullable=True)
    birthday = Column(Date, default=None, nullable=True)
    address = Column(String, default=None, nullable=True)
    phone = Column(String, default=None, nullable=True)

    user_roles = relationship('UserRoles', uselist=False, back_populates='users_info',
                              passive_deletes=True, passive_updates=True)


class UserRoles(BaseModel):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    num_document = Column(String, ForeignKey('users_info.number_document'), nullable=False)
    rol = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    inactivity = Column(Date, default=None, nullable=True)

    users_info = relationship('UsersInfo', uselist=False, back_populates='user_roles',
                              passive_deletes=True, passive_updates=True)
    patient_info = relationship('PatientInfo', uselist=False, back_populates='user_roles',
                                passive_deletes=True, passive_updates=True)
    doctor_specialities = relationship('DoctorSpecialities', uselist=False, back_populates='user_roles',
                                       passive_deletes=True, passive_updates=True)
    beds_used = relationship('BedsUsed', uselist=False, back_populates='user_roles',
                             passive_deletes=True, passive_updates=True)
    medical_consults = relationship('MedicalConsults', uselist=False, back_populates='user_roles',
                                    passive_deletes=True, passive_updates=True)
    hospitalizations = relationship('Hospitalizations', uselist=False, back_populates='user_roles',
                                    passive_deletes=True, passive_updates=True)


class PatientInfo(BaseModel):
    __tablename__ = 'patient_info'

    patient_id = Column(Integer, ForeignKey('user_roles.id'), primary_key=True)
    num_doc_responsable = Column(String, default=None, nullable=True)
    type_doc_responsable = Column(default=None, nullable=True)
    name_responsable = Column(String, default=None, nullable=True)
    surname_responsable = Column(String, default=None, nullable=True)
    relationship_responsable = Column(String, default=None, nullable=True)

    user_roles = relationship('UserRoles', uselist=False, back_populates='patient_info',
                              passive_deletes=True, passive_updates=True)


class Specialities(BaseModel):
    __tablename__ = 'specialities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    doctor_specialities = relationship('DoctorSpecialities', uselist=False, back_populates='specialities',
                                       passive_deletes=True, passive_updates=True)


class DoctorSpecialities(BaseModel):
    __tablename__ = 'doctor_specialities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey('user_roles.id'), nullable=False)
    speciality_id = Column(Integer, ForeignKey('specialities.id'), nullable=False)

    specialities = relationship('Specialities', uselist=False, back_populates='doctor_specialities',
                                passive_deletes=True, passive_updates=True)
    user_roles = relationship('UserRoles', uselist=False, back_populates='doctor_specialities',
                              passive_deletes=True, passive_updates=True)


class Beds(BaseModel):
    __tablename__ = 'beds'

    id = Column(Integer, primary_key=True, autoincrement=True)
    room = Column(String, nullable=False)

    beds_used = relationship('BedsUsed', uselist=False, back_populates='',
                             passive_deletes=True, passive_updates=True)
    

class BedsUsed(BaseModel):
    __tablename__ = 'beds_used'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_bed = Column(Integer, ForeignKey('beds.id'), nullable=False)
    id_patient = Column(Integer, ForeignKey('user_roles.id'), nullable=False)
    id_doctor = Column(Integer, ForeignKey('user_roles.id'), nullable=False)

    beds = relationship('Beds', uselist=False, back_populates='beds_used',
                        passive_deletes=True, passive_updates=True)
    user_roles = relationship('UserRoles', uselist=False, back_populates='beds_used',
                              passive_deletes=True, passive_updates=True)


class MedicalConsults(BaseModel):
    __tablename__ = 'medical_consults'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_patient = Column(Integer, ForeignKey('user_roles.id'), nullable=False)
    id_doctor = Column(Integer, ForeignKey('user_roles.id'), nullable=False)
    area = Column(String, nullable=False)
    day = Column(Date, default=datetime.date.today(), nullable=False)

    user_roles = relationship('UserRoles', uselist=False, back_populates='medical_consults',
                              passive_deletes=True, passive_updates=True)


class Hospitalizations(BaseModel):
    __tablename__ = 'hospitalizations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_patient = Column(Integer, ForeignKey('user_roles.id'), nullable=False)
    id_doctor = Column(Integer, ForeignKey('user_roles.id'), nullable=False)
    entry_day = Column(Date, default=datetime.date.today(), nullable=False)
    last_day = Column(Date, default=None, nullable=True)

    user_roles = relationship('UserRoles', uselist=False, back_populates='hospitalizations',
                              passive_deletes=True, passive_updates=True)
