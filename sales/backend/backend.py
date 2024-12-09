import os
import openai


import reflex as rx
import reflex_clerk as clerk
from sqlmodel import select, asc, desc, or_, func, Session
from .database import get_session, engine
from .config import CLERK_PUBLISHABLE_KEY, CLERK_SECRET_KEY
from .models import User, UserType

products: dict[str, dict] = {
    "T-shirt": {
        "description": "A plain white t-shirt made of 100% cotton.",
        "price": 10.99,
    },
    "Jeans": {
        "description": "A pair of blue denim jeans with a straight leg fit.",
        "price": 24.99,
    },
    "Hoodie": {
        "description": "A black hoodie made of a cotton and polyester blend.",
        "price": 34.99,
    },
    "Cardigan": {
        "description": "A grey cardigan with a V-neck and long sleeves.",
        "price": 36.99,
    },
    "Joggers": {
        "description": "A pair of black joggers made of a cotton and polyester blend.",
        "price": 44.99,
    },
    "Dress": {"description": "A black dress made of 100% polyester.", "price": 49.99},
    "Jacket": {
        "description": "A navy blue jacket made of 100% cotton.",
        "price": 55.99,
    },
    "Skirt": {
        "description": "A brown skirt made of a cotton and polyester blend.",
        "price": 29.99,
    },
    "Shorts": {
        "description": "A pair of black shorts made of a cotton and polyester blend.",
        "price": 19.99,
    },
    "Sweater": {
        "description": "A white sweater with a crew neck and long sleeves.",
        "price": 39.99,
    },
}

_client = None


def get_openai_client():
    global _client
    if _client is None:
        _client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    return _client


class State(rx.State):
    """The app state."""
    current_user: User | None = None
    users: list[User] = []
    products: dict[str, dict] = products
    email_content_data: str = (
        "Click 'Generate Email' to generate a personalized sales email."
    )
    gen_response = False
    tone: str = "😊 Formal"
    length: str = "1000"
    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    def is_admin(self) -> bool:
        """Check if current user is admin."""
        try:
            with Session(engine) as session:
                # Get user by clerk ID
                if clerk.ClerkState.user is None:
                    return False
                clerk_id = clerk.ClerkState.user.id
                user = session.exec(
                    select(User).where(User.clerk_id == clerk_id)
                ).first()
                return user is not None and user.user_type == UserType.ADMIN
        except:
            return False

    def get_or_create_user(self) -> None:
        """Get or create user from Clerk data."""
        try:
            with Session(engine) as session:
                # Check if Clerk user exists
                if clerk.ClerkState.user is None:
                    self.current_user = None
                    return

                # Get user by clerk ID
                clerk_id = clerk.ClerkState.user.id
                user = session.exec(
                    select(User).where(User.clerk_id == clerk_id)
                ).first()
                
                if not user:
                    # Check if user should be admin
                    admin_email = os.getenv("ADMIN_EMAIL")
                    if not clerk.ClerkState.user.email_addresses:
                        self.current_user = None
                        return
                        
                    user_email = clerk.ClerkState.user.email_addresses[0].email_address
                    is_admin = user_email == admin_email
                    
                    # Create new user
                    user = User(
                        email=user_email,
                        clerk_id=clerk_id,
                        user_type=UserType.ADMIN if is_admin else UserType.CUSTOMER,
                    )
                    
                    if not is_admin:
                        # Set customer fields with safe defaults
                        first_name = clerk.ClerkState.user.first_name or ""
                        last_name = clerk.ClerkState.user.last_name or ""
                        user.customer_name = f"{first_name} {last_name}".strip() or "Anonymous"
                        user.age = 0
                        user.gender = ""
                        user.location = ""
                        user.job = ""
                        user.salary = 0
                        
                    session.add(user)
                    session.commit()
                    session.refresh(user)
                
                self.current_user = user
        except Exception as e:
            print(f"Error getting/creating user: {e}")
            self.current_user = None

    def load_entries(self) -> None:
        """Get all users from the database."""
        try:
            self.get_or_create_user()  # Ensure user exists
            if not self.current_user:
                self.users = []
                return

            # with Session(engine) as session:
            #     statement = select(User).where(User.user_type == UserType.CUSTOMER)
            #     if self.search_value:
            #         statement = statement.where(
            #             or_(
            #                 User.customer_name.contains(self.search_value),
            #                 User.email.contains(self.search_value),
            #                 User.location.contains(self.search_value),
            #             )
            #         )
            #     if self.sort_value:
            #         if self.sort_reverse:
            #             statement = statement.order_by(desc(getattr(User, self.sort_value)))
            #         else:
            #             statement = statement.order_by(asc(getattr(User, self.sort_value)))
            #     self.users = session.exec(statement).all()
        except Exception as e:
            print(f"Error loading entries: {e}")
            self.users = []

    def get_user(self, user: User):
        """Set current user, with null check."""
        if user is None:
            self.current_user = None
            return
        self.current_user = user

    def sort_values(self, sort_value: str):
        self.sort_value = sort_value
        self.load_entries()

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        self.load_entries()

    def filter_values(self, search_value):
        self.search_value = search_value
        self.load_entries()

    def add_customer_to_db(self, form_data: dict):
        """Add a customer to the database."""
        with Session(engine) as session:
            customer = User(**form_data)
            session.add(customer)
            session.commit()
            session.refresh(customer)
            self.load_entries()
            return rx.toast.info(
                f"User {customer.customer_name} has been added.",
                position="bottom-right",
            )

    def update_customer_to_db(self, form_data: dict):
        """Update a customer in the database."""
        with Session(engine) as session:
            customer = session.get(User, form_data["id"])
            for key, value in form_data.items():
                setattr(customer, key, value)
            session.add(customer)
            session.commit()
            session.refresh(customer)
            self.load_entries()
            if customer is None:
                return
            return rx.toast.info(
                f"User {customer.customer_name} has been modified.",
                position="bottom-right",
            )

    def delete_customer(self, id: int):
        """Delete a customer from the database."""
        with Session(engine) as session:
            customer = session.get(User, id)
            session.delete(customer)
            session.commit()
            self.load_entries()
            if customer is None:
                return
            return rx.toast.info(
                f"User {customer.customer_name} has been deleted.", position="bottom-right"
            )

    @rx.event(background=True)
    async def call_openai(self):
        if self.current_user is None:
            self.email_content_data = "Error: No user selected"
            self.gen_response = False
            return

        session = get_openai_client().chat.completions.create(
            user=self.router.session.client_token,
            stream=True,
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a salesperson at Reflex, a company that sells clothing. You have a list of products and customer data. Your task is to write a sales email to a customer recommending one of the products. The email should be personalized and include a recommendation based on the customer's data. The email should be {self.tone} and {self.length} characters long.",
                },
                {
                    "role": "user",
                    "content": f"Based on these {products} write a sales email to {self.current_user.customer_name} and email {self.current_user.email} who is {self.current_user.age} years old and a {self.current_user.gender} gender. {self.current_user.customer_name} lives in {self.current_user.location} and works as a {self.current_user.job} and earns {self.current_user.salary} per year. Make sure the email recommends one product only and is personalized to {self.current_user.customer_name}. The company is named Reflex its website is https://reflex.dev.",
                },
            ],
        )
        for item in session:
            if hasattr(item.choices[0].delta, "content"):
                response_text = item.choices[0].delta.content
                async with self:
                    if response_text is not None:
                        self.email_content_data += response_text
                yield

        async with self:
            self.gen_response = False

    def generate_email(self, user: User):
        self.current_user = user
        self.gen_response = True
        self.email_content_data = ""
        return State.call_openai