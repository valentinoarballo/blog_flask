"""comentarios_descripcion_estaba_como_int_xd

Revision ID: 5d62425f3531
Revises: efcadc9c0031
Create Date: 2023-07-02 13:25:58.289421

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5d62425f3531'
down_revision = 'efcadc9c0031'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comentario', schema=None) as batch_op:
        batch_op.alter_column('descripcion',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('id_publicacion',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
        batch_op.drop_constraint('comentario_ibfk_2', type_='foreignkey')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comentario', schema=None) as batch_op:
        batch_op.create_foreign_key('comentario_ibfk_2', 'publicacion', ['descripcion'], ['id'])
        batch_op.alter_column('id_publicacion',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
        batch_op.alter_column('descripcion',
               existing_type=sa.String(length=100),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=False)

    # ### end Alembic commands ###
