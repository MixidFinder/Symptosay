from alembic import op
import sqlalchemy as sa

revision = '000000000000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'diseases',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(200), nullable=False, unique=True, index=True),
        sa.Column('description', sa.Text(), nullable=True),
    )

    op.create_table(
        'symptoms',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(200), nullable=False, unique=True, index=True),
        sa.Column('description', sa.Text(), nullable=True),
    )

    op.create_table(
        'disease_symptom',
        sa.Column('disease_id', sa.Integer(), sa.ForeignKey('diseases.id'), primary_key=True),
        sa.Column('symptom_id', sa.Integer(), sa.ForeignKey('symptoms.id'), primary_key=True),
    )

    op.create_table(
        'user_symptoms',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('symptom_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_table('user_symptoms')
    op.drop_table('disease_symptom')
    op.drop_table('symptoms')
    op.drop_table('diseases')
