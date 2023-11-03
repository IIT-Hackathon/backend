"""Initialize The DB again

Revision ID: 695c2606dfbe
Revises: 
Create Date: 2023-11-03 08:44:00.707908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '695c2606dfbe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('dob', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tax_reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('income', sa.Integer(), nullable=False),
    sa.Column('taxable_income', sa.Integer(), nullable=False),
    sa.Column('tax', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('breakdown', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tax_reports')
    op.drop_table('users')
    # ### end Alembic commands ###