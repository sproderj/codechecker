"""
add run labels

Revision ID: 173ad938f233
Revises:     feb5f01b5b52
Create Date: 2026-09-25 10:38:41.632973
"""

from logging import getLogger

from alembic import op
import sqlalchemy as sa



# Revision identifiers, used by Alembic.
revision = '173ad938f233'
down_revision = 'feb5f01b5b52'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'run_labels',
        sa.Column(
            'id',
            sa.BigInteger().with_variant(sa.Integer, "sqlite"),
            primary_key=True
        ),
        sa.Column('label_name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.UniqueConstraint('label_name', name='uq_run_label_name')
    )
    op.create_index('ix_run_labels_label_name', 'run_labels', ['label_name'])

    op.create_table(
        'run_to_run_labels',
        sa.Column(
            'run_id',
            sa.BigInteger().with_variant(sa.Integer, "sqlite"),
            sa.ForeignKey('runs.id', ondelete='CASCADE'),
            primary_key=True
        ),
        sa.Column(
            'run_label_id',
            sa.BigInteger().with_variant(sa.Integer, "sqlite"),
            sa.ForeignKey('run_labels.id', ondelete='CASCADE'),
            primary_key=True
        )
    )
    op.create_index(
        'ix_run_to_run_labels_run_id',
        'run_to_run_labels',
        ['run_id']
    )
    op.create_index(
        'ix_run_to_run_labels_label_id',
        'run_to_run_labels',
        ['run_label_id']
    )


def downgrade():
    op.drop_table('run_to_run_labels')

    op.drop_index('ix_run_labels_label_name', table_name='run_labels')
    op.drop_table('run_labels')
