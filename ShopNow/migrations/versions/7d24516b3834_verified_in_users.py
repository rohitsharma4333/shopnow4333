"""verified in users

Revision ID: 7d24516b3834
Revises: da9f12bbe66e
Create Date: 2019-01-07 23:41:28.723423

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7d24516b3834'
down_revision = 'da9f12bbe66e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_emailID', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
    op.drop_table('fnagrhd')
    op.drop_index('ix_fnauthtoken_userID_token', table_name='fnauthtoken')
    op.drop_index('ix_fnauthtoken_userID_token_a', table_name='fnauthtoken')
    op.drop_table('fnauthtoken')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fnauthtoken',
    sa.Column('tokenID', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('userID', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('token', mysql.VARCHAR(length=32), nullable=False),
    sa.Column('token_expiration', mysql.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['userID'], ['users.userID'], name='fnauthtoken_ibfk_1'),
    sa.PrimaryKeyConstraint('tokenID'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_fnauthtoken_userID_token_a', 'fnauthtoken', ['token', 'userID'], unique=False)
    op.create_index('ix_fnauthtoken_userID_token', 'fnauthtoken', ['userID', 'token'], unique=False)
    op.create_table('fnagrhd',
    sa.Column('comp_id', mysql.VARCHAR(length=10), nullable=False),
    sa.Column('agr_code', mysql.VARCHAR(length=10), nullable=False),
    sa.Column('agr_seq', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('userID', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['userID'], ['users.userID'], name='fnagrhd_ibfk_1'),
    sa.PrimaryKeyConstraint('comp_id', 'agr_code', 'agr_seq'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('users',
    sa.Column('userID', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('username', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('emailID', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('passwordHash', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('lastSeen', mysql.DATETIME(), nullable=True),
    sa.Column('authorized', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('userID'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_emailID', 'users', ['emailID'], unique=True)
    # ### end Alembic commands ###
