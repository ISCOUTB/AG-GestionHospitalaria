"""Agregar tablas a la base de datos

Revision ID: a698f22123fe
Revises: 
Create Date: 2024-10-05 18:26:57.891599

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a698f22123fe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users_info',
    sa.Column('num_document', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('type_document', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('surname', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('sex', sa.VARCHAR(length=1), server_default=sa.text('NULL::character varying'), autoincrement=False, nullable=True),
    sa.Column('birthday', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('address', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('phone', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('email', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('num_document', name='pk_users_info'),
    sa.UniqueConstraint('email', name='users_info_unique_email')
    )
    op.create_table('user_roles',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('user_roles_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('num_document', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('rol', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('password', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False),
    sa.Column('inactivity', sa.DATE(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['num_document'], ['users_info.num_document'], name='fk_users_rol_number_document', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='pk_users_rol'),
    sa.UniqueConstraint('num_document', 'rol', name='unique_users_rol'),
    postgresql_ignore_search_path=False
    )
    op.create_table('patient_info',
    sa.Column('patient_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('num_doc_responsable', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('type_doc_responsable', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('name_responsable', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('surname_responsable', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('phone_responsable', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('relationship_responsable', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['user_roles.id'], name='fk_patient_info_patient_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('patient_id', name='pk_patient_info')
    )
    op.create_table('beds',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('room', sa.TEXT(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_beds'),
    sa.UniqueConstraint('room', name='beds_room_key')
    )
    op.create_table('beds_used',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('id_bed', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id_patient', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id_doctor', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id_bed'], ['beds.id'], name='fk_beds_used_id_bed', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_doctor'], ['user_roles.id'], name='fk_beds_id_doctor', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_patient'], ['user_roles.id'], name='fk_beds_id_patient', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='pk_beds_used'),
    sa.UniqueConstraint('id_bed', name='beds_used_id_bed_key')
    )
    op.create_table('specialities',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('specialities_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_specialities'),
    postgresql_ignore_search_path=False
    )
    op.create_table('doctor_specialities',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('doctor_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('speciality_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['user_roles.id'], name='fk_doctor_specialities_doctor_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['speciality_id'], ['specialities.id'], name='fk_doctor_specialities_speciality_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='pk_doctor_specialities')
    )
    op.create_table('hospitalizations',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('id_patient', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id_doctor', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('entry_day', sa.DATE(), server_default=sa.text('CURRENT_DATE'), autoincrement=False, nullable=False),
    sa.Column('last_day', sa.DATE(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_doctor'], ['user_roles.id'], name='fk_hospitalizations_id_doctor', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_patient'], ['user_roles.id'], name='fk_hospitalizations_id_patient', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='pk_hospitalizations')
    )
    op.create_table('medical_consults',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('id_patient', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id_doctor', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('area', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('day', sa.DATE(), server_default=sa.text('CURRENT_DATE'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id_doctor'], ['user_roles.id'], name='fk_medical_consults_id_doctor', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_patient'], ['user_roles.id'], name='fk_medical_consults_id_patient', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='pk_medical_consults')
    )


def downgrade() -> None:
    pass