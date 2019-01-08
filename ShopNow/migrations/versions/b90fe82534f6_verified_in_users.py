"""verified in users

Revision ID: b90fe82534f6
Revises: afebe03d2421
Create Date: 2019-01-06 13:39:10.183272

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b90fe82534f6'
down_revision = 'afebe03d2421'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_emailID', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
    op.drop_table('fnagrhd')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
