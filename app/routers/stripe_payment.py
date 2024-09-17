from typing import Annotated, List

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.dependencies.auth import get_current_user
from app.models.stripe_payment import StripePayment
from app.schemas.stripe_payment import PaymentCreate, PaymentUpdate

from ..database import get_async_db

router = APIRouter(prefix="/stripe-payments", tags=["stripe-payments"])

db_dep = Annotated[AsyncSession, Depends(get_async_db)]
current_user_dep = Annotated[dict, Depends(get_current_user)]

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

@router.post("/")
async def create_payment_intent(payment: PaymentCreate, db: db_dep, current_user: current_user_dep):
    try:
        intent = stripe.PaymentIntent.create(
            amount=payment.amount,
            currency=payment.currency
        )
        
        # db_payment = StripePayment(
        #     amount=payment.amount,
        #     currency=payment.currency,
        #     status="pending",
        #     stripe_payment_intent_id=intent.id
        # )
        # db.add(db_payment)
        # await db.commit()
        # await db.refresh(db_payment)
        
        # return {"clientSecret": intent.client_secret, "paymentId": db_payment.id}
        return {"clientSecret": intent.client_secret, }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/update-payment-status")
async def update_payment_status(payment_update: PaymentUpdate, db: db_dep, current_user: current_user_dep):
    db_payment = await  StripePayment.get(db, [StripePayment.id == payment_update.payment_id])
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    db_payment.status = payment_update.status
    if payment_update.failure_code:
        db_payment.failure_code = payment_update.failure_code
    if payment_update.failure_message:
        db_payment.failure_message = payment_update.failure_message
    await db.commit()
    await db.refresh(db_payment)
    
    return {"message": "Payment status updated successfully"}

@router.post("/webhook/")
async def stripe_webhook(request: Request, db: db_dep):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Database update logic (Example: AsyncSession injection)
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        payment_id = payment_intent['id']
        # Update the payment status in the database
        await StripePayment.update(db, payment_id, status="succeeded")
        await db.commit()

    elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            payment_id = payment_intent['id']
            failure_reason = payment_intent['last_payment_error']['message']
            # Update the failure status in the database
            await StripePayment.update(db, payment_id, status="failed", failure_reason=failure_reason)
            await db.commit()

    return {"status": "success"}