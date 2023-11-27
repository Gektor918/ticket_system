from model import *

db = DatabaseManager()


async def create_tables() -> dict:
    """
    Create tables in db
    """
    async with db:
        status = await db.create_tables()
    return status


async def create_employee(name: str) -> asyncpg.Record:
    """
    Create employee
    """
    async with db:
        employee = await db.create_employee(name)
    return employee


async def filtered_tickets(status: str, assigned_employee: int, sort_by: str) -> List[dict]:
    """
    Filtered tickets
    """ 
    async with db:
        tickets = await db.filtered_tickets(status=status, assigned_employee=assigned_employee, sort_by=sort_by)
    return tickets


async def all_employees() -> asyncpg.Record:
    """
    Get one employees
    """
    async with db:
        employees = await db.get_all_employees()
    return employees


async def get_ticket_by_id(ticket_id: int) -> Optional[dict]:
    """
    Get one tickets
    """
    async with db:
        ticket = await db.get_ticket_by_id(ticket_id)
    return ticket


async def get_employee_by_id(employee: int) -> asyncpg.Record:
    """
    Get one employee
    """
    async with db:
        employee = await db.get_employee_by_id(employee)
    return employee


async def update_ticket_status(ticket_id: int, new_status: str) -> asyncpg.Record:
    """
    Update tickets status
    """
    async with db:
        updated_ticket = await db.update_ticket_status(ticket_id, new_status)
    return updated_ticket


async def update_ticket_employee(ticket_id: int, employee_id: int) -> asyncpg.Record:
    """
    Update tickets employee
    """
    async with db:
        updated_ticket = await db.update_employee_ticket(ticket_id, employee_id)
    return updated_ticket