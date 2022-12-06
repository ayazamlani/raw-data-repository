"""change_setatbirth_for_workspace__model

Revision ID: e968d868a097
Revises: ec6018a5919f
Create Date: 2020-02-04 11:33:00.348870

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e968d868a097'
down_revision = 'ec6018a5919f'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    if engine_name == "rdr" or engine_name == "metrics":
        globals()[f"upgrade_{engine_name}"]()
    else:
        pass


def downgrade(engine_name):
    if engine_name == "rdr" or engine_name == "metrics":
        globals()[f"downgrade_{engine_name}"]()
    else:
        pass



def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TABLE `workbench_researcher` MODIFY `sex_at_birth` JSON;")
    op.execute("ALTER TABLE `workbench_researcher_history` MODIFY `sex_at_birth` JSON;")
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TABLE `workbench_researcher` MODIFY `sex_at_birth` smallint(6);")
    op.execute("ALTER TABLE `workbench_researcher_history` MODIFY `sex_at_birth` smallint(6);")
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
