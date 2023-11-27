from typing import List, Optional

from fastapi import FastAPI, Form, Query

from bot import message
from model import *
from services_views import *

app = FastAPI()


@app.post("/create_tables/", response_model=List[dict])
async def create_tables_views():
    """
    Create tables in db
    """
    status = await create_tables()
    return [dict(status)]


@app.post("/create_employee/", response_model=List[dict])
async def create_employee_views(name:str = Form(description="Name employee")):
    """
    Create employee
    """
    employee = await create_employee(name)
    return [dict(employee)]


@app.get("/filtered_tickets/", response_model=List[dict])
async def filtered_tickets_views(
    status: Optional[str] = Query(None, description="Filter tickets by status Открыт В работе Закрыт"),
    assigned_employee: Optional[int] = Query(None, description="Filter tickets by assigned employee"),
    sort_by: Optional[str] = Query("creation_date", description="Sort tickets by creation_date or update_date"),
    ):
    """
    Filtered tickets
    """
    tickets = await filtered_tickets(status, assigned_employee, sort_by)
    return tickets


@app.get("/all_employees/", response_model=List[dict])
async def employees():
    """
    All employee in system
    """
    employees = await all_employees()
    return [dict(employees)]


@app.put("/update_ticket_status/", response_model=List[dict])
async def update_ticket_status_views(
    ticket_id:int = Form(..., description="Id ticket"),
    new_status:str = Form(..., description="New status ticket, Открыт В работе Закрыт")
    ):
    """
    Update ticket
    """
    if new_status not in ['Открыт','В работе','Закрыт']:
        raise HTTPException(status_code=400, detail=f"Status ticket {new_status} impossible")

    ticket = await get_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket with ID {ticket_id} not found")

    updated_ticket = await update_ticket_status(ticket_id, new_status)

    return [dict(updated_ticket)]


@app.put("/appointment_employee/", response_model=List[dict])
async def appointment_employee_views(
    ticket_id:int = Form(..., description="Id ticket"),
    employee_id:int = Form(..., description="Id employee")
    ):
    """
    Update employee in ticket
    """
    ticket = await get_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket with ID {ticket_id} not found")

    employee = await get_employee_by_id(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} not found")

    updated_ticket = await update_ticket_employee(ticket_id, employee_id)

    return [dict(updated_ticket)]


@app.post("/message/", response_model=List[dict])
async def message_views(
    ticket_id:int = Form(description="Id ticket"),
    text:str = Form(description="New message to the client in telegram")
    ): 
    """
    Sending a message to the client
    """
    ticket = await get_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket with ID {ticket_id} not found")

    resp_message = await message(ticket['id_chat'], text)
    return [dict(resp_message)]