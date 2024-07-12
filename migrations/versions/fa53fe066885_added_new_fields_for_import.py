"""added new fields for import

Revision ID: fa53fe066885
Revises: 92ac626e6128
Create Date: 2024-07-12 11:28:41.395965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa53fe066885'
down_revision = '92ac626e6128'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('persons', schema=None) as batch_op:
        batch_op.add_column(sa.Column('h_salesforce_id', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('h_salesforce_account_id', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('secondary_email', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('home_email', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('work_email', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('prefered_email', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('country_code', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('city', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('state', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('postal_code', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('preferred_phone', sa.String(length=15), nullable=True))
        batch_op.add_column(sa.Column('h_owner_id', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('opt_out_email', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('opt_out_phone', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('h_created_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('h_salesforce_primary_aff', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('h_org_name', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('age_group', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('do_not_contact', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('h_connector_join_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('h_connector_last_login_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('h_connecotr_join_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('h_connector_id', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('h_first_volunteer_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('h_num_of_attended_sessions', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('h_num_of_noshow_sessions', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('h_org_name_reported', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('person_of_color', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('racial_ethnic_background', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('status', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('h_last_email_message', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('h_connector_last_update', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('h_connector_signup_role', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('h_last_completed_task', sa.DateTime(), nullable=True))

    with op.batch_alter_table('volunteers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('h_interests', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('h_skills_text', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('h_skills', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('volunteers', schema=None) as batch_op:
        batch_op.drop_column('h_skills')
        batch_op.drop_column('h_skills_text')
        batch_op.drop_column('h_interests')

    with op.batch_alter_table('persons', schema=None) as batch_op:
        batch_op.drop_column('h_last_completed_task')
        batch_op.drop_column('h_connector_signup_role')
        batch_op.drop_column('h_connector_last_update')
        batch_op.drop_column('h_last_email_message')
        batch_op.drop_column('status')
        batch_op.drop_column('racial_ethnic_background')
        batch_op.drop_column('person_of_color')
        batch_op.drop_column('h_org_name_reported')
        batch_op.drop_column('h_num_of_noshow_sessions')
        batch_op.drop_column('h_num_of_attended_sessions')
        batch_op.drop_column('h_first_volunteer_date')
        batch_op.drop_column('h_connector_id')
        batch_op.drop_column('h_connecotr_join_date')
        batch_op.drop_column('h_connector_last_login_date')
        batch_op.drop_column('h_connector_join_date')
        batch_op.drop_column('do_not_contact')
        batch_op.drop_column('age_group')
        batch_op.drop_column('h_org_name')
        batch_op.drop_column('h_salesforce_primary_aff')
        batch_op.drop_column('h_created_date')
        batch_op.drop_column('opt_out_phone')
        batch_op.drop_column('opt_out_email')
        batch_op.drop_column('h_owner_id')
        batch_op.drop_column('preferred_phone')
        batch_op.drop_column('postal_code')
        batch_op.drop_column('state')
        batch_op.drop_column('city')
        batch_op.drop_column('country_code')
        batch_op.drop_column('prefered_email')
        batch_op.drop_column('work_email')
        batch_op.drop_column('home_email')
        batch_op.drop_column('secondary_email')
        batch_op.drop_column('h_salesforce_account_id')
        batch_op.drop_column('h_salesforce_id')

    # ### end Alembic commands ###
