"""seed_tbl_utlities

Revision ID: 59f312d538aa
Revises: 965212806375
Create Date: 2026-03-11 21:55:17.589998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59f312d538aa'
down_revision = '965212806375'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        INSERT INTO tbl_utilities (utility_name)
        VALUES ('Water'),
	   ('Sewer'), 	
	   ('Electricity'),
	   ('Natural Gas'),
	   ('Trash'),
	   ('Security'),
	   ('Internet')
    """)


def downgrade():
    op.execute("DELETE FROM tbl_utilities")
