"""createa post table

Revision ID: d194a1eb70f4
Revises: 
Create Date: 2023-12-20 10:12:45.369377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd194a1eb70f4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    pass
   
def downgrade():
    pass
