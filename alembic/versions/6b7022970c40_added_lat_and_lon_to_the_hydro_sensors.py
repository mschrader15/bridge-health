"""Added lat and lon to the hydro sensors

Revision ID: 6b7022970c40
Revises: cc970fd452f9
Create Date: 2020-08-23 14:25:11.366565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b7022970c40'
down_revision = 'cc970fd452f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hydro_sensors', sa.Column('latitude', sa.DECIMAL(precision=8, scale=6), nullable=True))
    op.add_column('hydro_sensors', sa.Column('longitude', sa.DECIMAL(precision=9, scale=6), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hydro_sensors', 'longitude')
    op.drop_column('hydro_sensors', 'latitude')
    # ### end Alembic commands ###
