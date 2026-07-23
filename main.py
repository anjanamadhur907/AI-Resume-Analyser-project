from typing import Optional

from fastapi import FastAPI, Form, UploadFile, File
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from src.db.dbConfig import SessionLocal
from src.exception.global_exception_handler import sqlalchemy_exception_handler, resource_not_found_exception_handler
from src.exception.resource_not_found_exception import ResourceNotFoundException
from src.middleware.auth import Auth
from src.model import User
from src.service.dashboard_service import DashboardService
from src.service.resume_service import ResumeService
from src.service.user_service import UserService
from src.utils.password import hash_password

app = FastAPI()
app.add_exception_handler(ResourceNotFoundException, resource_not_found_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)

app.add_middleware(Auth)
app.add_middleware(SessionMiddleware, secret_key="my secret key")

templates = Jinja2Templates(directory="src/templates")

@app.get("/")
async def home_page(request:Request):
    user = None

    if request.session.get("is_logged_in"):
        email = request.session.get("current_email")

        async with SessionLocal.begin() as session:
            user_service = UserService(session)
            user = await user_service.find_by_email(email)
    return templates.TemplateResponse(request,"index.html", {"request": request, "user":user})

@app.get("/signup")
async def signup_page(request:Request, message:Optional[str]=None):
    return templates.TemplateResponse(request,"signup.html", {"request": request, "message":message})

@app.post("/signup")
async def signup(request:Request, name:str=Form(...), email:str=Form(...), password:str=Form(...)):
    async with SessionLocal.begin() as session:
        user = User(name=name, email=email, password=hash_password(password))
        user_service = UserService(session)
        user = await user_service.create_user(user)
        print("User created successfully")
        return RedirectResponse("/signin?message=Account created successfully! Please sign in.", status_code=303)

@app.get("/signin")
async def signin_page(request:Request, message:Optional[str]=None):
    return templates.TemplateResponse(request,"signin.html", {"request": request, "message":message})

@app.post("/signin")
async def signin(request:Request, email:str=Form(...), password:str=Form(...)):
    async with SessionLocal.begin() as session:
        user = User(email=email, password=password)
        user_service = UserService(session)
        status = await user_service.authentication(user)
        if status:
            request.session["is_logged_in"] = True
            request.session["current_email"] = email
            return RedirectResponse("/", status_code=303)
        else:
            return RedirectResponse("/signin", status_code=303)

@app.get("/signout")
async def signout(request:Request):
    request.session["is_logged_in"] = None
    request.session["current_email"] = None
    request.session.clear()
    return RedirectResponse("/", status_code=303)

@app.get("/resume/upload")
async def upload_page(request: Request):
    return templates.TemplateResponse(request,"upload_resume.html",{"request": request})

@app.post("/resume/upload")
async def upload_resume(request: Request,file: UploadFile = File(...)):
    async with SessionLocal.begin() as session:
        email = request.session.get("current_email")
        user_service = UserService(session)
        user = await user_service.find_by_email(email)
        resume_service = ResumeService(session)
        await resume_service.upload_resume(file=file,user_id=user.id)
    return RedirectResponse("/dashboard", status_code=303)

@app.get("/dashboard")
async def dashboard(request: Request):
    email = request.session.get(
        "current_email"
    )
    async with SessionLocal.begin() as session:
        user_service = UserService(session)
        user = await user_service.find_by_email(email)
        dashboard_service = DashboardService(session)
        resumes = await dashboard_service.get_dashboard(user.id)
    return templates.TemplateResponse(request,
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "resumes": resumes
        }
    )


@app.get("/resume/{resume_id}")
async def analysis_page(request: Request,resume_id: int):
    async with SessionLocal.begin() as session:
        dashboard_service = DashboardService(session)
        resume = await dashboard_service.get_resume_analysis(resume_id)
    return templates.TemplateResponse(request,"analysis.html",
{"request": request,"resume": resume,"analysis": resume.analysis,"skills":resume.analysis.skills if resume.analysis else []
})

@app.get("/resume/delete/{resume_id}")
async def delete_resume(request: Request,resume_id: int):
    async with SessionLocal.begin() as session:
        resume_service = ResumeService(session)
        await resume_service.delete_resume(
            resume_id
        )
    return RedirectResponse(
        "/dashboard",
        status_code=303
    )