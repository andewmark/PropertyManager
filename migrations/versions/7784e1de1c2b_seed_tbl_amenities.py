"""seed_tbl_amenities

Revision ID: 7784e1de1c2b
Revises: bb5aa4319e85
Create Date: 2026-03-09 22:54:18.527521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7784e1de1c2b'
down_revision = 'bb5aa4319e85'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        INSERT INTO tbl_amenities (amenity_name) VALUES
        ('Air conditioning'),
        ('Deck/Patio'),
        ('Dishwasher'),
        ('Fireplace'),
        ('Hardwood floors'),
        ('Energy-efficient appliances'),
        ('In-Unit Laundry'),
        ('Private Balcony'),
        ('Outdoor Kitchen'),
        ('Community Events'),
        ('Clubhouse'),
        ('Community Garden'),
        ('Fitness Center'),
        ('Media Room'),
        ('Playground'),
        ('Sports Courts'),
        ('Pool'),
        ('Rooftop Lounge'),
        ('Concierge'),
        ('On-site laundry'),
        ('Storage'),
        ('Dog Park'),
        ('Pet Friendly'),
        ('Pet Daycare'),
        ('Covered Parking'),
        ('Designated parking space'),
        ('EV charging stations'),
        ('Garage'),
        ('Bike Parking'),
        ('Elevators'),
        ('Controlled entry'),
        ('Gated Entrance'),
        ('Security'),
        ('Secure Parking'),
        ('Security Cameras'),
        ('Virtual Doorperson'),
        ('Smart thermostats'),
        ('Daycare')
    """)


def downgrade():
    op.execute("DELETE FROM tbl_amenities")
