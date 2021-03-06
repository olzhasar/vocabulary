"""Add WordVariant

Revision ID: 329bf9a06bd2
Revises: de5c815d1c8f
Create Date: 2020-09-28 00:33:15.478221

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '329bf9a06bd2'
down_revision = 'de5c815d1c8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('word_variants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word_id', sa.Integer(), nullable=True),
    sa.Column('part_of_speech', sa.String(length=32), nullable=False),
    sa.Column('definition', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['word_id'], ['words.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_word_variants_part_of_speech'), 'word_variants', ['part_of_speech'], unique=False)
    op.drop_column('words', 'description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('words', sa.Column('description', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_word_variants_part_of_speech'), table_name='word_variants')
    op.drop_table('word_variants')
    # ### end Alembic commands ###
