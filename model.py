from typing import List, Optional

import asyncpg
from fastapi import HTTPException


class DatabaseManager:

    def __init__(self, database_url = "Your settings"):
        self.database_url = database_url
        self._database = None


    async def __aenter__(self):
        self._database = await asyncpg.connect(self.database_url)
        return self


    async def __aexit__(self, exc_type, exc, tb):
            await self._database.close()


    async def create_tables(self):
        employee_table_query = """
        CREATE TABLE IF NOT EXISTS employee (
            id SERIAL PRIMARY KEY,
            name VARCHAR(75) NOT NULL
        );
        """
        ticket_table_query = """
        CREATE TABLE IF NOT EXISTS ticket (
            id SERIAL PRIMARY KEY,
            id_chat INTEGER NOT NULL,
            user_name VARCHAR(75) NOT NULL,
            text TEXT NOT NULL,
            creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(50) CHECK (status IN ('Открыт', 'В работе', 'Закрыт')),
            assigned_employee_id INTEGER REFERENCES employee(id)
        );
        CREATE OR REPLACE FUNCTION update_ticket_timestamp()
        RETURNS TRIGGER AS $$
        BEGIN
        NEW.update_date = CURRENT_TIMESTAMP;
        RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER update_ticket_trigger
        BEFORE UPDATE ON ticket
        FOR EACH ROW
        EXECUTE FUNCTION update_ticket_timestamp();
    """
        try:
            await self._database.execute(employee_table_query)
            await self._database.execute(ticket_table_query)
            return {"status": "Tables and trigger created successfully."}
        except Exception as e:
            return {"status": "Tables are ready"}


    async def create_employee(self, name: str) -> asyncpg.Record:
        query = "INSERT INTO employee (name) VALUES ($1) RETURNING id, name;"
        employee = await self._database.fetchrow(query, name)
        return employee


    async def create_ticket(self, id_chat: int, user_name: str, message_text: str) -> asyncpg.Record:
        query = """
        INSERT INTO ticket (id_chat, user_name, text, status, assigned_employee_id)
        VALUES ($1, $2, $3, 'Открыт', NULL)
        RETURNING id, id_chat, user_name, text, creation_date, update_date, status, assigned_employee_id;
        """
        return await self._database.fetchrow(query, id_chat, user_name, message_text)


    async def filter_in_ticket(self, id_chat: int) -> asyncpg.Record:
        status = 'Открыт'
        query = """
        SELECT * FROM ticket
        WHERE id_chat = $1 AND status = $2;
        """
        tickets = await self._database.fetch(query, id_chat, status)
        return tickets


    async def get_ticket_by_id(self, ticket_id: int) -> Optional[dict]:
        query = """
        SELECT * FROM ticket
        WHERE id = $1;
        """
        ticket = await self._database.fetchrow(query, ticket_id)
        return dict(ticket) if ticket else None


    async def get_employee_by_id(self, employee_id: int) -> Optional[dict]:
        query = """
        SELECT * FROM employee
        WHERE id = $1;
        """
        employee = await self._database.fetchrow(query, employee_id)
        return dict(employee) if employee else None


    async def get_all_employees(self) -> asyncpg.Record:
        query = """
        SELECT * FROM employee;
        """
        employees = await self._database.fetch(query)
        return employees


    async def update_ticket_status(self, ticket_id: int, new_status: str) -> asyncpg.Record:
        query = """
        UPDATE ticket
        SET status = $1
        WHERE id = $2
        RETURNING *;
        """
        updated_ticket = await self._database.fetchrow(query, new_status, ticket_id)
        return updated_ticket


    async def update_employee_ticket(self, ticket_id: int, employee_id: int) -> asyncpg.Record:
        query = """
        UPDATE ticket
        SET assigned_employee_id = $1
        WHERE id = $2
        RETURNING *;
        """
        updated_ticket = await self._database.fetchrow(query, ticket_id, employee_id)
        return updated_ticket


    async def filtered_tickets(
        self,
        status: Optional[str] = None,
        assigned_employee: Optional[int] = None,
        sort_by: Optional[str] = "creation_date",
        sort_order: Optional[str] = "DESC",
    ) -> List[dict]:

        where_clause = []
        if status:
            where_clause.append(f"status = '{status}'")
        if assigned_employee:
            where_clause.append(f"assigned_employee_id = {assigned_employee}")

        where_condition = " AND ".join(where_clause) if where_clause else "1=1"

        order_by_clause = f"ORDER BY {sort_by} {sort_order}"

        query = f"""
            SELECT * FROM ticket
            WHERE {where_condition}
            {order_by_clause};
        """

        records = await self._database.fetch(query)
        
        return [dict(record) for record in records]


    async def fetch_data_from_db(self, query: str) -> asyncpg.Record:
        if not self._database:
            raise HTTPException(status_code=500, detail="Database connection not established")
        return await self._database.fetch(query)