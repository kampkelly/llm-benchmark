"""add indexes for simulation table

Revision ID: 650a9a53c36d
Revises: 65c8b03c1a03
Create Date: 2024-09-22 22:46:26.450178

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '650a9a53c36d'
down_revision: Union[str, None] = '65c8b03c1a03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_simulations_llm_id', 'simulations', ['llm_id'], unique=False)
    op.create_index('ix_simulations_metric_id', 'simulations', ['metric_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_simulations_metric_id', table_name='simulations')
    op.drop_index('ix_simulations_llm_id', table_name='simulations')
    # ### end Alembic commands ###
