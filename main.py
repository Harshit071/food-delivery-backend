from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend_models import Base, User, Restaurant, FoodItem, Order
from database import engine, SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from backend_auth import get_password_hash, authenticate_user, create_access_token, get_current_user
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware
import stripe

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Food Delivery Backend is running!"}

@app.post("/register/")
def register_user(name: str, email: str, password: str, address: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(password)
    user = User(name=name, email=email, password=hashed_password, address=address)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=60)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/")
def create_user(name: str, email: str, address: str, db: Session = Depends(get_db)):
    user = User(name=name, email=email, address=address)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/users/")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.post("/restaurants/")
def create_restaurant(name: str, address: str, db: Session = Depends(get_db)):
    restaurant = Restaurant(name=name, address=address)
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant

@app.get("/restaurants/")
def list_restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).all()

@app.post("/food_items/")
def create_food_item(name: str, price: float, restaurant_id: int, db: Session = Depends(get_db)):
    food_item = FoodItem(name=name, price=price, restaurant_id=restaurant_id)
    db.add(food_item)
    db.commit()
    db.refresh(food_item)
    return food_item

@app.get("/food_items/")
def list_food_items(db: Session = Depends(get_db)):
    return db.query(FoodItem).all()

@app.post("/orders/")
def create_order(user_id: int = None, food_item_id: int = None, quantity: int = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Use current_user.id for user_id
    order = Order(user_id=current_user.id, food_item_id=food_item_id, quantity=quantity)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@app.get("/orders/")
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

# Stripe configuration (replace with your test secret key)
stripe.api_key = "sk_test_..."  # TODO: Replace with your Stripe test secret key

@app.post("/create-payment-intent/")
def create_payment_intent(amount: int, currency: str = "usd"):
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,  # in cents
            currency=currency,
            payment_method_types=["card"],
        )
        return {"clientSecret": intent["client_secret"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )    