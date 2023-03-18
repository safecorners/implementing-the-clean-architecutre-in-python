from typing import Any, Dict

from sqlalchemy.engine import Connection

from customer_relationship import emails
from customer_relationship.config import CustomerRelationshipConfig
from customer_relationship.email_sender import EmailSender
from customer_relationship.models import customers
from foundation.value_objects import Money


class CustomerRelationshipFacade:
    def __init__(
        self, config: CustomerRelationshipConfig, connection: Connection
    ) -> None:
        self._sender = EmailSender(config)
        self._connection = connection

    def create_customer(self, customer_id: int, email: str) -> None:
        self._connection.execute(
            customers.insert().values({"id": customer_id, "email": email})
        )

    def update_customer(self, customer_id: int, email: str) -> None:
        self._connection.execute(
            customers.update().where(customers.c.id == customer_id).values(email=email)
        )

    def send_email_about_overbid(
        self, customer_id: int, new_price: Money, auction_title: str
    ) -> None:
        email = emails.Overbid(auction_title=auction_title, new_price=new_price)
        customer = self._get_customer(customer_id)
        self._send(customer["email"], email)

    def send_email_about_winning(
        self, customer_id: int, bid_amount: Money, auction_title: str
    ) -> None:
        email = emails.Winning(auction_title=auction_title, amount=bid_amount)
        customer = self._get_customer(customer_id)
        self._send(customer["email"], email)

    def send_email_after_successful_payment(
        self, customer_id: int, paid_price: Money, auction_title: str
    ) -> None:
        email = emails.PaymentSuccessful(
            auction_title=auction_title, paid_price=paid_price
        )
        customer = self._get_customer(customer_id)
        self._send(customer["email"], email)

    def _get_customer(self, customer_id: int) -> Dict[str, Any]:
        row = self._connection.execute(
            customers.select().where(customers.c.id == customer_id)
        ).first()

        return row._asdict()

    def _send(self, recipient: str, email: emails.Email) -> None:
        self._sender.send(recipient, email)
