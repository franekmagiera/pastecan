from contextlib import asynccontextmanager
import sqlalchemy as sa
from sqlalchemy.sql.schema import ForeignKey
from pastecan.mock_data import mock_users_data, mock_user_pastes_data, mock_pastes_data


metadata = sa.MetaData()

login_sessions_table_name = 'login_sessions'
login_sessions_table = sa.Table(login_sessions_table_name, metadata,
                                sa.Column('oauth_token', sa.String(767), primary_key=True, autoincrement=False),
                                sa.Column('oauth_token_secret', sa.String(3072))
)

users_table_name = 'users'
users_table = sa.Table(users_table_name, metadata,
                       sa.Column('user_id', sa.String(767), primary_key=True, autoincrement=False),
                       sa.Column('screen_name', sa.String(30)))

pastes_table_name = 'pastes_table'
pastes_table = sa.Table(pastes_table_name, metadata,
                        sa.Column('id', sa.Integer, primary_key=True),
                        sa.Column('content', sa.Text(20000)),
                        sa.Column('language', sa.String(20)),
                        sa.Column('date', sa.TIMESTAMP),
                        sa.Column('title', sa.String(20)),
                        sa.Column('user_id', sa.String(767), ForeignKey(users_table.c.user_id)),
                        sa.Column('exposure', sa.String(8)))

@asynccontextmanager
async def transaction_context(connection):
    transaction = await connection.begin()
    try:
        yield connection
    except:
        await transaction.rollback()
        raise
    else:
        await transaction.commit()

async def create_tables(engine):
    async with engine.acquire() as conn:
        async with transaction_context(conn) as tc_conn:
            await tc_conn.execute(sa.schema.CreateTable(login_sessions_table, if_not_exists=True))
            await tc_conn.execute(sa.schema.CreateTable(users_table, if_not_exists=True))
            await tc_conn.execute(sa.schema.CreateTable(pastes_table, if_not_exists=True))

async def insert_mock_data(engine):
    async with engine.acquire() as conn:
        async with transaction_context(conn) as tc_conn:
            insert_users = users_table.insert().prefix_with("IGNORE")
            await tc_conn.execute(insert_users, mock_users_data)

            insert_pastes = pastes_table.insert().prefix_with("IGNORE")
            await tc_conn.execute(insert_pastes, mock_pastes_data)

            await tc_conn.execute(insert_pastes, mock_user_pastes_data)

